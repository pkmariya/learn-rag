#!/usr/bin/env python3
"""
Static site generator for the Learn-RAG wiki.

Reads markdown pages from wiki/*.md, resolves [[wiki-links]], and renders
a browsable static HTML site (sidebar nav, search) into site/.

Usage: python3 build.py <repo_root>
    repo_root defaults to the current directory. Expects repo_root/wiki/*.md.
Output: repo_root/site/
"""
import sys
import os
import re
import json
import shutil
import markdown
from datetime import datetime

WIKILINK_RE = re.compile(r"\[\[([^\]|]+?)(?:\|([^\]]+))?\]\]")


def slugify(name):
    return name.strip()


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
        summary_match = re.search(r"\*\*Summary\*\*:\s*(.+)", text)
        summary = summary_match.group(1).strip() if summary_match else ""
        pages[slug] = {"title": title, "summary": summary, "raw": text}
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


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Learn RAG Wiki</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="layout">
  <nav class="sidebar">
    <div class="sidebar-header"><a href="index.html">Learn RAG Wiki</a></div>
    <input type="text" id="search-box" placeholder="Search wiki...">
    <div id="search-results"></div>
    <div id="nav-tree">{nav}</div>
  </nav>
  <main class="content">
    <article>
{body}
    </article>
  </main>
</div>
<script src="search-data.js"></script>
<script src="app.js"></script>
</body>
</html>
"""

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Learn RAG Wiki</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="layout">
  <nav class="sidebar">
    <div class="sidebar-header"><a href="index.html">Learn RAG Wiki</a></div>
    <input type="text" id="search-box" placeholder="Search wiki...">
    <div id="search-results"></div>
    <div id="nav-tree">{nav}</div>
  </nav>
  <main class="content">
    <article>
{body}
    </article>
  </main>
</div>
<script src="search-data.js"></script>
<script src="app.js"></script>
</body>
</html>
"""

CSS = """
:root {
  --bg: #ffffff;
  --sidebar-bg: #f7f6f3;
  --border: #e5e3de;
  --text: #1b1b18;
  --muted: #6b6b63;
  --accent: #a8622a;
  --accent-bg: #f0e6dc;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--text); line-height: 1.6; }
.layout { display: flex; min-height: 100vh; }
.sidebar {
  width: 280px;
  flex-shrink: 0;
  background: var(--sidebar-bg);
  border-right: 1px solid var(--border);
  padding: 16px;
  overflow-y: auto;
  position: sticky;
  top: 0;
  height: 100vh;
}
.sidebar-header a {
  font-weight: 700;
  font-size: 1.05rem;
  color: var(--text);
  text-decoration: none;
}
#search-box {
  width: 100%;
  margin: 12px 0;
  padding: 8px 10px;
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 0.9rem;
}
#search-results {
  margin-bottom: 8px;
}
#search-results a {
  display: block;
  padding: 6px 8px;
  border-radius: 4px;
  color: var(--text);
  text-decoration: none;
  font-size: 0.88rem;
  background: var(--accent-bg);
  margin-bottom: 4px;
}
#search-results a:hover { background: #e6d5c4; }
#nav-tree h3 {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--muted);
  margin: 18px 0 6px;
}
#nav-tree ul { list-style: none; padding-left: 0; margin: 0; }
#nav-tree li { margin: 2px 0; }
#nav-tree a {
  display: block;
  padding: 4px 8px;
  border-radius: 4px;
  color: var(--text);
  text-decoration: none;
  font-size: 0.9rem;
}
#nav-tree a:hover, #nav-tree a.active { background: var(--accent-bg); }
.content { flex: 1; padding: 40px 48px; max-width: 860px; }
article h1 { font-size: 1.9rem; margin-bottom: 4px; }
article h2 { font-size: 1.3rem; margin-top: 2em; border-bottom: 1px solid var(--border); padding-bottom: 4px; }
article h3 { font-size: 1.05rem; margin-top: 1.5em; }
article p { margin: 0.8em 0; }
article code { background: var(--accent-bg); padding: 2px 5px; border-radius: 4px; font-size: 0.88em; }
article pre { background: #24211d; color: #f2ede6; padding: 14px 16px; border-radius: 8px; overflow-x: auto; }
article pre code { background: none; color: inherit; padding: 0; }
article table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 0.92rem; }
article th, article td { border: 1px solid var(--border); padding: 6px 10px; text-align: left; }
article th { background: var(--sidebar-bg); }
a.wikilink { color: var(--accent); text-decoration: none; border-bottom: 1px dotted var(--accent); }
a.wikilink:hover { border-bottom-style: solid; }
.wikilink.broken { color: var(--muted); border-bottom: 1px dotted var(--muted); cursor: help; }
hr { border: none; border-top: 1px solid var(--border); margin: 1.5em 0; }
@media (max-width: 800px) {
  .layout { flex-direction: column; }
  .sidebar { width: 100%; height: auto; position: static; }
  .content { padding: 24px; }
}
"""

