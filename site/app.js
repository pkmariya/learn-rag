
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
