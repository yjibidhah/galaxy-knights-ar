#!/usr/bin/env python3
"""Build a child-friendly Arabic fan website. Uses Python standard library only."""
from pathlib import Path
import os
import json
import shutil
from html import escape
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "public"
ASSETS = ROOT / "assets"
SITE_URL = os.environ.get("SITE_URL", "https://galaxy-knights-ar.pages.dev").strip().rstrip("/")
NAME = "مجرة الفرسان"
SERIES = "أبطال الكرة: فرسان المجرة"
ROUTES = []

NAV = [
    ("/", "الرئيسية"),
    ("/episodes/", "الحلقات"),
    ("/characters/", "الشخصيات"),
    ("/articles/", "المقالات"),
    ("/quiz/", "التحدي"),
]

def full_url(path):
    return SITE_URL + path if SITE_URL else ""

def safe(text):
    return escape(str(text), quote=True)

def link(path, label, cls=""):
    return '<a href="{}" class="{}">{}</a>'.format(path, safe(cls), safe(label))

def card(title, description, route, icon="⚽"):
    return '<a href="{}" class="card" data-search><span class="art" aria-hidden="true">{}</span><h3>{}</h3><p>{}</p><span class="more">اكتشف المزيد ←</span></a>'.format(route,icon,safe(title),safe(description))

def cards(items, cls=""):
    return '<div class="cards {}">{}</div>'.format(cls,"".join(card(*item) for item in items))

def breadcrumbs(route, title):
    if route == "/": return ""
    return '<nav class="breadcrumbs" aria-label="مسار التصفح"><a href="/">الرئيسية</a><span aria-hidden="true">/</span><span>{}</span></nav>'.format(safe(title))

def render(route, title, description, body, *, head="", article=False):
    route = route if route.startswith("/") else "/" + route
    full_title = "{} | {}".format(title, NAME) if route != "/" else "مجرة الفرسان | أبطال الكرة فرسان المجرة بالعربية"
    canonical = '<link rel="canonical" href="{}">'.format(safe(full_url(route))) if SITE_URL else ""
    og_url = '<meta property="og:url" content="{}">'.format(safe(full_url(route))) if SITE_URL else ""
    og_image = '<meta property="og:image" content="{}">'.format(safe(full_url("/assets/galaxy-hero-desktop.webp"))) if SITE_URL else ""
    current = lambda path: ' aria-current="page"' if route == path or (path != "/" and route.startswith(path)) else ""
    navbar = "".join('<a href="{}"{}>{}</a>'.format(p,current(p),safe(t)) for p,t in NAV)
    web_schema = {
        "@context":"https://schema.org",
        "@type":"WebSite" if route=="/" else "WebPage",
        "name": NAME if route=="/" else title,
        "inLanguage":"ar",
        "description":description
    }
    if SITE_URL: web_schema["url"] = full_url(route)
    schema = '<script type="application/ld+json">{}</script>'.format(json.dumps(web_schema,ensure_ascii=False).replace("</", "<\\/"))
    main_heading = '' if route=="/" else '<div class="page-heading shell">{}<h1>{}</h1><p class="section-intro">{}</p></div>'.format(breadcrumbs(route,title),safe(title),safe(description))
    main_content = body if route == "/" else '<div class="shell"><div class="{}">{}</div></div>'.format("article" if article else "section",body)
    html = '''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#07132d">
<meta name="robots" content="index,follow,max-image-preview:large">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ar_AR">
<meta property="og:site_name" content="مجرة الفرسان">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
{canonical}{og_url}{og_image}
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="stylesheet" href="/assets/styles.css?v=galaxy-layout-fix-20261110">
{schema}{head}
<script defer src="/assets/app.js"></script>
</head>
<body>
<a class="skip" href="#main">تخطَّ إلى المحتوى</a>
<header class="site-header"><div class="shell topbar">
<a class="brand" href="/" aria-label="مجرة الفرسان، الصفحة الرئيسية"><span class="brand-mark" aria-hidden="true"><img class="brand-emblem" src="/assets/favicon.svg" width="38" height="38" alt=""></span><span>مجرة الفرسان</span></a>
<button id="menu-btn" class="menu-btn" aria-expanded="false" aria-controls="main-nav" aria-label="فتح قائمة الموقع">☰</button>
<nav id="main-nav" class="nav" aria-label="القائمة الرئيسية">{navbar}</nav>
</div></header>
<main id="main">{heading}{body}</main>
<footer class="site-footer"><div class="shell footer-grid">
<div><div class="brand"><span class="brand-mark" aria-hidden="true"><img class="brand-emblem" src="/assets/favicon.svg" width="38" height="38" alt=""></span>مجرة الفرسان</div>
<p>مساحة عربية مستقلة لمحبي أبطال الكرة: فرسان المجرة، تقدم أدلة أصلية وتحديات مرحة ومحتوى مناسبًا للعائلة.</p>
<p class="tiny">موقع معجبين مستقل وغير تابع للشركات المالكة للأنمي. لا يوفر حلقات مقرصنة.</p></div>
<div class="footer-links"><a href="/about/">من نحن</a><a href="/contact/">تواصل معنا</a><a href="/privacy/">الخصوصية</a><a href="/episodes/">الحلقات</a></div>
</div></footer>
</body></html>'''.format(title=safe(full_title),desc=safe(description),canonical=canonical,og_url=og_url,og_image=og_image,schema=schema,head=head,navbar=navbar,heading=main_heading,body=main_content)
    output = OUT / (route.lstrip("/") + "index.html" if route!="/" else "index.html")
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(html,encoding="utf-8")
    ROUTES.append(route)

