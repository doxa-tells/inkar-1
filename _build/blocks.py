# -*- coding: utf-8 -*-
"""Переиспользуемые блоки: соцдоказательство, клиенты, счётчики, цикл, тендер-тизер."""

from lib import media, scrim, ARW, head_row, feat, ticks, specs

# (подпись, файл логотипа или None — тогда рисуется текстовый чип)
CLIENTS = [
    ("Металлургический комбинат, Темиртау", "client-arcelormittal.png"),
    ("Корпорация Казахмыс",                 "client-kazakhmys.png"),
    ("Казцинк",                             "client-kazzinc.png"),
    ("Шубарколь комир",                     "client-shubarkol.png"),
    ("Карагандинский литейно-машиностроительный завод", "client-klmz.png"),
    ("Евразийская Группа (ERG)",            None),
    ("АО «Соколовско-Сарбайское ГПО»",      None),
]

def _chip(title, file):
    if file:
        return (f'<span class="logo-chip logo-chip--img" title="{title}">'
                f'<img src="assets/img/{file}" alt="{title}" loading="lazy" height="120"></span>')
    return f'<span class="logo-chip"><i></i>{title}</span>'

def clients_marquee():
    row = "".join(_chip(t, f) for t, f in CLIENTS * 2)
    return f"""
<section class="section section--tight bg-2">
  <div class="container">
    <p class="eyebrow" data-reveal>Нам доверяют производство</p>
  </div>
  <div class="marquee" data-reveal><div class="marquee__row">{row}</div></div>
  <div class="container u-mt-sm">
    <p class="small" style="max-width:70ch">Поставляем узлы и запасные части предприятиям чёрной и цветной
    металлургии, горно-обогатительным комбинатам и энергетике Казахстана. Отдельные позиции —
    единственное производство в стране.</p>
  </div>
</section>"""

def social_proof():
    return f"""
<section class="section">
  <div class="container">
    {head_row("Цифры", "Завод, а не посредник.<br>Всё считается в станко-часах.",
              '<a class="btn btn--ghost" href="o-kompanii.html">О компании ' + ARW + "</a>")}
    <div class="stats" data-stagger>
      <div class="stat"><b data-count="1998">0</b><span>Год основания</span>
        <small>Непрерывная работа в металлообработке с апреля 1998 года.</small></div>
      <div class="stat"><b data-count="27" data-suffix="+">0</b><span>Лет на рынке</span>
        <small>От запасных частей — до комплексов производственных линий.</small></div>
      <div class="stat"><b data-count="60" data-suffix="+">0</b><span>Единиц оборудования</span>
        <small>Токарные, фрезерные, расточные, шлифовальные, термия, резка.</small></div>
      <div class="stat"><b data-count="4500" data-suffix="+">0</b><span>Позиций в год</span>
        <small>От единичных деталей до серийных партий по чертежам заказчика.</small></div>
    </div>
    <div class="grid g3 u-mt" data-stagger>
      <div class="quote">
        <p class="quote__t">«Единственное производство в Казахстане, способное обработать сверхпрочный
        наплавленный слой роликов МНЛЗ, выдержав требуемую чистоту поверхности и размеры».</p>
        <div class="quote__a"><b>Компетенция</b><span>Конвертерный цех, ОНРС</span></div>
      </div>
      <div class="quote">
        <p class="quote__t">«Единственный в стране производитель технологического инструмента — валков
        для изготовления электросварной трубы. Сталь Х12МФ / 1.2379, закалка до HRC 58…63».</p>
        <div class="quote__a"><b>Компетенция</b><span>Трубоэлектросварочное производство</span></div>
      </div>
      <div class="quote">
        <p class="quote__t">«Разработчик и изготовитель собственных линий профилегибочного оборудования
        с современной системой автоматического управления. Гарантия и сопровождение».</p>
        <div class="quote__a"><b>Компетенция</b><span>Нестандартное оборудование</span></div>
      </div>
    </div>
  </div>
</section>"""

def awards_row(slots):
    """slots: список (SLOT, описание, год, заголовок, текст)"""
    cards = ""
    for s, d, y, t, x in slots:
        cards += f"""<article class="award">{media(s, "4:3", d)}
          <div class="award__b"><span class="award__y">{y}</span>
          <h3 class="h4">{t}</h3><p class="small">{x}</p></div></article>"""
    return f'<div class="awards" data-stagger>{cards}</div>'

