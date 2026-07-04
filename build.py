#!/usr/bin/env python3
"""
Static site generator for the Learn-RAG wiki.

Generates a Q&A-style homepage: the user types a question, and client-side
JS ranks chunks of wiki content (by section) against it and shows the best
matching passages with a citation link back to the full wiki page. No
backend, no LLM, no API key -- pure client-side keyword retrieval.

Individual wiki pages are still rendered (wiki-links resolved) so citation
links have somewhere to go, but they are no longer the primary interface.

Usage: python3 build.py <repo_root>
    repo_root defaults to the current directory. Expects repo_root/wiki/*.md.
Output: repo_root/site/
"""
import sys
import os
import re
import json
import markdown
from datetime import datetime

WIKILINK_RE = re.compile(r"\[\[([^\]|]+?)(?:\|([^\]]+))?\]\]")
SKIP_HEADINGS = {"related pages", "related page", "sources"}


def load_pages(wiki_dir):
    pages = {}
    for fname in sorted(os.listdir(wiki_dir)):
        if not fname.endswith(".md"):
            continue
        if fname in ("log.md",):
            continue
        slug = fname[:-3]
        path = os.path.join(wiki_dir, fname)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else slug
        pages[slug] = {"title": title, "raw": text}
    return pages


def normalize_key(s):
    s = s.strip().rstrip("\\").strip()
    return s.lower().replace(" ", "-")


def resolve_wikilinks(text, pages):
    lookup = {normalize_key(slug): slug for slug in pages}

    def repl(m):
        raw_target = m.group(1).strip().rstrip("\\").strip()
        label = (m.group(2) or raw_target).strip().rstrip("\\").strip()
        key = normalize_key(raw_target)
        slug = lookup.get(key)
        if slug:
            return f'<a class="wikilink" href="{slug}.html">{label}</a>'
        return f'<span class="wikilink broken" title="page not found">{label}</span>'
    return WIKILINK_RE.sub(repl, text)


def heading_slug(text):
    s = text.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
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
    """Split page body (after the H1 title line) into (heading, text) chunks
    on '## ' boundaries. The preamble before the first '## ' becomes 'Overview'."""
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


def build_qa_chunks(pages):
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


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Learn RAG Wiki</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="page">
    <a class="back-link" href="index.html">&larr; Ask a question</a>
    <article>
{body}
    </article>
  </div>
</body>
</html>
"""

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ask the RAG Wiki</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="qa-page">
    <header class="qa-header">
      <h1>Ask the RAG Wiki</h1>
      <p class="qa-sub">Ask a question about Retrieval-Augmented Generation. Answers are pulled straight from the wiki content below &mdash; no external AI, just search over what's already written here.</p>
    </header>
    <form id="qa-form" class="qa-form" autocomplete="off">
      <input type="text" id="qa-input" placeholder="e.g. What is hybrid retrieval?" autocomplete="off">
      <button type="submit">Ask</button>
    </form>
    <div id="qa-results"></div>
  </div>
  <script src="qa-data.js"></script>
  <script src="app.js"></script>
</body>
</html>
"""