def section(title, intro, content, href="", linktext="عرض الكل"):
    view = link(href,linktext,"btn secondary") if href else ""
    return '<section class="section"><div class="section-head"><div><h2>{}</h2><p class="section-intro">{}</p></div>{}</div>{}</section>'.format(safe(title),safe(intro),view,content)

def write_home():
    critical_style = """<style>
/* Homepage critical CSS: full-width banner; also protects against stale cached stylesheets. */
#main{display:block;width:100%;max-width:none;margin:0}
#main>.galaxy-hero{display:block;position:relative;clear:both;width:100%;max-width:none;overflow:hidden;padding:0 0 52px;background:linear-gradient(180deg,#081a3c,#071b36)}
#main .galaxy-hero-picture{display:block;width:100%;max-width:none;margin:0;overflow:hidden}
#main .galaxy-hero-picture img{display:block;width:100%;height:auto;max-height:680px;aspect-ratio:3/1;object-fit:cover;object-position:center}
#main .galaxy-hero-panel{position:relative;box-sizing:border-box;width:min(1160px,92%);max-width:1160px;margin:-24px auto 0;padding:24px 30px;border:1px solid #3c77ac;border-radius:22px;background:linear-gradient(115deg,#06172ef7,#102855f0);box-shadow:0 22px 54px #0008;display:flex;align-items:center;justify-content:space-between;gap:26px;backdrop-filter:blur(12px)}
#main .galaxy-hero-copy{flex:1;min-width:0}
#main .galaxy-hero-kicker{color:#67efff;font-weight:900;font-size:.9rem}
#main .galaxy-hero-panel h1{color:#fff;font-size:clamp(1.6rem,2.6vw,2.5rem);line-height:1.35;margin:6px 0}
#main .galaxy-hero-panel p{margin:0;color:#c7daf1;font-size:1rem;line-height:1.85}
#main .galaxy-hero-links{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
#main .galaxy-hero-links .btn{white-space:nowrap}
@media(max-width:900px){#main .galaxy-hero-panel{flex-direction:column;align-items:stretch;gap:16px}#main .galaxy-hero-links{justify-content:flex-start}}
@media(max-width:700px){#main>.galaxy-hero{padding-bottom:24px}#main .galaxy-hero-picture img{aspect-ratio:1/1;max-height:none;object-fit:cover}#main .galaxy-hero-panel{margin:-10px auto 0;padding:16px;border-radius:17px}#main .galaxy-hero-links{display:grid;grid-template-columns:1fr;gap:10px}#main .galaxy-hero-links .btn{width:100%;white-space:normal}#main .galaxy-hero-panel p{font-size:.92rem}}
</style>"""
    hero = '''<section class="galaxy-hero" aria-label="مقدمة موقع مجرة الفرسان">
    <picture class="galaxy-hero-picture">
      <source media="(max-width: 700px)" srcset="/assets/galaxy-hero-mobile.webp" type="image/webp">
      <img src="/assets/galaxy-hero-desktop.webp" width="1200" height="400" fetchpriority="high" decoding="async" alt="ملصق أنمي مجرّي يجمع الأبطال تنما وشيندو وتسووروجي مع كرة قدم مضيئة، وعنوان أبطال الكرة فرسان المجرة">
    </picture>
    <div class="shell galaxy-hero-panel">
      <div class="galaxy-hero-copy">
        <span class="galaxy-hero-kicker">⚽ انطلق مع أبطال المجرة</span>
        <h1>أبطال الكرة: فرسان المجرة</h1>
        <p>مغامرتك تبدأ من هنا! استكشف الشخصيات، وتابع دليل الحلقات، وخُض تحديات ممتعة باللغة العربية.</p>
      </div>
      <div class="galaxy-hero-links" aria-label="ابدأ الاستكشاف">
        <a class="btn primary" href="/episodes/">اكتشف الحلقات ←</a>
        <a class="btn secondary" href="/quiz/">اختبر معلوماتك ✨</a>
      </div>
    </div>
  </section>'''
    main = '<div class="shell">'+section("استكشف العالم","كل شيء في مكان واحد، بتجربة عربية سهلة على الهاتف والحاسوب.",cards([
        ("دليل الحلقات","تابع تقدمك عبر الحلقات الـ43 من النسخة اليابانية الأصلية.","/episodes/","🎬"),
        ("أبطال القصة","صفحات تعريفية بالشخصيات وأدوارها في عالم كرة القدم.","/characters/","🌟"),
        ("تحدي الفرسان","اختبار تفاعلي ممتع من ثمانية أسئلة.","/quiz/","🏆")
    ]))+section("اقرأ وتعلّم","مقالات أصلية للتعرّف أكثر على المسلسل وأفكاره.",cards([
        ("قصة فرسان المجرة","مدخل دون حرق كبير للأحداث.","/articles/story/","🌌"),
        ("ترتيب المشاهدة","من أين تبدأ وما الذي يجب معرفته؟","/articles/watch-order/","🧭"),
        ("دليل الشخصيات","كيف تتعرّف على أبطالك المفضلين؟","/articles/characters-guide/","👥")
    ]))+'<div class="callout"><h2>شارك روح الفريق ⚽</h2><p>كل لاعب يملك مهارة مختلفة، والعمل الجماعي والاحترام يصنعان فريقًا أقوى. هذا الموقع مساحة تشجع المرح والروح الرياضية بعيدًا عن الإساءة أو مشاركة البيانات الشخصية.</p></div></div>'
    render("/","أبطال الكرة فرسان المجرة","موقع مجرة الفرسان العربي: دليل حلقات أبطال الكرة فرسان المجرة، الشخصيات، المقالات والاختبارات التفاعلية.",hero+main,head=critical_style)

