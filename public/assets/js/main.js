/* Z.R. Tool Inc. — site behaviour (no dependencies) */
(function () {
  'use strict';

  /* ---------- Mobile navigation ---------- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.textContent = open ? 'Close' : 'Menu';
    });
  }

  /* ---------- Document availability (manuals / trade sheets) ----------
     Every download link starts as a "pending" state that works with no JS
     (it opens an email request). When the matching PDF has been uploaded
     to /downloads/…, this check quietly upgrades it to a real download. */
  var docLinks = document.querySelectorAll('[data-doc]');
  if (docLinks.length && window.fetch && location.protocol.indexOf('http') === 0) {
    docLinks.forEach(function (el) {
      var url = el.getAttribute('data-doc');
      fetch(url, { method: 'HEAD' })
        .then(function (res) {
          var type = (res.headers.get('content-type') || '').toLowerCase();
          if (res.ok && type.indexOf('pdf') !== -1) {
            el.classList.remove('doc-pending');
            el.classList.add('doc-link');
            el.setAttribute('href', url);
            el.removeAttribute('target');
            var st = el.querySelector('.st');
            if (st) st.textContent = 'PDF';
          }
        })
        .catch(function () { /* keep request-by-email fallback */ });
    });
  }

  /* ---------- Product filter (catalog page) ---------- */
  var filterbar = document.getElementById('tool-filter');
  if (filterbar) {
    var cards = Array.prototype.slice.call(document.querySelectorAll('[data-widths]'));
    var state = { width: 'all', power: 'all' };

    function apply() {
      var shown = 0;
      cards.forEach(function (card) {
        var widths = card.getAttribute('data-widths').split(' ');
        var power = card.getAttribute('data-power');
        var okW = state.width === 'all' || widths.indexOf(state.width) !== -1;
        var okP = state.power === 'all' || power === state.power;
        var show = okW && okP;
        card.classList.toggle('is-hidden', !show);
        if (show) shown++;
      });
      var count = document.getElementById('filter-count');
      if (count) count.textContent = shown + ' of ' + cards.length + ' tools shown';
    }

    filterbar.addEventListener('click', function (e) {
      var btn = e.target.closest('.fbtn');
      if (!btn) return;
      var group = btn.getAttribute('data-group');
      state[group] = btn.getAttribute('data-value');
      filterbar.querySelectorAll('.fbtn[data-group="' + group + '"]').forEach(function (b) {
        b.setAttribute('aria-pressed', b === btn ? 'true' : 'false');
      });
      apply();
    });

    /* allow deep-links like /products/?width=34&power=manual */
    var params = new URLSearchParams(location.search);
    ['width', 'power'].forEach(function (g) {
      var v = params.get(g);
      if (!v) return;
      var btn = filterbar.querySelector('.fbtn[data-group="' + g + '"][data-value="' + v + '"]');
      if (btn) btn.click();
    });
    apply();
  }

  /* ---------- Quote / distributor forms ----------
     Static-hosting friendly: builds a pre-filled email in the visitor's
     mail client. Swap for a Cloudflare Pages Function when ready — see
     README.md for the drop-in endpoint. ---------- */
  document.querySelectorAll('form[data-mailto]').forEach(function (form) {
    /* pre-select product from ?product= */
    var params = new URLSearchParams(location.search);
    var pre = params.get('product');
    var select = form.querySelector('select[name="product"]');
    if (pre && select) {
      Array.prototype.forEach.call(select.options, function (o) {
        if (o.value.toLowerCase() === pre.toLowerCase()) select.value = o.value;
      });
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var to = form.getAttribute('data-mailto');
      var subjectBase = form.getAttribute('data-subject') || 'Website inquiry';
      var lines = [];
      var subjectExtra = '';
      Array.prototype.forEach.call(form.elements, function (el) {
        if (!el.name || el.type === 'submit') return;
        var label = el.getAttribute('data-label') || el.name;
        if (el.value) lines.push(label + ': ' + el.value);
        if (el.name === 'product' && el.value) subjectExtra = ' — ' + el.value;
      });
      lines.push('', 'Sent from zrtool.com');
      var href = 'mailto:' + to +
        '?subject=' + encodeURIComponent(subjectBase + subjectExtra) +
        '&body=' + encodeURIComponent(lines.join('\n'));
      var status = form.querySelector('.form-status');
      if (status) {
        status.textContent = 'Opening your email client… If nothing happens, email us directly at ' + to + '.';
        status.classList.add('show');
      }
      window.location.href = href;
    });
  });
})();