CSS = """
:root {
  --bg: #ffffff;
  --panel-bg: #f7f6f3;
  --border: #e5e3de;
  --text: #1b1b18;
  --muted: #6b6b63;
  --accent: #a8622a;
  --accent-bg: #f0e6dc;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--text); line-height: 1.6; }

/* Q&A homepage */
.qa-page { max-width: 720px; margin: 0 auto; padding: 64px 24px 80px; }
.qa-header h1 { font-size: 2.1rem; margin-bottom: 8px; }
.qa-sub { color: var(--muted); font-size: 1rem; margin-bottom: 32px; }
.qa-form { display: flex; gap: 8px; margin-bottom: 8px; }
#qa-input {
  flex: 1;
  padding: 14px 16px;
  font-size: 1rem;
  border: 1px solid var(--border);
  border-radius: 8px;
}
.qa-form button {
  padding: 14px 22px;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  background: var(--accent);
  color: white;
  cursor: pointer;
}
.qa-form button:hover { opacity: 0.9; }
#qa-results { margin-top: 32px; display: flex; flex-direction: column; gap: 16px; }
.qa-card {
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 18px 20px;
  background: var(--panel-bg);
}
.qa-card h3 { margin: 0 0 8px; font-size: 1.05rem; }
.qa-card p { margin: 0 0 10px; color: var(--text); }
.qa-card mark { background: #f5d7ae; color: inherit; padding: 0 2px; border-radius: 2px; }
.qa-source { font-size: 0.85rem; color: var(--accent); text-decoration: none; }
.qa-source:hover { text-decoration: underline; }
.qa-empty { color: var(--muted); }

/* Individual wiki page view (reached via citation links) */
.page { max-width: 780px; margin: 0 auto; padding: 32px 24px 80px; }
.back-link { color: var(--accent); text-decoration: none; font-size: 0.9rem; }
.back-link:hover { text-decoration: underline; }
article h1 { font-size: 1.9rem; margin: 24px 0 4px; }
article h2 { font-size: 1.3rem; margin-top: 2em; border-bottom: 1px solid var(--border); padding-bottom: 4px; }
article h3 { font-size: 1.05rem; margin-top: 1.5em; }
article p { margin: 0.8em 0; }
article code { background: var(--accent-bg); padding: 2px 5px; border-radius: 4px; font-size: 0.88em; }
article pre { background: #24211d; color: #f2ede6; padding: 14px 16px; border-radius: 8px; overflow-x: auto; }
article pre code { background: none; color: inherit; padding: 0; }
article table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 0.92rem; }
article th, article td { border: 1px solid var(--border); padding: 6px 10px; text-align: left; }
article th { background: var(--panel-bg); }
a.wikilink { color: var(--accent); text-decoration: none; border-bottom: 1px dotted var(--accent); }
a.wikilink:hover { border-bottom-style: solid; }
.wikilink.broken { color: var(--muted); border-bottom: 1px dotted var(--muted); cursor: help; }
hr { border: none; border-top: 1px solid var(--border); margin: 1.5em 0; }
@media (max-width: 600px) {
  .qa-form { flex-direction: column; }
}
"""