CHARACTERS = [
    ("bayan","بيان","الشخصيات البارزة في النسخة العربية", "⚡","اكتشف صفحة بيان ضمن دليل الشخصيات باللغة العربية."),
    ("hayyan","حيان","الحماس وروح التحدي","🔥","تعرّف على حيان وأسباب حب الجمهور لشخصيات أبطال الكرة."),
    ("oqab","عقاب","التركيز والعمل الجماعي","🦅","صفحة مخصصة لعقاب مع لمحة عن متابعة تطور الشخصيات.")
]

def write_characters():
    items = [(name,"صفحة تعريفية وحقائق عامة وشخصيات عالم فرسان المجرة.","/characters/{}/".format(slug),icon) for slug,name,subtitle,icon,desc in CHARACTERS]
    render("/characters/","شخصيات أبطال الكرة فرسان المجرة","استكشف شخصيات أبطال الكرة فرسان المجرة بالعربية، ومنها بيان وحيان وعقاب.",'<div class="toolbar"><input id="search-site" class="field" type="search" placeholder="ابحث عن شخصية" aria-label="ابحث عن شخصية"></div>'+cards(items)+'<p id="search-empty" class="empty" hidden>لا توجد نتائج مطابقة.</p>')
    for slug,name,subtitle,icon,desc in CHARACTERS:
        body='<span class="chip">دليل شخصيات فرسان المجرة</span><div style="font-size:5rem" aria-hidden="true">{}</div><p>{}</p><h2>كيف تستكشف شخصية {}؟</h2><p>عند مشاهدة الحلقات، تابع طريقة تعامل الشخصية مع زملائها وكيف تتغير قراراتها في أوقات التحدي. لاحظ متى تعتمد على مهاراتها، ومتى تستفيد من دعم الفريق.</p><h2>نصيحة للمشاهد</h2><p>يمكنك تدوين لحظاتك المفضلة ومناقشتها مع أصدقائك باحترام، مع تجنب نشر حرق للأحداث لمن لم يشاهد الحلقات بعد.</p><div class="notice">هذه مقدمة عامة لمحبّي المسلسل، وليست سيرة رسمية أو نصًا منقولًا عن الشركة المنتجة.</div><a class="btn secondary" href="/characters/">كل الشخصيات</a>'.format(icon,desc,safe(name))
        render("/characters/{}/".format(slug),"{} - أبطال الكرة فرسان المجرة".format(name),"اكتشف صفحة شخصية {} في موقع مجرة الفرسان العربي.".format(name),body,article=True)

