# -*- coding: utf-8 -*-
"""Сборка сайта ИНКАР-1. Запуск: python3 _build/build.py"""

import os, sys, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import lib
import pages_core, pages_prod, pages_serv, pages_new

STYLE = ("Единый киношный стиль для всех кадров:\n"
 "  · тяжёлая индустриальная кинематография, референс — рекламные ролики промышленных брендов;\n"
 "  · тёмная база: графит, вороненая сталь, бетон; акценты — раскалённый оранжевый и холодный "
 "сине-стальной;\n"
 "  · один доминирующий направленный источник света, глубокие тени, объёмный свет в дыму и пыли;\n"
 "  · оптика 35–85 мм, малая глубина резкости на предметных кадрах, широкий угол на общих планах;\n"
 "  · лёгкое зерно, анаморфные блики допустимы, без HDR-пересветов и без пластиковой глянцевости;\n"
 "  · люди — достоверные рабочие в спецовке и СИЗ, без постановочных улыбок;\n"
 "  · никаких читаемых логотипов и брендов на технике.\n")


def brief():
    """MEDIA-TODO.md — слоты, для которых кадра ещё нет (с готовыми промптами).
    Полный справочник по всем слотам лежит в MEDIA-BRIEF.md и правится вручную."""
    seen, uniq = set(), []
    for m in lib.MEDIA:
        if m["slot"] in seen:
            continue
        seen.add(m["slot"])
        uniq.append(m)

    done = [m for m in uniq if m.get("src")]
    todo = [m for m in uniq if not m.get("src")]

    by_page = collections.OrderedDict()
    for m in todo:
        by_page.setdefault((m["page"], m["page_title"]), []).append(m)

    lines = ["# Что ещё нужно сгенерировать", "",
             f"Готово: **{len(done)}** из {len(uniq)} слотов. Осталось: **{len(todo)}** "
             f"(фото {len([m for m in todo if m['kind'] != 'video'])}, "
             f"видео {len([m for m in todo if m['kind'] == 'video'])}).", "",
             "Файл пересобирается автоматически: как только кадр попадает в `assets/img/`",
             "под именем слота, слот исчезает из этого списка.", "",
             "## Уже подставлено", ""]
    for m in done:
        lines.append(f"- `{m['slot']}` → `{m['src']}`")
    lines += ["", "---", ""]

    for (slug, title), items in by_page.items():
        nv = len([m for m in items if m["kind"] == "video"])
        lines.append(f"## {title}")
        lines.append(f"`{slug}` — осталось {len(items)}, из них видео: {nv}\n")
        for m in items:
            lines.append(f"### `{m['slot']}` · {'ВИДЕО' if m['kind'] == 'video' else 'фото'} · {m['ratio']}\n")
            lines.append("```")
            lines.append(m["prompt"])
            lines.append("```\n")
        lines.append("---\n")

    with open(os.path.join(lib.OUT, "MEDIA-TODO.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Кадров подставлено: {len(done)} / {len(uniq)}")


README = """# ИНКАР-1 — демо-сайт

Статический сайт в стиле icomat.co.uk: тёмная кинематографичная подача, full-bleed медиа,
pill-навигация, mono-подписи, анимации появления, sticky-скролл, переходы между страницами.

## Запуск

Откройте `index.html` в браузере. Для корректной работы реестра (он читает `assets/registry.json`
через fetch) поднимите локальный сервер:

```
cd inkar && python3 -m http.server 8000
```

и откройте http://localhost:8000

## Структура

```
inkar/
  index.html                    Главная
  o-kompanii.html               О компании
  sertifikaty.html              Сертификаты и награды
  otzyvy.html                   Отзывы
  fotogalereya.html             Фотогалерея
  novosti.html                  Новости / хроника производства
  kontakty.html                 Контакты
  proizvodstvo.html             Производство — хаб
  proizvodstvo-*.html           5 направлений производства
  uslugi.html                   Услуги — хаб
  usluga-*.html                 7 страниц технологий
  reestr.html                   НОВОЕ — реестр изделий с фильтрами
  tendery.html                  НОВОЕ — тендерный блок
  request.html                  НОВОЕ — заявка с загрузкой чертежа
  assets/
    style.css                   Дизайн-система
    app.js                      Анимации, фильтры, форма
    registry.json               Данные реестра (26 позиций)
    media-manifest.json         Все медиа-слоты машиночитаемо
    img/                        Сюда класть ИИ-кадры
    docs/                       Сюда класть PDF для тендерного пакета
  MEDIA-BRIEF.md                Бриф по всем слотам под генерацию
```

## Медиа-слоты

Каждый кадр — `<figure class="media" data-slot="..." data-desc="...">`. Пока файла нет,
рисуется пустышка с номером слота и описанием будущего кадра.

**Подстановка автоматическая.** Положите файл в `assets/img/` и назовите его именем слота:

```
assets/img/HERO-01.mp4          видео для слота HERO-01
assets/img/HERO-01-poster.jpg   постер к нему (необязательно)
assets/img/DIR-MET.jpg          фото для слота DIR-MET
```

После этого запустите пересборку — `data-src` проставится сам:

```
python3 _build/build.py
```

Оставшиеся незакрытые слоты с готовыми промптами собираются в `MEDIA-TODO.md`.
Полный справочник по всем 184 слотам — `MEDIA-BRIEF.md`, интерактивный — `prompts.html`.

## Оптимизация медиа

Исходники из генератора весят по 8–14 МБ. Перед публикацией прогоняйте их через:

```
# фото: ширина 2000, JPEG q=84, прогрессивный
python3 -c "from PIL import Image; im=Image.open('in.png').convert('RGB'); \
im.thumbnail((2000,2000)); im.save('out.jpg',quality=84,optimize=True,progressive=True)"

# видео: H.264 CRF 24, без звука, быстрый старт
ffmpeg -i in.mp4 -an -c:v libx264 -crf 24 -preset slow -pix_fmt yuv420p \
       -movflags +faststart out.mp4

# постер-кадр
ffmpeg -ss 1 -i in.mp4 -frames:v 1 -vf scale=1600:-2 -q:v 4 out-poster.jpg
```

Текущие материалы уже сжаты: фото 113 → 5 МБ, видео 50 → 8 МБ без заметной потери качества.
Оригиналы лежат в `assets/img/_orig/` и в репозиторий не попадают.

## Шрифты

Сейчас подключены свободные аналоги через Google Fonts:

* заголовки — **Inter Tight** (аналог Helvetica Now Display);
* mono-подписи и навигация — **Roboto Mono** (аналог ABC Diatype Mono).

Чтобы поставить лицензионные: положите `.woff2` в `assets/fonts/`, раскомментируйте `@font-face`
в начале `style.css` и поменяйте `--font-display` / `--font-mono`.

## Логотип и фавикон

Логотип лежит в `assets/img/logo.png`. `app.js` находит его сам и подставляет в шапку,
подвал, занавес перехода, мобильное меню и «печать» в тендерном разделе — править HTML
не нужно. Поддерживаемые имена: `logo-inkar.svg`, `logo-inkar.png`, `logo.svg`, `logo.png`.

Фавиконки (`favicon-32.png`, `favicon-64.png`, `favicon-180.png`) собраны из логотипа.
Пересобрать после замены логотипа:

```
python3 - <<'EOF'
from PIL import Image
lg = Image.open("inkar/assets/img/logo.png").convert("RGBA")
for size in (32, 64, 180):
    pad = round(size*0.10); box = size - pad*2
    w, h = box, round(lg.height*box/lg.width)
    if h > box: h, w = box, round(lg.width*box/lg.height)
    c = Image.new("RGBA", (size,size), (8,9,10,255))
    r = lg.resize((w,h), Image.LANCZOS)
    c.paste(r, ((size-w)//2,(size-h)//2), r)
    c.save(f"inkar/assets/img/favicon-{size}.png", optimize=True)
EOF
```

## Фирменный цвет

Синий задан одной переменной в начале `style.css`:

```css
--accent:#2f6fd0;        /* основной */
--accent-light:#5a9ae8;  /* градиенты */
--accent-deep:#1b4b96;   /* тёмный акцент */
```

Поменяете `--accent` — перекрасится весь сайт: надзаголовки, кнопки, подчёркивания,
бейджи слотов, шкалы и полоса прогресса.

## Пересборка

```
python3 _build/build.py
```

Весь контент живёт в `_build/pages_*.py` — правьте там, а не в готовых HTML.

## Что нужно проверить перед публикацией

* реквизиты в `tendery.html` (БИН, НДС, доля казсодержания) — демонстрационные;
* характеристики станков в `o-kompanii.html` и на страницах услуг — ориентировочные;
* позиции реестра — демонстрационные, замените на реальные из вашей номенклатуры;
* форма заявки работает в демо-режиме и не отправляет данные на сервер.
"""


def main():
    os.makedirs(os.path.join(lib.OUT, "assets", "img"), exist_ok=True)
    os.makedirs(os.path.join(lib.OUT, "assets", "docs"), exist_ok=True)
    os.makedirs(os.path.join(lib.OUT, "assets", "fonts"), exist_ok=True)

    pages_core.build_all()
    pages_prod.build_all()
    pages_serv.build_all()
    pages_new.build_all()

    lib.save_manifest()
    brief()
    with open(os.path.join(lib.OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write(README)

    slots = [m["slot"] for m in lib.MEDIA]
    dupes = [s for s, c in collections.Counter(slots).items() if c > 1]
    print("Страниц:", len(set(p for p, _ in lib.PAGES)))
    print("Медиа-слотов:", len(lib.MEDIA), "| уникальных:", len(set(slots)))
    if dupes:
        print("Повторяющиеся слоты (это нормально, если кадр переиспользуется):", ", ".join(sorted(dupes)[:20]))


if __name__ == "__main__":
    main()