APP_JS = """
(function() {
  var form = document.getElementById('qa-form');
  var input = document.getElementById('qa-input');
  var results = document.getElementById('qa-results');
  if (!form || typeof QA_DATA === 'undefined') return;

  var STOPWORDS = ["a","an","the","is","are","was","were","be","been","being",
    "of","in","on","at","to","for","and","or","but","what","how","why","when",
    "where","which","who","whom","does","do","did","can","could","should",
    "would","will","with","this","that","these","those","it","its","as","by",
    "from","about","into","than","then","so","if","not","no","yes","i","you",
    "me","my","your"];
  var STOP = {};
  STOPWORDS.forEach(function(w){ STOP[w] = true; });

  function escapeRe(s) { return s.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&'); }

  function tokenize(s) {
    return (s.toLowerCase().match(/[a-z0-9]+/g) || []);
  }

  // TF-IDF-lite: down-weight terms (like "rag") that appear in almost every
  // chunk, so topic-specific words actually drive the ranking.
  function computeIdf(qTokens) {
    var idf = {};
    var N = QA_DATA.length;
    qTokens.forEach(function(t) {
      if (STOP[t] || t.length < 2 || idf[t] !== undefined) return;
      var df = 0;
      for (var i = 0; i < QA_DATA.length; i++) {
        if (QA_DATA[i].text.toLowerCase().indexOf(t) !== -1) df++;
      }
      idf[t] = Math.log((N + 1) / (df + 1)) + 0.15;
    });
    return idf;
  }

  function scoreChunk(qTokens, idf, chunk) {
    var textLower = chunk.text.toLowerCase();
    var headingLower = chunk.heading.toLowerCase();
    var titleLower = chunk.title.toLowerCase();
    var score = 0;
    qTokens.forEach(function(t) {
      if (STOP[t] || t.length < 2) return;
      var w = idf[t] || 0.15;
      var re = new RegExp('\\\\b' + escapeRe(t) + '\\\\b', 'g');
      var textMatches = (textLower.match(re) || []).length;
      var headingBonus = headingLower.indexOf(t) !== -1 ? 2 : 0;
      var titleBonus = titleLower.indexOf(t) !== -1 ? 1 : 0;
      score += (textMatches + headingBonus + titleBonus) * w;
    });
    return score / Math.sqrt(chunk.text.length / 200 + 1);
  }

  function highlight(text, qTokens) {
    var escaped = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    qTokens.forEach(function(t) {
      if (STOP[t] || t.length < 2) return;
      var re = new RegExp('(' + escapeRe(t) + ')', 'ig');
      escaped = escaped.replace(re, '<mark>$1</mark>');
    });
    return escaped;
  }

  function snippet(text, maxLen) {
    if (text.length <= maxLen) return text;
    return text.slice(0, maxLen).trim() + '\\u2026';
  }

  function render(matches, query) {
    results.innerHTML = '';
    if (!query.trim()) return;
    if (!matches.length) {
      results.innerHTML = '<p class="qa-empty">No matching content found in the wiki for that question. Try different wording.</p>';
      return;
    }
    var qTokens = tokenize(query);
    matches.slice(0, 5).forEach(function(m) {
      var card = document.createElement('div');
      card.className = 'qa-card';
      var snip = snippet(m.text, 500);
      var h3 = document.createElement('h3');
      h3.textContent = m.heading;
      var p = document.createElement('p');
      p.innerHTML = highlight(snip, qTokens);
      var a = document.createElement('a');
      a.className = 'qa-source';
      a.href = m.slug + '.html#' + m.anchor;
      a.textContent = 'Source: ' + m.title + ' \\u2192';
      card.appendChild(h3);
      card.appendChild(p);
      card.appendChild(a);
      results.appendChild(card);
    });
  }

  function ask(query) {
    var allTokens = tokenize(query);
    var qTokens = allTokens.filter(function(t) { return !STOP[t]; });
    if (!qTokens.length) { render([], query); return; }
    var idf = computeIdf(qTokens);
    var scored = QA_DATA.map(function(chunk) {
      return { chunk: chunk, score: scoreChunk(qTokens, idf, chunk) };
    }).filter(function(x) { return x.score > 0; });
    scored.sort(function(a, b) { return b.score - a.score; });
    render(scored.map(function(x) { return x.chunk; }), query);
  }

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    ask(input.value);
  });
})();
"""


def main():
    repo_root = sys.argv[1] if len(sys.argv) > 1 else "."
    wiki_dir = os.path.join(repo_root, "wiki")
    site_dir = os.path.join(repo_root, "site")

    if not os.path.isdir(wiki_dir):
        print(f"error: {wiki_dir} not found")
        sys.exit(1)

    # Note: we intentionally never delete/rename files here (only create or
    # overwrite-in-place via open(...,"w")) since the target folder may be a
    # mounted workspace that disallows delete/rename of existing files.
    os.makedirs(site_dir, exist_ok=True)

    pages = load_pages(wiki_dir)
    qa_chunks = build_qa_chunks(pages)

    for slug, page in pages.items():
        body_md = resolve_wikilinks(page["raw"], pages)
        body_html = markdown.markdown(
            body_md, extensions=["tables", "fenced_code", "toc"]
        )
        out = PAGE_TEMPLATE.format(title=page["title"], body=body_html)
        with open(os.path.join(site_dir, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(out)

    with open(os.path.join(site_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(INDEX_TEMPLATE)

    with open(os.path.join(site_dir, "style.css"), "w", encoding="utf-8") as f:
        f.write(CSS)
    with open(os.path.join(site_dir, "app.js"), "w", encoding="utf-8") as f:
        f.write(APP_JS)
    with open(os.path.join(site_dir, "qa-data.js"), "w", encoding="utf-8") as f:
        f.write("var QA_DATA = " + json.dumps(qa_chunks) + ";")

    print(f"Built {len(pages)} pages and {len(qa_chunks)} Q&A chunks into {site_dir} at {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