APP_JS = """
(function() {
  var box = document.getElementById('search-box');
  var results = document.getElementById('search-results');
  var navTree = document.getElementById('nav-tree');
  if (!box) return;

  function render(matches) {
    results.innerHTML = '';
    if (!matches.length) return;
    matches.slice(0, 12).forEach(function(m) {
      var a = document.createElement('a');
      a.href = m.slug + '.html';
      a.textContent = m.title;
      results.appendChild(a);
    });
  }

  box.addEventListener('input', function() {
    var q = box.value.trim().toLowerCase();
    if (!q) { render([]); navTree.style.display = ''; return; }
    navTree.style.display = 'none';
    var matches = SEARCH_DATA.filter(function(p) {
      return p.title.toLowerCase().indexOf(q) !== -1 ||
             p.summary.toLowerCase().indexOf(q) !== -1 ||
             p.text.toLowerCase().indexOf(q) !== -1;
    });
    render(matches);
  });

  // Highlight current page in nav
  var current = window.location.pathname.split('/').pop();
  document.querySelectorAll('#nav-tree a').forEach(function(a) {
    if (a.getAttribute('href') === current) a.classList.add('active');
  });
})();
"""


def build_nav(index_text, pages):
    """Turn index.md's '## Section' + '- [[slug]] — desc' structure into sidebar HTML."""
    html = []
    lines = index_text.splitlines()
    in_list = False
    for line in lines:
        h2 = re.match(r"^##\s+(.+)$", line)
        item = re.match(r"^-\s+\[\[([^\]]+)\]\]", line)
        if h2:
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<h3>{h2.group(1).strip()}</h3><ul>")
            in_list = True
        elif item:
            slug = item.group(1).strip()
            title = pages.get(slug, {}).get("title", slug)
            html.append(f'<li><a href="{slug}.html">{title}</a></li>')
    if in_list:
        html.append("</ul>")
    return "\n".join(html)


def strip_markdown_for_search(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"[#*`_>\[\]]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()[:2000]


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
    index_raw = pages.get("index", {}).get("raw", "")
    nav_html = build_nav(index_raw, pages)

    search_data = []

    for slug, page in pages.items():
        body_md = resolve_wikilinks(page["raw"], pages)
        body_html = markdown.markdown(
            body_md, extensions=["tables", "fenced_code", "toc"]
        )
        template = INDEX_TEMPLATE if slug == "index" else PAGE_TEMPLATE
        out = template.format(title=page["title"], nav=nav_html, body=body_html)
        with open(os.path.join(site_dir, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(out)
        search_data.append({
            "slug": slug,
            "title": page["title"],
            "summary": page["summary"],
            "text": strip_markdown_for_search(page["raw"]),
        })

    with open(os.path.join(site_dir, "style.css"), "w", encoding="utf-8") as f:
        f.write(CSS)
    with open(os.path.join(site_dir, "app.js"), "w", encoding="utf-8") as f:
        f.write(APP_JS)
    with open(os.path.join(site_dir, "search-data.js"), "w", encoding="utf-8") as f:
        f.write("var SEARCH_DATA = " + json.dumps(search_data) + ";")

    # Redirect root -> index.html for convenience if server doesn't do it
    print(f"Built {len(pages)} pages into {site_dir} at {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
