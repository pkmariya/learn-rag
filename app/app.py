#!/usr/bin/env python3
"""
Ask Mariya's Wiki anything about RAG.

A small Flask app that answers questions purely by retrieval over the
wiki/*.md content (TF-IDF-lite keyword scoring, no LLM, no external API for
answering). If nothing scores above SCORE_THRESHOLD, it says so honestly and
offers a feedback form; submissions are filed as a GitHub Issue for manual
review (never auto-written into the wiki).
"""
import os
import re
import math
import html as htmllib

from flask import Flask, request, render_template, redirect, url_for
import markdown
import requests

APP_DIR = os.path.dirname(os.path.abspath(__file__))
WIKI_DIR = os.path.join(os.path.dirname(APP_DIR), "wiki")

WIKILINK_RE = re.compile(r"\[\[([^\]|]+?)(?:\|([^\]]+))?\]\]")
SKIP_HEADINGS = {"related pages", "related page", "sources"}
STOPWORDS = set("""a an the is are was were be been being of in on at to for and or but
what how why when where which who whom does do did can could should would will
with this that these those it its as by from about into than then so if not no yes
i you me my your""".split())

GITHUB_TOKEN = os.environ.get("WIKI_FEEDBACK_TOKEN", "")
GITHUB_REPO = os.environ.get("GITHUB_REPO", "pkmariya/learn-rag")
SCORE_THRESHOLD = float(os.environ.get("SCORE_THRESHOLD", "1.8"))
APP_TITLE = "Ask Mariya's Wiki anything about RAG"

app = Flask(__name__)


# ---------- wiki loading & chunking ----------

def load_pages():
    pages = {}
    for fname in sorted(os.listdir(WIKI_DIR)):
        if not fname.endswith(".md") or fname == "log.md":
            continue
        slug = fname[:-3]
        with open(os.path.join(WIKI_DIR, fname), encoding="utf-8") as f:
            text = f.read()
        m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        title = m.group(1).strip() if m else slug
        pages[slug] = {"title": title, "raw": text}
    return pages


def normalize_key(s):
    return s.strip().rstrip("\\").strip().lower().replace(" ", "-")


def resolve_wikilinks(text, pages):
    lookup = {normalize_key(slug): slug for slug in pages}

    def repl(m):
        target = m.group(1).strip().rstrip("\\").strip()
        label = (m.group(2) or target).strip().rstrip("\\").strip()
        slug = lookup.get(normalize_key(target))
        if slug:
            return f'<a class="wikilink" href="/wiki/{slug}">{label}</a>'
        return f'<span class="wikilink broken" title="page not found">{label}</span>'
    return WIKILINK_RE.sub(repl, text)


def heading_slug(text):
    s = re.sub(r"[^a-z0-9]+", "-", text.strip().lower()).strip("-")
    return s or "section"


