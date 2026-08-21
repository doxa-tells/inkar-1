# -*- coding: utf-8 -*-
"""Общий каркас: шапка, подвал, медиа-слоты, сборка страницы."""

import html, json, os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "inkar")

# все медиа-слоты собираем сюда -> потом в MEDIA-BRIEF.md и media-manifest.json
MEDIA = []
_CUR_PAGE = {"slug": "", "title": ""}

RATIOS = {
    "16:9": "media--r169", "4:3": "media--r43", "1:1": "media--r11",
    "4:5": "media--r45", "3:4": "media--r34", "21:9": "media--r219",
    "3:2": "media--r32", "fill": "media--fill", "tall": "media--tall",
}

PHONE = "+7 (7213) 44-77-99"
PHONE_HREF = "+77213447799"
MAIL = "inkar-1@yandex.kz"
ADDR = "101406, Республика Казахстан, Карагандинская область,<br>г. Темиртау, ул. Мичурина, строение 32Е"

ACCENT = "#2f6fd0"          # фирменный синий

LOGO_FILE = "assets/img/logo.png"

def logo(cls="brand__logo"):
    return f'<img class="{cls}" src="{LOGO_FILE}" alt="ТОО «ИНКАР-1»" width="700" height="288">'

LOGO_SVG = logo()           # совместимость со старыми вызовами

# Общий стилевой хвост — добавляется в КАЖДЫЙ промпт.
STYLE_TAIL = (
    "Стиль: тяжёлая индустриальная кинематография, фотореализм. Тёмная база — графит, "
    "вороненая сталь, бетон. Холодные сине-стальные акценты как доминанта, раскалённый металл "
    "только там, где он есть по сюжету. Один направленный источник света, глубокие тени, "
    "объёмный свет в дыму и пыли. Оптика 35–85 мм, малая ГРИП на предметных кадрах. "
    "Лёгкое зерно, без HDR-пересветов, без глянца, без читаемых логотипов и брендов."
)

# Слоты, которые должны быть видео (первый экран и полосы во всю ширину).
VIDEO_SLOTS = {
    "HERO-01", "BAND-01", "CTA-01", "ABOUT-BAND", "GAL-HERO",
    "PROD-HERO", "PROD-BAND", "SERV-HERO", "SERV-BAND",
    "MET-HERO", "MET-BAND", "TUBE-HERO", "TUBE-BAND",
    "CUST-HERO", "CUST-BAND", "EN-HERO", "EN-BAND",
    "GOK-HERO", "GOK-BAND",
}

# ---------------------------------------------------------------- медиа
IMG_DIR = os.path.join(OUT, "assets", "img")

def _find_src(slot, kind):
    """Ищет готовый файл кадра в assets/img по имени слота."""
    exts = (".mp4", ".webm") if kind == "video" else (".jpg", ".jpeg", ".webp", ".png")
    for ext in exts:
        if os.path.exists(os.path.join(IMG_DIR, slot + ext)):
            return "assets/img/" + slot + ext
    return ""

def _find_poster(slot):
    for name in (slot + "-poster.jpg", slot + "-poster.png", slot + ".jpg"):
        if os.path.exists(os.path.join(IMG_DIR, name)):
            return "assets/img/" + name
    return ""

def media(slot, ratio="16:9", desc="", kind="image", cls="", attrs=""):
    """Слот под кадр. Если файл уже лежит в assets/img — подставляется автоматически."""
    if slot in VIDEO_SLOTS:
        kind = "video"
    src = _find_src(slot, kind)
    MEDIA.append({
        "slot": slot, "page": _CUR_PAGE["slug"], "page_title": _CUR_PAGE["title"],
        "ratio": ratio, "kind": kind, "desc": desc, "src": src,
        "prompt": desc.strip() + " " + STYLE_TAIL,
    })
    rc = RATIOS.get(ratio, "media--r169")
    poster = ""
    if kind == "video" and src:
        p = _find_poster(slot)
        if p:
            poster = f' data-poster="{p}"'
    return (f'<figure class="media {rc} {cls}" data-slot="{slot}" data-ratio="{ratio}" '
            f'data-kind="{kind}" data-src="{src}"{poster} '
            f'data-desc="{html.escape(desc, quote=True)}" {attrs}></figure>')

def scrim(kind="b"):
    return f'<div class="scrim scrim--{kind}"></div>'