ARTICLES = [
    ("story","قصة أبطال الكرة فرسان المجرة","ما الذي يميز رحلة كرة القدم في هذا الجزء؟","🌌",[
        ("مدخل إلى عالم المسلسل","أبطال الكرة: فرسان المجرة هو الاسم الذي يعرف به بعض الجمهور العربي مسلسل Inazuma Eleven GO Galaxy، وهو جزء من عالم يجمع كرة القدم والخيال والحماس. تدور التجربة حول مباريات مختلفة، وتحديات متصاعدة، وشخصيات تتعلم كيف تتعامل مع الضغط وتعمل كفريق."),
        ("لماذا يحب المشاهدون هذا العالم؟","يمزج الأنمي المباريات الدرامية بالمهارات المبالغ فيها والروابط بين اللاعبين. كل مباراة تمنح الجمهور فرصة لاكتشاف أساليب جديدة للتعاون، واتخاذ القرارات، والقتال من أجل الهدف دون التخلي عن الروح الرياضية."),
        ("كيف تبدأ متابعته؟","إذا كنت جديدًا على عالم أبطال الكرة، يمكنك البدء بالتعرّف على السلسلة وأجزائها، ثم مراجعة دليل ترتيب المشاهدة في موقعنا. وإن كنت تعرف الشخصيات مسبقًا، انتقل إلى قائمة الحلقات ونظّم تقدمك بنفسك."),
        ("بدون حرق","نتجنب هنا كشف النتائج المهمة للمباريات أو مفاجآت القصة حتى تبقى متعة الاكتشاف عند المشاهدة.")
    ]),
    ("watch-order","ترتيب مشاهدة أبطال الكرة فرسان المجرة","دليل للمبتدئين مع توضيح الفرق بين النسخة اليابانية والدبلجة.","🧭",[
        ("من أين أبدأ؟","إذا كانت هذه تجربتك الأولى مع Inazuma Eleven، فقد يساعدك التعرف على الأجزاء السابقة من سلسلة GO لفهم العلاقات بين بعض الشخصيات. لكن يمكنك أيضًا الاستمتاع بعالم Galaxy مع قراءة ملخص عام للسياق."),
        ("عدد الحلقات","النسخة اليابانية الأصلية من Inazuma Eleven GO Galaxy تتكون من 43 حلقة. قد تختلف طريقة تقسيم حلقات العرض العربي أو تسميتها بحسب منصة البث أو إصدار الدبلجة؛ لذلك يعتمد متتبع الحلقات هنا الترقيم الياباني الأصلي بوضوح."),
        ("طريقة تنظيم المشاهدة","افتح دليل الحلقات، واضغط على كل حلقة تنتهي منها. سيحتفظ متصفحك بتقدمك على الجهاز نفسه فقط دون إنشاء حساب. يمكنك العودة في أي وقت لتكملة رحلتك."),
        ("أين أشاهد؟","احرص على استخدام مصادر مشاهدة رسمية مرخّصة متاحة في بلدك. هذا الموقع يقدم معلومات وتحديات ولا يستضيف الحلقات أو يعيد نشرها.")
    ]),
    ("characters-guide","دليل شخصيات فرسان المجرة","نصائح لاكتشاف أبطال الأنمي وتحليل أدوارهم.","👥",[
        ("ما الذي يجعل الشخصية مميزة؟","ليست المهارات وحدها ما يحدد قوة اللاعب. الشخصية تصبح أكثر إثارة للاهتمام عندما يظهر أسلوبها في التعامل مع الصعوبات، وطريقتها في تشجيع زملائها، وقدرتها على التعلم من الأخطاء."),
        ("كيف تقارن بين الشخصيات؟","يمكن مقارنة الشخصيات من خلال التعاون، والثبات أمام الضغط، والتطور، والقدرة على احترام المنافسين. تجنب المقارنات الجارحة، واستمتع باختلاف نقاط القوة."),
        ("اصنع قائمتك الخاصة","ضع قائمة بخمسة لاعبين تفضلهم. اسأل نفسك عن السبب لكل اختيار: هل هي الشجاعة أم ذكاء اللعب أم الولاء للأصدقاء؟ هكذا تصبح مشاهدة الأنمي فرصة للنقاش الإيجابي."),
        ("اكتشف صفحاتنا","ابدأ بزيارة دليل الشخصيات الموجود على الموقع، واختر الشخصية التي تريد معرفة المزيد عنها.")
    ]),
    ("lessons","دروس من أبطال الكرة: روح الفريق والصداقة","أفكار إيجابية يمكن أن يستفيد منها المتابعون الصغار.","💛",[
        ("لا أحد يفوز وحده","قد يكون لدى أحد اللاعبين مهارة استثنائية، لكن المباريات تذكرنا بأن كل لاعب يحتاج إلى الثقة في زملائه. النجاح ليس مجرد تسجيل هدف بل مشاركة المسؤولية."),
        ("التدرب أفضل من الاستسلام","حين يواجه الفريق خصمًا صعبًا، يستطيع البحث عن طريقة أفضل للتعلم والتحسن. يمكن تطبيق هذه الفكرة على الدراسة والرياضة والهوايات في الحياة اليومية."),
        ("احترام الخصوم","المنافس ليس عدوًا. المنافسة تساعدنا على اكتشاف قدراتنا، بشرط الحفاظ على الأدب والاحترام، حتى عند الخسارة."),
        ("الصداقة والأمان الرقمي","استمتع بمناقشة الأنمي مع الأصدقاء، لكن لا تشارك معلوماتك الشخصية أو صورك الخاصة مع غرباء في الإنترنت. وإذا أزعجك شخص، أخبر شخصًا بالغًا تثق به.")
    ])
]

