/* ============================================================
   ИНКАР-1 — интерактив и анимации
   ============================================================ */
(function () {
  'use strict';

  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------- 0. Стиль и видео-слоты */

  // Общий стилевой хвост — подставляется в КАЖДЫЙ промпт при генерации кадров.
  var STYLE_TAIL =
    'Стиль: тяжёлая индустриальная кинематография, фотореализм. Тёмная база — графит, ' +
    'вороненая сталь, бетон. Холодные сине-стальные акценты как доминанта, раскалённый металл ' +
    'только там, где он есть по сюжету. Один направленный источник света, глубокие тени, ' +
    'объёмный свет в дыму и пыли. Оптика 35–85 мм, малая ГРИП на предметных кадрах. ' +
    'Лёгкое зерно, без HDR-пересветов, без глянца, без читаемых логотипов и брендов.';

  // Слоты, которые должны быть ВИДЕО (первый экран и полосы во всю ширину).
  var VIDEO_SLOTS = [
    'HERO-01', 'BAND-01', 'CTA-01', 'ABOUT-BAND', 'GAL-HERO',
    'PROD-HERO', 'PROD-BAND', 'SERV-HERO', 'SERV-BAND',
    'MET-HERO', 'MET-BAND', 'TUBE-HERO', 'TUBE-BAND',
    'CUST-HERO', 'CUST-BAND', 'EN-HERO', 'EN-BAND',
    'GOK-HERO', 'GOK-BAND'
  ];

  /* ---------------------------------------------------- 1. Медиа-слоты
     <figure class="media" data-slot="HERO-01" data-src="" data-kind="image|video" ...>
     Если data-src пустой — рисуем пустышку с описанием будущего кадра.
     Как появятся ИИ-кадры: просто проставить data-src="assets/img/hero-01.jpg". */
  function hydrateMedia() {
    $$('.media').forEach(function (el) {
      if (el.dataset.ready) return;
      // контейнеры-обёртки (без слота и без картинки) пропускаем
      if (!el.getAttribute('data-slot') && !el.getAttribute('data-src')) return;
      el.dataset.ready = '1';
      var src  = (el.getAttribute('data-src') || '').trim();
      var slotName = el.getAttribute('data-slot') || '';
      var kind = VIDEO_SLOTS.indexOf(slotName) > -1
        ? 'video'
        : (el.getAttribute('data-kind') || 'image');
      el.setAttribute('data-kind', kind);
      var alt  = el.getAttribute('data-alt') || el.getAttribute('data-desc') || '';

      if (src) {
        if (kind === 'video') {
          var v = document.createElement('video');
          v.src = src; v.muted = true; v.loop = true; v.playsInline = true;
          v.autoplay = true;
          // видео первого экрана грузим сразу — от него зависит занавес
          v.setAttribute('preload', el.closest('.hero') ? 'auto' : 'metadata');
          if (el.getAttribute('data-poster')) v.poster = el.getAttribute('data-poster');
          el.appendChild(v);
        } else {
          var i = document.createElement('img');
          i.src = src; i.alt = alt; i.loading = 'lazy'; i.decoding = 'async';
          el.appendChild(i);
        }
        return;
      }

      var slot  = el.getAttribute('data-slot') || 'SLOT';
      var ratio = el.getAttribute('data-ratio') || '—';
      var desc  = el.getAttribute('data-desc') || 'Кадр в общем киношном стиле.';
      // полный промпт = описание кадра + общий стилевой хвост
      el.setAttribute('data-prompt', desc + ' ' + STYLE_TAIL);
      var ph = document.createElement('div');
      ph.className = 'ph';
      ph.innerHTML =
        '<i class="ph__crop ph__crop--tl"></i><i class="ph__crop ph__crop--tr"></i>' +
        '<i class="ph__crop ph__crop--bl"></i><i class="ph__crop ph__crop--br"></i>' +
        '<div class="ph__top"><span><span class="ph__id">' + slot + '</span>' +
        '<span class="ph__kind' + (kind === 'video' ? ' ph__kind--video' : '') + '">' +
        (kind === 'video' ? 'видео' : 'фото') + '</span></span>' +
        '<span class="ph__meta">' + ratio + '</span></div>' +
        '<div class="ph__bot"><div><p class="ph__desc">' + desc + '</p>' +
        '<p class="ph__style">+ ' + STYLE_TAIL + '</p></div></div>';
      el.appendChild(ph);
    });
  }

  /* ---------------------------------------------------- 2. Занавес / переходы
     Створки расходятся не сразу, а когда медиа первого экрана готово
     (или по таймауту, чтобы не держать зрителя, если сеть медленная). */
  var MIN_HOLD = 700;      // минимум, чтобы занавес не мигал
  var MAX_HOLD = 3500;     // максимум ожидания медиа

  function curtain() {
    var c = $('.curtain');
    if (!c) return;
    var t0 = Date.now(), opened = false;

    function open() {
      if (opened) return;
      opened = true;
      var wait = Math.max(0, MIN_HOLD - (Date.now() - t0));
      setTimeout(function () { c.classList.add('is-up'); }, reduced ? 0 : wait);
    }

    if (reduced) { open(); }
    else {
      setTimeout(open, MAX_HOLD);
      var hero = $('.hero__bg .media, .hero .media');
      var el = hero && hero.querySelector('video, img');
      if (!el) {
        setTimeout(open, 250);
      } else if (el.tagName === 'VIDEO') {
        if (el.readyState >= 3) open();
        else {
          el.addEventListener('canplay', open, { once: true });
          el.addEventListener('loadeddata', open, { once: true });
          el.addEventListener('error', open, { once: true });
        }
      } else {
        if (el.complete) open();
        else {
          el.addEventListener('load', open, { once: true });
          el.addEventListener('error', open, { once: true });
        }
      }
      window.addEventListener('load', function () { setTimeout(open, 150); });
    }
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a');
      if (!a || reduced) return;
      var href = a.getAttribute('href') || '';
      if (!href || href.charAt(0) === '#' || a.target === '_blank' ||
          /^(mailto:|tel:|http)/.test(href) || a.hasAttribute('data-nocurtain')) return;
      e.preventDefault();
      c.classList.remove('is-up');
      setTimeout(function () { window.location.href = href; }, 520);
    });
    window.addEventListener('pageshow', function (e) { if (e.persisted) c.classList.add('is-up'); });
  }

  /* ---------------------------------------------------- 3. Шапка */
  function header() {
    var hdr = $('.hdr');
    if (!hdr) return;
    var last = 0;
    window.addEventListener('scroll', function () {
      var y = window.scrollY;
      if (y > 260 && y > last) hdr.classList.add('is-hidden');
      else hdr.classList.remove('is-hidden');
      last = y;
    }, { passive: true });

    // выпадающие меню
    $$('.nav__item').forEach(function (it) {
      if (!$('.drop', it)) return;
      var t;
      it.addEventListener('mouseenter', function () { clearTimeout(t); it.classList.add('is-open'); });
      it.addEventListener('mouseleave', function () { t = setTimeout(function () { it.classList.remove('is-open'); }, 140); });
      var lnk = $('.nav__link', it);
      lnk.addEventListener('click', function (e) {
        if (lnk.getAttribute('href') === '#') { e.preventDefault(); it.classList.toggle('is-open'); }
      });
    });

    // мобильное меню
    var b = $('.burger'), m = $('.mmenu');
    if (b && m) {
      b.addEventListener('click', function () {
        var on = m.classList.toggle('is-open');
        b.classList.toggle('is-on', on);
        document.body.classList.toggle('is-locked', on);
      });
    }
  }

  /* ---------------------------------------------------- 4. Появление при скролле */
  function reveals() {
    // разбить заголовок на строки-маски
    $$('[data-split]').forEach(function (el) {
      if (el.dataset.splitted) return;
      el.dataset.splitted = '1';
      var html = el.innerHTML.split(/<br\s*\/?>/i);
      el.innerHTML = html.map(function (part) {
        return '<span class="line-mask"><span>' + part + '</span></span>';
      }).join('');
      if (!el.hasAttribute('data-reveal')) el.setAttribute('data-reveal', '');
    });

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('is-in');
        io.unobserve(en.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

    $$('[data-reveal]').forEach(function (el, i) {
      el.style.transitionDelay = (parseFloat(el.getAttribute('data-delay') || 0) || 0) + 's';
      io.observe(el);
    });

    $$('[data-stagger]').forEach(function (wrap) {
      Array.prototype.forEach.call(wrap.children, function (ch, i) {
        ch.style.transitionDelay = (i * 0.075) + 's';
      });
      io.observe(wrap);
    });
  }

  /* ---------------------------------------------------- 5. Параллакс */
  function parallax() {
    if (reduced) return;
    var items = $$('.parallax');
    if (!items.length) return;
    var tick = false;
    function upd() {
      var vh = window.innerHeight;
      items.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) return;
        var p = (r.top + r.height / 2 - vh / 2) / vh;      // -1..1
        var k = parseFloat(el.getAttribute('data-speed') || 0.12);
        el.style.transform = 'translate3d(0,' + (-p * k * 100).toFixed(2) + 'px,0) scale(1.08)';
      });
      tick = false;
    }
    window.addEventListener('scroll', function () {
      if (!tick) { tick = true; requestAnimationFrame(upd); }
    }, { passive: true });
    upd();
  }

  /* ---------------------------------------------------- 6. Счётчики */
  function counters() {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        io.unobserve(el);
        var to = parseFloat(el.getAttribute('data-count'));
        var suf = el.getAttribute('data-suffix') || '';
        var pre = el.getAttribute('data-prefix') || '';
        var dec = parseInt(el.getAttribute('data-dec') || 0, 10);
        if (reduced) { el.textContent = pre + to.toFixed(dec) + suf; return; }
        var t0 = null, dur = 1500;
        function step(ts) {
          if (!t0) t0 = ts;
          var p = Math.min((ts - t0) / dur, 1);
          var e = 1 - Math.pow(1 - p, 3);
          el.textContent = pre + (to * e).toFixed(dec).replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + suf;
          if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.5 });
    $$('[data-count]').forEach(function (el) { io.observe(el); });

    // шкала казсодержания
    var g = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return;
        g.unobserve(en.target);
        en.target.style.width = en.target.getAttribute('data-w') + '%';
      });
    }, { threshold: 0.4 });
    $$('.gauge__fill').forEach(function (el) { g.observe(el); });
  }

  /* ---------------------------------------------------- 7. Горизонтальный пин */
  function pinned() {
    if (window.innerWidth < 900 || reduced) return;
    $$('.pin').forEach(function (pin) {
      var track = $('.pin__track', pin);
      if (!track) return;
      function size() {
        var dist = Math.max(0, track.scrollWidth - window.innerWidth + 120);
        pin.style.height = (window.innerHeight + dist) + 'px';
        pin.dataset.dist = dist;
      }
      size();
      window.addEventListener('resize', size);
      window.addEventListener('scroll', function () {
        var r = pin.getBoundingClientRect();
        var dist = parseFloat(pin.dataset.dist || 0);
        var p = Math.min(Math.max(-r.top / (pin.offsetHeight - window.innerHeight), 0), 1);
        track.style.transform = 'translate3d(' + (-p * dist) + 'px,0,0)';
      }, { passive: true });
    });
  }

  /* ---------------------------------------------------- 7b. Цифры в заголовках
     В Shoptronic цифры выпадают, поэтому подменяем их моноширинным. */
  var DIGIT_SEL = '.h-display,.h1,.h2,.h3,.h4,.card__title,.dircard__t,' +
                  '.regcard__t,.newsrow__t,.feat__t,.ftr__big,.quote__t,.lead';
  function digits() {
    $$(DIGIT_SEL).forEach(function (el) {
      if (el.dataset.numed) return;
      el.dataset.numed = '1';
      var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
      var nodes = [], n;
      while ((n = walker.nextNode())) if (/\d/.test(n.nodeValue)) nodes.push(n);
      nodes.forEach(function (node) {
        var frag = document.createDocumentFragment();
        node.nodeValue.split(/(\d+(?:[.,]\d+)?)/).forEach(function (part, i) {
          if (!part) return;
          if (i % 2) {
            var s = document.createElement('span');
            s.className = 'num'; s.textContent = part;
            frag.appendChild(s);
          } else {
            frag.appendChild(document.createTextNode(part));
          }
        });
        node.parentNode.replaceChild(frag, node);
      });
    });
  }

  /* ---------------------------------------------------- 7c. Шаги, листаемые скроллом */
  function scrollSteps() {
    $$('.sscroll').forEach(function (sec) {
      var items = $$('.steps__nav li', sec);
      var panes = $$('.steps__pane', sec);
      var prog  = $('.steps__prog i', sec);
      var n = panes.length;
      if (!n) return;

      if (window.innerWidth < 900 || reduced) { sec.style.height = 'auto'; return; }

      function size() { sec.style.height = Math.round(window.innerHeight * (1 + (n - 1) * 0.8)) + 'px'; }
      size();
      window.addEventListener('resize', size);

      var cur = -1;
      function set(i) {
        if (i === cur) return;
        cur = i;
        items.forEach(function (li, k) { li.classList.toggle('is-on', k === i); });
        panes.forEach(function (p, k) { p.classList.toggle('is-on', k === i); });
      }
      function upd() {
        var total = sec.offsetHeight - window.innerHeight;
        if (total <= 0) return;
        var p = Math.min(Math.max(-sec.getBoundingClientRect().top / total, 0), 1);
        set(Math.min(n - 1, Math.floor(p * n * 0.999)));
        if (prog) prog.style.width = (p * 100).toFixed(1) + '%';
      }
      window.addEventListener('scroll', upd, { passive: true });
      upd();

      // клик по пункту — доскроллить до его отрезка
      items.forEach(function (li, i) {
        var b = $('.steps__btn', li);
        if (!b) return;
        b.addEventListener('click', function () {
          var total = sec.offsetHeight - window.innerHeight;
          var y = sec.offsetTop + total * ((i + 0.35) / n);
          window.scrollTo({ top: y, behavior: 'smooth' });
        });
      });
    });
  }

  /* ---------------------------------------------------- 8. Шаги / табы */
  function steps() {
    $$('.steps').forEach(function (box) {
      if (box.closest('.sscroll')) return;   // там переключение идёт скроллом
      var btns  = $$('.steps__btn', box);
      var panes = $$('.steps__pane', box);
      btns.forEach(function (b, i) {
        b.addEventListener('click', function () {
          btns.forEach(function (x) { x.parentNode.classList.remove('is-on'); });
          panes.forEach(function (x) { x.classList.remove('is-on'); });
          b.parentNode.classList.add('is-on');
          if (panes[i]) panes[i].classList.add('is-on');
        });
      });
    });
  }

  /* ---------------------------------------------------- 9. Полоса прогресса */
  function pbar() {
    var b = $('.pbar');
    if (!b) return;
    window.addEventListener('scroll', function () {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      b.style.width = (h > 0 ? (window.scrollY / h) * 100 : 0) + '%';
    }, { passive: true });
  }

  /* ---------------------------------------------------- 10. Реестр изделий */
  var REG = [];
  function registry() {
    var grid = $('#reg-grid');
    if (!grid) return;

    fetch('assets/registry.json')
      .then(function (r) { return r.json(); })
      .then(function (data) { REG = data; buildFilters(); render(); })
      .catch(function () { grid.innerHTML = '<div class="reg-empty">Не удалось загрузить реестр</div>'; });

    function uniq(key) {
      var s = [];
      REG.forEach(function (i) { if (i[key] && s.indexOf(i[key]) < 0) s.push(i[key]); });
      return s.sort(function (a, b) { return a.localeCompare(b, 'ru'); });
    }
    function fill(sel, key, label) {
      var el = $(sel);
      if (!el) return;
      el.innerHTML = '<option value="">' + label + '</option>' +
        uniq(key).map(function (v) { return '<option value="' + v + '">' + v + '</option>'; }).join('');
    }
    function buildFilters() {
      fill('#f-branch',   'branch',   'Все отрасли');
      fill('#f-node',     'node',     'Все узлы');
      fill('#f-material', 'material', 'Все материалы');
      fill('#f-size',     'size',     'Любой габарит');
      ['#f-branch', '#f-node', '#f-material', '#f-size'].forEach(function (s) {
        var el = $(s); if (el) el.addEventListener('change', render);
      });
      var q = $('#f-q'); if (q) q.addEventListener('input', render);
      var rst = $('#f-reset');
      if (rst) rst.addEventListener('click', function () {
        ['#f-branch', '#f-node', '#f-material', '#f-size', '#f-q'].forEach(function (s) {
          var el = $(s); if (el) el.value = '';
        });
        render();
      });
    }
    function val(s) { var el = $(s); return el ? el.value : ''; }
    function render() {
      var b = val('#f-branch'), n = val('#f-node'), m = val('#f-material'),
          z = val('#f-size'), q = val('#f-q').toLowerCase().trim();
      var out = REG.filter(function (i) {
        if (b && i.branch !== b) return false;
        if (n && i.node !== n) return false;
        if (m && i.material !== m) return false;
        if (z && i.size !== z) return false;
        if (q && (i.title + ' ' + i.sku + ' ' + i.material + ' ' + (i.tags || []).join(' ')).toLowerCase().indexOf(q) < 0) return false;
        return true;
      });
      var cnt = $('#reg-count');
      if (cnt) cnt.textContent = out.length + ' поз. из ' + REG.length;
      if (!out.length) { grid.innerHTML = '<div class="reg-empty">Ничего не найдено — снимите часть фильтров</div>'; return; }
      grid.innerHTML = out.map(card).join('');
      hydrateMedia();
      $$('.js-open', grid).forEach(function (btn) {
        btn.addEventListener('click', function () { openItem(btn.getAttribute('data-sku')); });
      });
    }
    function card(i) {
      return '' +
      '<article class="regcard">' +
        '<div class="regcard__top">' +
          '<span class="regcard__sku">' + i.sku + '</span>' +
          '<figure class="media media--r43" data-slot="' + i.slotPhoto + '" data-ratio="4:3" data-desc="' + esc(i.photoDesc) + '"></figure>' +
          '<figure class="media media--r43" data-slot="' + i.slotDraw + '" data-ratio="4:3" data-desc="' + esc(i.drawDesc) + '"></figure>' +
        '</div>' +
        '<div class="regcard__b">' +
          '<h3 class="regcard__t">' + i.title + '</h3>' +
          '<ul class="regcard__specs">' +
            row('Отрасль', i.branch) + row('Узел', i.node) + row('Материал', i.material) +
            row('Термообработка', i.heat) + row('Габарит', i.dims) + row('Срок', i.lead) +
          '</ul>' +
          '<div class="regcard__f">' +
            '<button class="btn btn--ghost js-open" data-sku="' + i.sku + '">Паспорт</button>' +
            '<a class="btn btn--solid" href="request.html?sku=' + encodeURIComponent(i.sku) + '">Заказать повтор</a>' +
          '</div>' +
        '</div>' +
      '</article>';
    }
    function row(k, v) { return v ? '<li><span>' + k + '</span><span>' + v + '</span></li>' : ''; }

    function openItem(sku) {
      var i = REG.filter(function (x) { return x.sku === sku; })[0];
      if (!i) return;
      var mw = $('#modal-w');
      mw.innerHTML =
        '<button class="modal__x" aria-label="Закрыть">&times;</button>' +
        '<figure class="media media--r219" data-slot="' + i.slotPhoto + '" data-ratio="21:9" data-desc="' + esc(i.photoDesc) + '"></figure>' +
        '<div style="padding:clamp(22px,3vw,44px)">' +
          '<p class="eyebrow">' + i.sku + ' · ' + i.branch + '</p>' +
          '<h2 class="h2" style="margin-bottom:18px">' + i.title + '</h2>' +
          '<p class="body measure" style="margin-bottom:26px">' + i.about + '</p>' +
          '<ul class="speclist">' +
            li('Отрасль', i.branch) + li('Узел / система', i.node) + li('Материал', i.material) +
            li('Термообработка', i.heat) + li('Габарит', i.dims) + li('Класс точности', i.tol) +
            li('Контроль', i.qc) + li('Срок изготовления', i.lead) + li('Заказчик', i.client) +
          '</ul>' +
          '<div class="u-flex u-gap u-wrap u-mt">' +
            '<a class="btn btn--solid" href="request.html?sku=' + encodeURIComponent(i.sku) + '">Заказать повтор</a>' +
            '<a class="btn btn--ghost" href="request.html">Прислать свой чертёж</a>' +
          '</div>' +
        '</div>';
      $('#modal').classList.add('is-open');
      document.body.classList.add('is-locked');
      hydrateMedia();
      $('.modal__x', mw).addEventListener('click', closeModal);
    }
    function li(k, v) { return v ? '<li><span class="k">' + k + '</span><span class="v">' + v + '</span></li>' : ''; }
  }
  function closeModal() {
    var m = $('#modal');
    if (!m) return;
    m.classList.remove('is-open');
    document.body.classList.remove('is-locked');
  }
  function modalInit() {
    var m = $('#modal');
    if (!m) return;
    $('.modal__bd', m).addEventListener('click', closeModal);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeModal(); });
  }
  function esc(s) { return String(s || '').replace(/"/g, '&quot;'); }

  /* ---------------------------------------------------- 11. Форма заявки + чертёж */
  function requestForm() {
    var form = $('#req-form');
    if (!form) return;

    var zone = $('#dz'), input = $('#dz-input'), list = $('#dz-list');
    var OK = ['pdf', 'dwg', 'dxf', 'step', 'stp', 'igs', 'iges', 'sldprt', 'x_t', 'zip', 'rar', 'jpg', 'jpeg', 'png'];
    var files = [];

    // подставить SKU из ?sku=
    var sku = new URLSearchParams(location.search).get('sku');
    if (sku && $('#f-msg')) $('#f-msg').value = 'Повтор позиции ' + sku + '. Количество: ';

    function human(b) {
      if (b < 1024) return b + ' Б';
      if (b < 1048576) return (b / 1024).toFixed(0) + ' КБ';
      return (b / 1048576).toFixed(1) + ' МБ';
    }
    function paint() {
      list.innerHTML = files.map(function (f, i) {
        var ext = (f.name.split('.').pop() || '?').toLowerCase();
        return '<li><span class="ext">' + ext + '</span><span>' + f.name + '</span>' +
               '<span class="sz">' + human(f.size) + '</span>' +
               '<button type="button" class="rm" data-i="' + i + '" aria-label="Убрать">&times;</button></li>';
      }).join('');
      $$('.rm', list).forEach(function (b) {
        b.addEventListener('click', function () { files.splice(+b.getAttribute('data-i'), 1); paint(); });
      });
    }
    function add(fl) {
      Array.prototype.forEach.call(fl, function (f) {
        var ext = (f.name.split('.').pop() || '').toLowerCase();
        if (OK.indexOf(ext) < 0) { alert('Формат .' + ext + ' не поддерживается.\nПринимаем: ' + OK.join(', ')); return; }
        if (f.size > 60 * 1024 * 1024) { alert('Файл ' + f.name + ' больше 60 МБ — пришлите ссылкой.'); return; }
        files.push(f);
      });
      paint();
    }
    zone.addEventListener('click', function () { input.click(); });
    input.addEventListener('change', function () { add(input.files); input.value = ''; });
    ['dragenter', 'dragover'].forEach(function (ev) {
      zone.addEventListener(ev, function (e) { e.preventDefault(); zone.classList.add('is-over'); });
    });
    ['dragleave', 'drop'].forEach(function (ev) {
      zone.addEventListener(ev, function (e) { e.preventDefault(); zone.classList.remove('is-over'); });
    });
    zone.addEventListener('drop', function (e) { if (e.dataTransfer) add(e.dataTransfer.files); });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var bad = false;
      $$('[data-required]', form).forEach(function (el) {
        var f = el.closest('.field');
        var empty = !el.value.trim();
        var mail = el.type === 'email' && el.value && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(el.value);
        f.classList.toggle('is-bad', empty || mail);
        if (empty || mail) bad = true;
      });
      if (bad) { form.querySelector('.is-bad .inp, .is-bad .ta, .is-bad .sel').focus(); return; }

      var d = new Date();
      var num = 'INK-' + d.getFullYear() +
                String(d.getMonth() + 1).padStart(2, '0') +
                String(d.getDate()).padStart(2, '0') + '-' +
                String(Math.floor(Math.random() * 900) + 100);
      $('#ok-num').textContent = num;
      $('#ok-files').textContent = files.length
        ? 'Принято файлов: ' + files.length + ' (' + files.map(function (f) { return f.name; }).join(', ') + ')'
        : 'Файлы не приложены — пришлём опросный лист вместе с подтверждением.';
      form.classList.add('u-hide');
      $('#ok-box').classList.add('is-on');
      $('#ok-box').scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'center' });
    });

    $$('[data-required]', form).forEach(function (el) {
      el.addEventListener('input', function () { el.closest('.field').classList.remove('is-bad'); });
    });
  }

  /* ---------------------------------------------------- 12. Год в подвале */
  function misc() {
    $$('.js-year').forEach(function (el) { el.textContent = new Date().getFullYear(); });
  }

  /* ---------------------------------------------------- запуск */
  function init() {
    hydrateMedia(); curtain(); header(); reveals(); digits(); parallax();
    counters(); pinned(); scrollSteps(); steps(); pbar(); registry(); modalInit();
    requestForm(); misc();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
