# ИНКАР-1 — демо-сайт

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
python3 -c "from PIL import Image; im=Image.open('in.png').convert('RGB'); im.thumbnail((2000,2000)); im.save('out.jpg',quality=84,optimize=True,progressive=True)"

# видео: H.264 CRF 24, без звука, быстрый старт
ffmpeg -i in.mp4 -an -c:v libx264 -crf 24 -preset slow -pix_fmt yuv420p        -movflags +faststart out.mp4

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