def article_html(slug,title,intro,emoji,parts):
    chunks=['<span class="chip">مقال أصلي • مجرة الفرسان</span><p>{}</p>'.format(safe(intro))]
    for h,p in parts: chunks.append('<h2>{}</h2><p>{}</p>'.format(safe(h),safe(p)))
    chunks.append('<div class="notice">اقرأ أيضًا: {} • {} • {}</div>'.format(link('/articles/watch-order/','ترتيب المشاهدة'),link('/characters/','الشخصيات'),link('/quiz/','اختبار الفرسان')))
    return "".join(chunks)

def write_articles():
    render("/articles/","مقالات أبطال الكرة فرسان المجرة","مقالات عربية أصلية عن قصة أبطال الكرة فرسان المجرة وترتيب المشاهدة والشخصيات وروح الفريق.",'<div class="toolbar"><input id="search-site" type="search" class="field" placeholder="ابحث بين المقالات" aria-label="بحث المقالات"></div>'+cards([(title,intro,"/articles/{}/".format(slug),emoji) for slug,title,intro,emoji,parts in ARTICLES])+'<p id="search-empty" class="empty" hidden>لم نجد مقالات بهذه الكلمات.</p>')
    for slug,title,intro,emoji,parts in ARTICLES:
        render("/articles/{}/".format(slug),title,intro,article_html(slug,title,intro,emoji,parts),article=True)