# ---------------------------------------------------------------- навигация
PROD = [
    ("proizvodstvo-metallurgiya.html", "Для металлургического производства"),
    ("proizvodstvo-truba.html", "Для трубоэлектросварочного производства"),
    ("proizvodstvo-nestandart.html", "Нестандартное оборудование"),
    ("proizvodstvo-energetika.html", "Для энергетического сектора"),
    ("proizvodstvo-gok.html", "Для горно-обогатительного производства"),
]
SERV = [
    ("usluga-rezka.html", "Газоплазменная резка металла"),
    ("usluga-proektirovanie.html", "Разработка и проектирование"),
    ("usluga-svarka.html", "Сварочные работы"),
    ("usluga-tokarnaya.html", "Токарная обработка"),
    ("usluga-frezernaya.html", "Фрезерная обработка"),
    ("usluga-shlifovanie.html", "Шлифование металла"),
    ("usluga-sverlenie.html", "Сверление"),
]
COMP = [
    ("o-kompanii.html", "О компании"),
    ("sertifikaty.html", "Сертификаты и награды"),
    ("otzyvy.html", "Отзывы"),
    ("fotogalereya.html", "Фотогалерея"),
    ("novosti.html", "Новости"),
    ("kontakty.html", "Контакты"),
]

CARET = ('<svg class="nav__caret" viewBox="0 0 12 12" fill="none">'
         '<path d="M2 4.5 6 8.5l4-4" stroke="currentColor" stroke-width="1.5"/></svg>')
ARW = ('<svg class="btn__arw" width="13" height="9" viewBox="0 0 13 9" fill="none">'
       '<path d="M8.5 1 12 4.5 8.5 8M12 4.5H0" stroke="currentColor" stroke-width="1.3"/></svg>')

def _drop(items, title=None):
    h = '<div class="drop">'
    if title:
        h += f'<div class="drop__grp">{title}</div>'
    for href, label in items:
        h += f'<a href="{href}">{label}</a>'
    h += "</div>"
    return h

def header(active=""):
    def cl(key):
        return " is-active" if active == key else ""
    return f"""
<div class="curtain">
  <i class="curtain__p curtain__p--t"></i><i class="curtain__p curtain__p--b"></i>
  <div class="curtain__c">{logo("curtain__logo")}<span class="curtain__bar"><i></i></span></div>
</div>
<div class="pbar"></div>
<header class="hdr">
  <div class="hdr__in">
    <a class="brand" href="index.html" aria-label="ИНКАР-1 — на главную">
      {logo()}
      <span class="brand__txt"><span class="brand__sub">Машиностроение</span>
      <span class="brand__sub">Темиртау · с 1998</span></span>
    </a>
    <nav class="nav">
      <div class="nav__item"><a class="nav__link{cl('prod')}" href="proizvodstvo.html">Производство {CARET}</a>
        {_drop(PROD + [("proizvodstvo.html", "Все направления →")], "Направления")}</div>
      <div class="nav__item"><a class="nav__link{cl('serv')}" href="uslugi.html">Услуги {CARET}</a>
        {_drop(SERV + [("uslugi.html", "Все услуги →")], "Технологии")}</div>
      <div class="nav__item"><a class="nav__link{cl('reg')}" href="reestr.html">Реестр изделий</a></div>
      <div class="nav__item"><a class="nav__link{cl('tender')}" href="tendery.html">Тендеры</a></div>
      <div class="nav__item"><a class="nav__link{cl('comp')}" href="o-kompanii.html">Компания {CARET}</a>
        {_drop(COMP)}</div>
    </nav>
    <div class="hdr__cta">
      <a class="btn btn--solid" href="request.html">Прислать чертёж {ARW}</a>
      <button class="burger" aria-label="Меню"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="mmenu">
  {logo("mmenu__logo")}
  <div class="mmenu__grp"><a href="index.html">Главная</a></div>
  <div class="mmenu__grp"><p class="mono">Производство</p>
    <a href="proizvodstvo.html">Все направления</a>
    <div class="mmenu__sub">{''.join(f'<a href="{h}">{t}</a>' for h, t in PROD)}</div></div>
  <div class="mmenu__grp"><p class="mono">Услуги</p>
    <a href="uslugi.html">Все услуги</a>
    <div class="mmenu__sub">{''.join(f'<a href="{h}">{t}</a>' for h, t in SERV)}</div></div>
  <div class="mmenu__grp"><a href="reestr.html">Реестр изделий</a><a href="tendery.html">Тендеры и закупки</a>
    <a href="request.html">Прислать чертёж</a></div>
  <div class="mmenu__grp"><p class="mono">Компания</p>
    <div class="mmenu__sub">{''.join(f'<a href="{h}">{t}</a>' for h, t in COMP)}</div></div>
  <div class="mmenu__grp"><a href="tel:{PHONE_HREF}">{PHONE}</a><a href="mailto:{MAIL}">{MAIL}</a></div>
</div>"""