def strip_markdown(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = WIKILINK_RE.sub(lambda m: (m.group(2) or m.group(1)).strip().rstrip("\\"), text)
    text = re.sub(r"[#*`_>]", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\|", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def split_sections(raw_md):
    body = re.sub(r"^#\s+.+$", "", raw_md, count=1, flags=re.MULTILINE)
    parts = re.split(r"^##\s+(.+)$", body, flags=re.MULTILINE)
    sections = []
    preamble = parts[0].strip()
    if preamble:
        sections.append(("Overview", preamble))
    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        text = parts[i + 1] if i + 1 < len(parts) else ""
        sections.append((heading, text))
    return sections


def build_chunks(pages):
    chunks = []
    for slug, page in pages.items():
        if slug == "index":
            continue
        for heading, text in split_sections(page["raw"]):
            if heading.lower() in SKIP_HEADINGS:
                continue
            plain = strip_markdown(text)
            if len(plain) < 20:
                continue
            chunks.append({
                "slug": slug,
                "title": page["title"],
                "heading": heading,
                "anchor": heading_slug(heading),
                "text": plain,
            })
    return chunks


PAGES = load_pages()
CHUNKS = build_chunks(PAGES)


# ---------- retrieval (TF-IDF-lite) ----------

def tokenize(s):
    return re.findall(r"[a-z0-9]+", s.lower())


def compute_idf(q_tokens):
    n = len(CHUNKS)
    idf = {}
    for t in q_tokens:
        if t in STOPWORDS or len(t) < 2 or t in idf:
            continue
        df = sum(1 for c in CHUNKS if t in c["text"].lower())
        idf[t] = math.log((n + 1) / (df + 1)) + 0.15
    return idf


def score_chunk(q_tokens, idf, chunk):
    text_lower = chunk["text"].lower()
    heading_lower = chunk["heading"].lower()
    title_lower = chunk["title"].lower()
    score = 0.0
    for t in q_tokens:
        if t in STOPWORDS or len(t) < 2:
            continue
        w = idf.get(t, 0.15)
        count = len(re.findall(r"\b" + re.escape(t) + r"\b", text_lower))
        # Log-damped term frequency: a section that repeats the term in a
        # dense bullet list (e.g. "Standard RAG... Corrective RAG...
        # Fusion RAG...") shouldn't out-rank a section that actually
        # explains the term once or twice in plain prose.
        term_component = math.log1p(count) if count else 0.0
        heading_bonus = 4 if t in heading_lower else 0
        title_bonus = 2 if t in title_lower else 0
        score += (term_component + heading_bonus + title_bonus) * w
    base = score
    # Prefer canonical definitional sections ("Overview" / "What is X?")
    # once a chunk already has *some* real relevance -- people expect a
    # definition to live in a page's intro, not wherever the term happens
    # to be repeated most. Gated on a minimum base score so this doesn't
    # rescue chunks that only mention the term in passing.
    if base >= 1.2 and (heading_lower == "overview" or heading_lower.startswith("what is")):
        score += 2.5
    return score / math.sqrt(len(chunk["text"]) / 200 + 1)


def rank(question):
    q_tokens = [t for t in tokenize(question) if t not in STOPWORDS and len(t) >= 2]
    if not q_tokens:
        return [], q_tokens
    idf = compute_idf(q_tokens)
    unique_q = list(set(q_tokens))
    total_weight = sum(idf.get(t, 0.15) for t in unique_q) or 1.0

    # Require at least half of the question's "information weight" (by idf)
    # to actually be present in a chunk. This stops a single incidental,
    # common-word match (e.g. "best" or "capital" in an unrelated example)
    # from masquerading as a real answer, while still letting one truly
    # distinctive term (e.g. "reranking") carry a match on its own.
    scored = []
    for c in CHUNKS:
        text_lower = c["text"].lower()
        matched_weight = sum(
            idf.get(t, 0.15) for t in unique_q
            if re.search(r"\b" + re.escape(t) + r"\b", text_lower)
        )
        if matched_weight / total_weight < 0.5:
            continue
        s = score_chunk(q_tokens, idf, c)
        if s > 0:
            scored.append((s, c))
    scored.sort(key=lambda x: -x[0])
    return scored, q_tokens


def highlight(text, q_tokens):
    escaped = htmllib.escape(text)
    for t in q_tokens:
        if t in STOPWORDS or len(t) < 2:
            continue
        escaped = re.sub(f"({re.escape(t)})", r"<mark>\1</mark>", escaped, flags=re.IGNORECASE)
    return escaped


def snippet(text, max_len=500):
    if len(text) <= max_len:
        return text
    return text[:max_len].strip() + "…"


# ---------- routes ----------

@app.route("/")
def index():
    question = request.args.get("q", "").strip()
    feedback_status = request.args.get("feedback")
    results = None
    no_match = False

    if question:
        scored, q_tokens = rank(question)
        top = scored[:5]
        best_score = top[0][0] if top else 0
        if not top or best_score < SCORE_THRESHOLD:
            no_match = True
        else:
            results = []
            for score, c in top:
                results.append({
                    "heading": c["heading"],
                    "title": c["title"],
                    "slug": c["slug"],
                    "anchor": c["anchor"],
                    "snippet": highlight(snippet(c["text"]), q_tokens),
                })

    return render_template(
        "index.html",
        app_title=APP_TITLE,
        question=question,
        results=results,
        no_match=no_match,
        feedback_status=feedback_status,
    )


@app.route("/feedback", methods=["POST"])
def feedback():
    question = request.form.get("question", "").strip()
    answer = request.form.get("answer", "").strip()
    status = "error"

    if question and GITHUB_TOKEN:
        title = f"Wiki gap: {question[:80]}"
        body = (
            f"**Question asked on the site:**\n\n{question}\n\n"
            f"**Visitor-submitted info:**\n\n{answer or '_(none provided)_'}\n\n"
            f"---\n_Submitted via the Ask-the-Wiki feedback form. "
            f"Review before adding to wiki/*.md — not auto-merged._"
        )
        try:
            resp = requests.post(
                f"https://api.github.com/repos/{GITHUB_REPO}/issues",
                headers={
                    "Authorization": f"token {GITHUB_TOKEN}",
                    "Accept": "application/vnd.github+json",
                },
                json={"title": title, "body": body, "labels": ["wiki-feedback"]},
                timeout=10,
            )
            if resp.status_code == 201:
                status = "ok"
        except requests.RequestException:
            pass

    return redirect(url_for("index", q=question, feedback=status))


@app.route("/wiki/<slug>")
def wiki_page(slug):
    page = PAGES.get(slug)
    if not page:
        return render_template("404.html", slug=slug), 404
    body_md = resolve_wikilinks(page["raw"], PAGES)
    body_html = markdown.markdown(body_md, extensions=["tables", "fenced_code", "toc"])
    return render_template("page.html", title=page["title"], body=body_html)


@app.route("/healthz")
def healthz():
    return {"status": "ok", "pages": len(PAGES), "chunks": len(CHUNKS)}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