def write_episodes():
    eps="".join('<button type="button" class="episode" data-episode="{}" aria-pressed="false"><span>الحلقة {:02d}</span><span class="episode-status">لم أشاهدها</span></button>'.format(n,n) for n in range(1,44))
    body='''<div class="notice"><strong>معلومة مهمة:</strong> هذا الدليل يعتمد ترقيم <strong>43 حلقة من النسخة اليابانية الأصلية</strong> لمسلسل Inazuma Eleven GO Galaxy. قد يختلف عدد أو تقسيم حلقات النسخ العربية حسب جهة العرض. لا توجد روابط مشاهدة غير مرخصة هنا.</div>
<div class="callout"><h2>تقدم المشاهدة: <span id="watched-count">0</span> / 43</h2><div class="progress-track" role="progressbar" id="watch-progress" aria-label="نسبة الحلقات التي شاهدتها" aria-valuemin="0" aria-valuemax="43" aria-valuenow="0"><div class="progress-bar"></div></div>
<p class="tiny">يُحفظ تقدمك محليًا في هذا المتصفح فقط، دون إنشاء حساب أو إرسال بيانات إلينا.</p></div>
<div class="toolbar"><input class="field" id="episode-filter" type="search" inputmode="numeric" placeholder="ابحث برقم الحلقة، مثل 12" aria-label="البحث برقم الحلقة"><button id="reset-watch" type="button" class="btn">مسح التقدم</button></div>
<div class="episodes-grid">'''+eps+'''</div><a href="/articles/watch-order/" class="btn secondary">اقرأ دليل ترتيب المشاهدة</a>'''
    render("/episodes/","حلقات أبطال الكرة فرسان المجرة كاملة بالترتيب","دليل ترتيب حلقات أبطال الكرة فرسان المجرة: قائمة 43 حلقة يابانية أصلية مع متتبع تقدم مشاهدة مجاني.",body)

def write_quiz():
    body='''<div class="callout"><h2>هل أنت من أبطال المجرة؟ 🏆</h2><p>ثمانية أسئلة ممتعة عن كرة القدم والمسلسل. لا حاجة إلى التسجيل أو إدخال الاسم أو البريد الإلكتروني.</p></div>
<div id="quiz-area" class="quiz" aria-live="polite"><p>جارٍ تحميل التحدي...</p></div>
<div class="notice">نتيجتك تبقى على هذا الجهاز فقط. كن لطيفًا مع أصدقائك عند مقارنة النقاط.</div>'''
    render("/quiz/","اختبار أبطال الكرة فرسان المجرة","اختبار عربي مجاني وتفاعلي لمحبي أبطال الكرة فرسان المجرة: ثمانية أسئلة وتحديات رياضية.",body)