# ---------------------------------------------------------------- CTA + подвал
def cta(slot="CTA-01",
        desc="Ночная съёмка цеха с высокой точки: длинный пролёт, мостовой кран, редкие искры сварки, глубокие тени, холодный свет ртутных ламп с тёплыми акцентами от металла.",
        title="Пришлите чертёж —<br>ответим за один рабочий день",
        text="Принимаем PDF, DWG, DXF, STEP. Если чертежа нет — пришлём опросный лист и поможем оформить задачу."):
    return f"""
<section class="cta">
  <div class="cta__bg">{media(slot, "fill", desc)}{scrim("all")}</div>
  <div class="container cta__in">
    <p class="eyebrow eyebrow--plain" data-reveal>Начнём работу</p>
    <h2 class="h1 measure" data-split>{title}</h2>
    <p class="lead measure-sm" data-reveal data-delay=".1">{text}</p>
    <div class="u-flex u-gap u-wrap" data-reveal data-delay=".2" style="justify-content:center">
      <a class="btn btn--solid btn--lg" href="request.html">Прислать чертёж {ARW}</a>
      <a class="btn btn--ghost btn--lg" href="tel:{PHONE_HREF}">{PHONE}</a>
    </div>
  </div>
</section>"""

def footer():
    return f"""
<footer class="ftr">
  <div class="container">
    <div class="ftr__top">
      <div>
        <a class="brand brand--ftr" href="index.html">{logo("ftr__logo")}</a>
        <p class="small" style="margin:20px 0 0;max-width:34ch">Машиностроительное и металлообрабатывающее
          предприятие полного цикла. Темиртау, Карагандинская область. Работаем с 1998 года.</p>
      </div>
      <div><h4>Производство</h4><ul>{''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in PROD)}</ul></div>
      <div><h4>Услуги</h4><ul>{''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in SERV[:5])}
        <li><a href="uslugi.html">Все услуги →</a></li></ul></div>
      <div><h4>Компания</h4><ul>{''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in COMP)}
        <li><a href="reestr.html">Реестр изделий</a></li><li><a href="tendery.html">Тендеры и закупки</a></li></ul>
        <h4 style="margin-top:26px">Контакты</h4>
        <ul><li><a href="tel:{PHONE_HREF}">{PHONE}</a></li><li><a href="mailto:{MAIL}">{MAIL}</a></li></ul>
      </div>
    </div>
    <p class="ftr__big">ИНКАР-1</p>
    <div class="ftr__bot">
      <span>© <span class="js-year">2026</span> ТОО «Инкар-1». Все права защищены</span>
      <span>БИН 980940000441 · Темиртау, ул. Мичурина, 32Е</span>
      <span>Демо-версия сайта</span>
    </div>
  </div>
</footer>"""

# ---------------------------------------------------------------- страница
TPL = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" href="assets/fonts/shoptronic.woff2" as="font" type="font/woff2" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700&family=Roboto+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
<link rel="icon" type="image/png" sizes="32x32" href="assets/img/favicon-32.png">
<link rel="icon" type="image/png" sizes="64x64" href="assets/img/favicon-64.png">
<link rel="icon" type="image/png" sizes="192x192" href="assets/img/favicon-192.png">
<link rel="icon" type="image/png" sizes="512x512" href="assets/img/favicon-512.png">
<link rel="apple-touch-icon" sizes="180x180" href="assets/img/favicon-180.png">
</head>
<body>
{header}
<main>
{body}
</main>
{footer}
<div class="modal" id="modal"><div class="modal__bd"></div><div class="modal__w" id="modal-w"></div></div>
<script src="assets/app.js"></script>
</body>
</html>
"""

PAGES = []

def page(slug, title, desc, body, active="", with_cta=True, cta_block=None):
    _CUR_PAGE["slug"] = slug
    _CUR_PAGE["title"] = title
    PAGES.append((slug, title))
    full = body + (cta_block if cta_block is not None else (cta() if with_cta else ""))
    htm = TPL.format(title=html.escape(title), desc=html.escape(desc),
                     header=header(active), body=full, footer=footer())
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug), "w", encoding="utf-8") as f:
        f.write(htm)
    return slug

def start(slug, title):
    """Открыть страницу для набора контента (нужно до вызова media())."""
    _CUR_PAGE["slug"] = slug
    _CUR_PAGE["title"] = title

# ---------------------------------------------------------------- блоки-конструкторы
def hero(slot, desc, eyebrow, title, lead="", stats=None, meta="", tall=True, crumbs=""):
    st = ""
    if stats:
        chunks = []
        for v, s, l in stats:
            suf = ' data-suffix="' + s + '"' if s else ""
            chunks.append('<div class="hero__stat"><b data-count="' + str(v) + '"' + suf +
                          '>0</b><span>' + l + "</span></div>")
        st = '<div class="hero__stats" data-stagger>' + "".join(chunks) + "</div>"
    return f"""