def cycle_pin():
    steps = [
        ("O1", "Приём задачи и чертежа", "PDF, DWG, DXF, STEP. Если чертежа нет — обмеряем образец или разрабатываем КД с нуля.",
         "CYCLE-01", "Крупный план: инженер разворачивает бумажный чертёж на столе рядом с изношенной деталью, свет от лампы сбоку, тёплый тон."),
        ("O2", "Конструкторская проработка", "Проверка изготовимости, подбор материала и припусков, разработка техпроцесса и УП для ЧПУ.",
         "CYCLE-02", "Экран CAD/CAM с 3D-моделью узла, отражение в очках конструктора, тёмный офис, холодное синее свечение монитора."),
        ("O3", "Заготовка и раскрой", "Газоплазменная резка листа толщиной до 180 мм, отрезка проката, подготовка поковок.",
         "CYCLE-03", "Плазменный резак ведёт рез по толстому листу, фонтан искр и оранжевый отсвет на металле, дым, длинная выдержка."),
        ("O4", "Механическая обработка", "Токарная, фрезерная, расточная, зубообработка, сверление. Крупногабарит и высокая точность.",
         "CYCLE-04", "Токарный станок в работе: стружка сходит спиралью с крупной детали, СОЖ бликует, полумрак цеха, узкий свет на зоне резания."),
        ("O5", "Термообработка и наплавка", "Закалка до HRC 58…63, наплавка рабочих поверхностей износостойкими материалами.",
         "CYCLE-05", "Раскалённая докрасна деталь выходит из печи, оператор в термокостюме и щитке, оранжевое зарево заливает цех."),
        ("O6", "Шлифование и финиш", "Круглое и плоское шлифование, доводка размеров и чистоты поверхности под чертёж.",
         "CYCLE-06", "Шлифовальный круг касается вала, тонкий веер искр, зеркальная поверхность металла, очень контрастный свет."),
        ("O7", "Контроль и отгрузка", "Замер по картам контроля, протокол ОТК, маркировка, паспорт изделия, упаковка и отгрузка.",
         "CYCLE-07", "Контролёр ОТК с микрометром у готовой детали на столе с гранитной плитой, чистый холодный свет, синие ящики на фоне."),
    ]
    panels = ""
    for n, t, d, slot, desc in steps:
        panels += f"""<div class="pin__panel">
          {media(slot, "4:3", desc)}
          <p class="card__num u-mt-sm">{n}</p>
          <h3 class="h3" style="margin:8px 0 8px">{t}</h3>
          <p class="small measure-sm">{d}</p>
        </div>"""
    return f"""
<section class="section bg-2">
  <div class="container">
    {head_row("Как устроено производство", "Полный цикл под одной крышей:<br>от чертежа до отгрузки.",
              '<a class="btn btn--ghost" href="uslugi.html">Технологии и услуги ' + ARW + "</a>")}
  </div>
  <div class="pin">
    <div class="pin__inner">
      <div class="pin__track" style="padding-left:var(--pad-x)">{panels}</div>
    </div>
  </div>
</section>"""

def registry_teaser():
    return f"""
<section class="section">
  <div class="container">
    {head_row("Новое", "Реестр изготовленных изделий.<br>Найдите свою позицию и повторите заказ.",
              '<a class="btn btn--solid" href="reestr.html">Открыть реестр ' + ARW + "</a>")}
    <div class="split split--wide-l">
      <div>{media("REG-HERO", "16:9", "Стеллаж с готовыми изделиями в цехе: валки, ролики, шестерни, каждый с биркой и QR-кодом. Ряд уходит в перспективу, направленный свет сверху, промышленный полумрак.")}</div>
      <div class="stack">
        <p class="lead">Каждая изготовленная позиция попадает в реестр: фото, превью чертежа,
        марка материала, режим термообработки, габарит, срок изготовления и класс точности.</p>
        {ticks([
          "Фильтры <b>отрасль → узел → материал → габарит</b> и поиск по номеру позиции",
          "Паспорт изделия с полными характеристиками и протоколом контроля",
          "Кнопка <b>«Заказать повтор»</b> — заявка уходит уже с привязкой к позиции",
          "Каждая карточка — отдельная посадочная страница под поисковые запросы",
        ])}
        <div><a class="link-u" href="reestr.html">Смотреть все позиции {ARW}</a></div>
      </div>
    </div>
  </div>
</section>"""

def tender_teaser():
    return f"""
<section class="section bg-2">
  <div class="container">
    <div class="split split--wide-r">
      <div class="stack">
        <p class="eyebrow" data-reveal>Отделу закупок</p>
        <h2 class="h2" data-split>Пакет документов для тендера —<br>одной кнопкой.</h2>
        <p class="body measure" data-reveal data-delay=".1">Реквизиты, свидетельство о регистрации,
        сертификат СТ-KZ, доля казахстанского содержания, справки об отсутствии задолженности,
        сертификаты системы менеджмента качества и благодарственные письма. Всё в одном архиве,
        в актуальной редакции.</p>
        <div class="gauge" data-reveal data-delay=".2" style="max-width:420px">
          <div class="gauge__lb"><span>Казахстанское содержание</span><span>СТ-KZ</span></div>
          <div class="gauge__bar"><i class="gauge__fill" data-w="87" style="display:block"></i></div>
          <div class="gauge__lb"><span>по товарам собственного производства</span><span>87 %</span></div>
        </div>
        <div class="u-flex u-gap u-wrap">
          <a class="btn btn--solid" href="tendery.html">Тендерный раздел {ARW}</a>
          <a class="btn btn--ghost" href="tendery.html#docs">Скачать пакет</a>
        </div>
      </div>
      <div>{media("TENDER-01", "4:3", "Строгий натюрморт сверху: папка с документами, печать, сертификаты в рамках, металлическая деталь как пресс-папье. Тёмная столешница, драматичный боковой свет, минимализм.")}</div>
    </div>
  </div>
</section>"""