def write_info():
    about='<h2>من نحن؟</h2><p>مجرة الفرسان موقع عربي مستقل من صنع محبّي عالم أبطال الكرة، يهدف إلى تقديم محتوى أصلي ممتع وسهل القراءة عن فرسان المجرة، مع أدوات لمتابعة الحلقات وتحديات معرفية بسيطة.</p><h2>هل الموقع رسمي؟</h2><p>لا. الموقع ليس تابعًا لـ LEVEL-5 أو الجهات المنتجة أو الموزعة للمسلسل. جميع حقوق الشخصيات والعناوين الأصلية لأصحابها. الرسوم التخطيطية المستخدمة هنا أصلية وليست منسوخة من لقطات الأنمي.</p><h2>ماذا نقدم؟</h2><p>مقالات تعريفية، صفحات شخصيات، دليل للحلقات، واختبارات مناسبة للعائلة. لا نستضيف نسخًا مقرصنة من الحلقات أو نطلب معلومات شخصية من الأطفال.</p>'
    render("/about/","من نحن - مجرة الفرسان","تعرف إلى مشروع مجرة الفرسان، موقع عربي مستقل لمحبي أبطال الكرة فرسان المجرة.",about,article=True)
    contact='<h2>للتواصل</h2><p>نرحب باقتراحات تطوير الموقع وتصحيح المعلومات. سنضيف رابط التواصل الرسمي لحسابات المجتمع بعد تأكيد مالك الموقع لعناوين صفحاته على يوتيوب وفيسبوك.</p><div class="notice">لا ترسل اسمك الكامل أو رقم هاتفك أو عنوانك أو صورك الشخصية. إذا كنت صغير السن، اطلب مساعدة أحد والديك أو شخص بالغ تثق به قبل التواصل مع أي جهة عبر الإنترنت.</div>'
    render("/contact/","تواصل معنا","طرق التواصل مع فريق موقع مجرة الفرسان ومشاركة الاقتراحات لتطوير المحتوى.",contact,article=True)
    privacy='<h2>سياسة الخصوصية</h2><p>هذا الموقع في نسخته الأولى لا يقدم حسابات شخصية ولا يجمع أسماء أو عناوين بريد إلكتروني أو أرقام هواتف أو معلومات تسجيل من الزائرين.</p><h2>تقدم الحلقات والاختبار</h2><p>يمكن أن يحفظ متصفحك تقدم المشاهدة وأفضل نتيجة في الاختبار باستخدام التخزين المحلي على جهازك. لا ترسل هذه المعلومات إلى خادم الموقع. يمكنك حذفها من إعدادات المتصفح أو عبر زر مسح التقدم.</p><h2>الاستضافة والخدمات الخارجية</h2><p>عند زيارتك قد تعالج شركة الاستضافة بيانات تقنية ضرورية لتقديم الموقع وحمايته، مثل عنوان IP، حسب سياساتها. نحاول الحد من أدوات الأطراف الثالثة؛ وقد يُطلب تحميل خط عربي من خدمة Google Fonts.</p><h2>الإعلانات</h2><p>لا يحتوي الإصدار الأول على شبكات إعلانات أو أدوات تتبع إعلاني. إذا أضفنا إعلانات لاحقًا، سنراجع متطلبات حماية الأطفال ونحدّث هذه الصفحة قبل التفعيل.</p><h2>حقوق المحتوى</h2><p>كل ما يتعلق بالأنمي من أسماء وعلامات يظل ملكًا لأصحابه الأصليين. النصوص التعريفية والتصميمات في الموقع مستقلة.</p>'
    render("/privacy/","سياسة الخصوصية","سياسة خصوصية موقع مجرة الفرسان: تتبع محلي لتقدم الحلقات والاختبار دون حسابات شخصية.",privacy,article=True)

def write_files():
    OUT.mkdir(parents=True,exist_ok=True)
    shutil.copytree(ASSETS,OUT/"assets",dirs_exist_ok=True)
    (OUT/"_headers").write_text('''/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
  Permissions-Policy: geolocation=(), microphone=(), camera=()
  Content-Security-Policy: frame-ancestors 'self'
/assets/*
  Cache-Control: public, max-age=86400
''',encoding="utf-8")
    (OUT/"_redirects").write_text("/home / 301\n",encoding="utf-8")
    (OUT/"robots.txt").write_text("User-agent: *\nAllow: /\n"+("Sitemap: "+SITE_URL+"/sitemap.xml\n" if SITE_URL else ""),encoding="utf-8")
    if SITE_URL:
        lines=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        lines += ["  <url><loc>{}</loc></url>".format(safe(full_url(route))) for route in ROUTES]
        lines.append("</urlset>")
        (OUT/"sitemap.xml").write_text("\n".join(lines),encoding="utf-8")
    else:
        (OUT/"sitemap.xml").unlink(missing_ok=True)
    (OUT/"404.html").write_text('''<!doctype html><html lang="ar" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>الصفحة غير موجودة | مجرة الفرسان</title><link rel="stylesheet" href="/assets/styles.css"><main class="shell page-heading"><h1>404 - الصفحة غير موجودة 🚀</h1><p>ربما ابتعدنا قليلًا عن المجرة!</p><a href="/" class="btn primary">العودة للرئيسية</a></main></html>''',encoding="utf-8")

if __name__ == "__main__":
    if OUT.exists():
        shutil.rmtree(OUT)
    write_home()
    write_episodes()
    write_characters()
    write_articles()
    write_quiz()
    write_info()
    write_files()
    print("Built {} Arabic pages. SITE_URL={}".format(len(ROUTES),SITE_URL or "(not configured yet)"))
