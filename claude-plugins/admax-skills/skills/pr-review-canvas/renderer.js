function esc(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// Parse original hunk lines before any presentation decisions.
function parseDiff(input) {
  var lines = Array.isArray(input) ? input : String(input || '').split('\n');
  var rows = [], oldLine = 0, newLine = 0, inHunk = false;
  lines.forEach(function(line) {
    var match = line.match(/^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@/);
    if (match) {
      oldLine = Number(match[1]); newLine = Number(match[2]); inHunk = true;
      rows.push({type: 'hunk', code: line});
    } else if (inHunk && line.startsWith('+')) {
      rows.push({type: 'add', code: line.slice(1), newLine: newLine++});
    } else if (inHunk && line.startsWith('-')) {
      rows.push({type: 'del', code: line.slice(1), oldLine: oldLine++});
    } else if (inHunk && line.startsWith(' ')) {
      rows.push({type: 'ctx', code: line.slice(1), oldLine: oldLine++, newLine: newLine++});
    } else if (line) {
      // Includes no-newline markers, binary notices, and extended headers.
      rows.push({type: 'hunk', code: line});
      if (line.startsWith('diff ')) inHunk = false;
    }
  });
  return rows;
}

function renderDiff(target, input) {
  var el = typeof target === 'string' ? document.getElementById(target) : target;
  if (!el) return;
  var rows = parseDiff(input);
  el.innerHTML = rows.length ? '<table class="diff-table"><tbody>' + rows.map(function(row) {
    return '<tr class="diff-' + row.type + '"><td class="diff-ln">' +
      (row.oldLine === undefined ? '' : row.oldLine) + '</td><td class="diff-ln">' +
      (row.newLine === undefined ? '' : row.newLine) + '</td><td class="diff-code">' +
      esc(row.code) + '</td></tr>';
  }).join('') + '</tbody></table>' : '<p>Patch unavailable; inspect the source diff.</p>';
}

if (typeof document !== 'undefined') {
  document.addEventListener('DOMContentLoaded', function() {
    var data = document.getElementById('pr-diffs-json');
    if (!data) return;
    var patches = JSON.parse(data.textContent);
    document.querySelectorAll('[data-diff]').forEach(function(el) {
      renderDiff(el, patches[el.getAttribute('data-diff')]);
    });
  });
}
if (typeof module !== 'undefined') module.exports = {parseDiff: parseDiff, renderDiff: renderDiff};
