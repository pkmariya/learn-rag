
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

  function escapeRe(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }

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
      var re = new RegExp('\\b' + escapeRe(t) + '\\b', 'g');
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
    return text.slice(0, maxLen).trim() + '\u2026';
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
      a.textContent = 'Source: ' + m.title + ' \u2192';
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