<section class="hero{'' if tall else ' hero--page'}">
  <div class="hero__bg">{media(slot, "fill", desc)}{scrim("b")}{scrim("l")}</div>
  <div class="container hero__in">
    {crumbs}
    <div class="hero__grid">
      <div>
        <p class="eyebrow" data-reveal>{eyebrow}</p>
        <h1 class="{'h-display' if tall else 'h1'}" data-split>{title}</h1>
        {f'<p class="lead measure u-mt-sm" data-reveal data-delay=".15">{lead}</p>' if lead else ''}
      </div>
      {f'<div class="hero__meta" data-reveal data-delay=".25">{meta}</div>' if meta else ''}
    </div>
    {st}
  </div>
  {'<div class="scroll-hint"><span>Листайте</span><i></i></div>' if tall else ''}
</section>"""

def crumbs(*items):
    h = '<div class="crumbs" data-reveal><a href="index.html">Главная</a>'
    for it in items:
        if isinstance(it, tuple):
            h += f'<span>/</span><a href="{it[1]}">{it[0]}</a>'
        else:
            h += f'<span>/</span><span>{it}</span>'
    return h + "</div>"

def halfband(slot, desc, eyebrow, title, body, link=None, rev=False, ratio="fill"):
    lk = f'<div class="u-mt-sm"><a class="link-u" href="{link[1]}">{link[0]} {ARW}</a></div>' if link else ""
    return f"""
<section class="halfband{' halfband--rev' if rev else ''}">
  <div class="halfband__media">{media(slot, ratio, desc, cls="parallax", attrs='data-speed=".1"')}</div>
  <div class="halfband__txt">
    <p class="eyebrow" data-reveal>{eyebrow}</p>
    <h2 class="h2" data-split>{title}</h2>
    <div class="body measure u-mt-sm" data-reveal data-delay=".1">{body}</div>
    {lk}
  </div>
</section>"""

def full_band(slot, desc, caption="", ratio="21:9"):
    band_r = {"21:9": "band--r219", "16:9": "band--r169", "3:2": "band--r32"}.get(ratio, "band--r219")
    return f"""
<section class="section section--tight">
  <div class="band {band_r}">
    {media(slot, "fill", desc, cls="parallax", attrs='data-speed=".14"')}
  </div>
  {f'<div class="container"><p class="media__cap">{caption}</p></div>' if caption else ''}
</section>"""

def head_row(eyebrow, title, right=""):
    return f"""<div class="head-row">
  <div><p class="eyebrow" data-reveal>{eyebrow}</p><h2 class="h2 measure" data-split>{title}</h2></div>
  {f'<div data-reveal data-delay=".15">{right}</div>' if right else ''}
</div>"""

def dircard(href, slot, desc, title, text):
    return f"""<a class="dircard" href="{href}">
  {media(slot, "fill", desc)}{scrim("b")}
  <div class="dircard__in">
    <h3 class="dircard__t">{title}</h3>
    <p class="dircard__d">{text}</p>
    <span class="dircard__go"><i></i> Смотреть</span>
  </div></a>"""

def feat(n, t, d):
    return f'<div class="feat"><span class="feat__n">{n}</span><h3 class="feat__t">{t}</h3><p class="feat__d">{d}</p></div>'

def specs(rows):
    return '<ul class="speclist">' + "".join(
        f'<li><span class="k">{k}</span><span class="v">{v}</span></li>' for k, v in rows) + "</ul>"

def ticks(items):
    return '<ul class="ticks">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def save_manifest():
    seen, uniq = set(), []
    for m in MEDIA:
        if m["slot"] in seen:
            continue
        seen.add(m["slot"])
        uniq.append(m)
    with open(os.path.join(OUT, "assets", "media-manifest.json"), "w", encoding="utf-8") as f:
        json.dump(uniq, f, ensure_ascii=False, indent=2)
