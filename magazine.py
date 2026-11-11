"""Arabic editorial magazine builder for Galaxy Knights. Standard library only."""
from pathlib import Path
from html import escape
from datetime import date
import json

GROUPS = {
    "story": "العالم والقصة",
    "watch-order": "الحلقات",
    "characters-guide": "الشخصيات",
    "lessons": "القيم والرياضة",
    "team-guide": "الشخصيات",
    "galaxy-worlds": "العالم والقصة",
    "powers": "المهارات",
    "tactics": "المهارات",
    "bayan-leadership": "الشخصيات",
    "hayyan-spotlight": "الشخصيات",
    "nidal-spotlight": "الشخصيات",
}
FILTERS = ["الكل", "العالم والقصة", "الحلقات", "الشخصيات", "المهارات", "القيم والرياضة"]
CATEGORY_COLORS = {
    "العالم والقصة": "cyan",
    "الحلقات": "gold",
    "الشخصيات": "purple",
    "المهارات": "mint",
    "القيم والرياضة": "pink"
}
def h(value):
    return escape(str(value), quote=True)

def cover(article):
    alternate = {"watch-order": "episodes", "characters-guide": "characters"}
    return "/assets/article-" + alternate.get(article["slug"], article["slug"]) + ".svg"

def minutes(article):
    text = article["lead"] + " ".join(t + " " + p for t,p in article["sections"])
    return max(3, round(len(text.split()) / 170))

def safe_meta(article):
    return f'<span class="magazine-meta-item">📖 {minutes(article)} دقائق قراءة</span><span class="magazine-meta-item">✦ {h(article["category"])}</span>'

def video_card(video, cover_path, intro="", compact=False):
    vid = video["id"]
    if not vid or len(vid) != 11 or not all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-" for c in vid):
        return ""
    title, channel = h(video["title"]), h(video["channel"])
    href = f"https://www.youtube.com/watch?v={vid}"
    return f'''<div class="magazine-video {'compact' if compact else ''}" data-video-container>
        <div class="magazine-video-preview">
          <img src="{cover_path}" loading="lazy" width="800" height="500" alt="لوحة مرئية مستوحاة من عالم أبطال الكرة فرسان المجرة">
          <div class="magazine-video-front">
            <span class="magazine-video-source">▶ مقطع رسمي · {channel}</span>
            <h3>{title}</h3>
            <p>{h(intro) if intro else 'المقطع من قناة سبيستون غو الموثقة على يوتيوب.'}</p>
            <button type="button" class="magazine-video-play" data-load-video="{vid}" aria-label="تشغيل الفيديو الرسمي: {title}">▶ تشغيل المقطع</button>
          </div>
        </div>
        <div class="magazine-video-player" data-video-player hidden></div>
        <div class="magazine-video-note">لا يُحمّل مشغّل يوتيوب إلا بعد ضغطك على تشغيل. <a href="{href}" target="_blank" rel="noopener noreferrer">افتح المقطع على قناة سبيستون غو الرسمية ↗</a></div>
        </div>'''

def magazine_card(article, group_override=None, featured=False):
    url = "/articles/" + article["slug"] + "/"
    category = GROUPS.get(article["slug"], article["category"])
    return f'''<article class="magazine-card {'featured' if featured else ''}" data-magazine-card data-magazine-group="{h(category)}" data-magazine-slug="{h(article["slug"])}">
      <a href="{url}" class="magazine-card-link" aria-label="اقرأ {h(article["title"])}">
        <div class="magazine-card-photo"><img src="{cover(article)}" loading="lazy" width="640" height="390" alt="رسمة أصلية لموضوع {h(article["title"])}"></div>
        <div class="magazine-card-content">
          <span class="magazine-category {CATEGORY_COLORS.get(category, 'cyan')}">{h(category)}</span>
          <h3>{h(article["title"])}</h3>
          <p>{h(article["excerpt"])}</p>
          <div class="magazine-card-meta"><span>⏱ {minutes(article)} دقائق</span><span>اقرأ المقال ←</span></div>
        </div>
      </a>
      <button class="magazine-bookmark" type="button" data-magazine-save="{h(article["slug"])}" aria-pressed="false" aria-label="حفظ المقال على هذا الجهاز">☆</button>
    </article>'''

def article_video_link(video):
    return f'<a href="https://www.youtube.com/watch?v={video["id"]}" rel="noopener noreferrer" target="_blank">المقطع الرسمي على يوتيوب ↗</a>'

def article_head(article, full_url):
    url = full_url("/articles/" + article["slug"] + "/")
    image = full_url(cover(article))
    graph = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article["title"],
        "description": article["excerpt"],
        "inLanguage": "ar",
        "dateModified": "2026-11-11",
        "author": {"@type": "Organization", "name": "مجرة الفرسان"},
        "publisher": {"@type": "Organization", "name": "مجرة الفرسان"},
        "isAccessibleForFree": True,
        "image": image if image else "/assets/article-story.svg"
    }
    if url: graph["mainEntityOfPage"] = url
    structured = json.dumps(graph, ensure_ascii=False).replace("</","<\\/")
    return f'''<meta property="og:image" content="{h(image)}"><meta property="og:image:alt" content="{h(article["title"])}"><meta property="article:modified_time" content="2026-11-11">
<script type="application/ld+json">{structured}</script>
<script defer src="/assets/magazine.js?v=1"></script>'''

def build_magazine(render, full_url, root):
    data = json.loads((Path(root) / "articles_data.json").read_text(encoding="utf-8"))
    articles = data["articles"]
    byslug = {a["slug"]: a for a in articles}
    assert len(byslug) == len(articles), "Duplicate article slug"
    for a in articles:
        assert a["slug"] in GROUPS
        assert (Path(root) / cover(a).lstrip("/")).exists(), cover(a)
        for r in a.get("related", []):
            assert r in byslug, f"Unknown related article {r}"
    featured = next(a for a in articles if a["featured"])
    hero = f'''<section class="magazine-lead" aria-label="موضوع المجلة الرئيسي">
       <div class="magazine-lead-image"><img src="/assets/galaxy-hero-desktop-v2.webp" alt="مشهد فني كوني يضم أبطال كرة القدم أمام ملعب في الفضاء" fetchpriority="high" width="1200" height="430"></div>
       <div class="magazine-lead-content"><span class="magazine-eyebrow">✦ مجلة مجرة الفرسان — محتوى عربي أصلي</span>
         <h2>كل مباراة حكاية… وكل بطل يستحق أن نعرف قصته</h2>
         <p>تعمّق في عالم فرسان المجرة: أدلة ومقالات تحليلية، صور أصلية، فيديوهات رسمية مختارة، وطرق ممتعة لمتابعة 43 حلقة.</p>
         <div class="magazine-lead-actions"><a class="btn primary" href="/articles/{featured["slug"]}/">اقرأ قصة فرسان المجرة ←</a><a class="btn secondary" href="/quiz/">اختبر معلوماتك 🎮</a></div>
         <div class="magazine-stats"><span>📚 {len(articles)} مقالًا مفصلًا</span><span>▶ مقاطع رسمية مختارة</span><span>🌌 دليل عربي لعالم المسلسل</span></div>
       </div>
    </section>'''
    filters = ''.join(f'<button type="button" class="magazine-filter {"active" if i==0 else ""}" data-magazine-filter="{h(g)}" aria-pressed="{"true" if i==0 else "false"}">{h(g)}</button>' for i,g in enumerate(FILTERS))
    cards = "".join(magazine_card(a) for a in articles)
    videos = [a for a in articles if a.get("video")]
    selected_videos = "".join(video_card(a["video"],cover(a),a["excerpt"],True) for a in videos)
    spotlight = [a for a in articles if a["slug"] in {"bayan-leadership","hayyan-spotlight","nidal-spotlight"}]
    spotlight_links = "".join(f'<a href="/articles/{a["slug"]}/" class="magazine-spotlight-link"><img src="{cover(a)}" loading="lazy" width="250" height="140" alt="فن أصلي يعبّر عن شخصية {h(a["title"])}"><span>{h(a["title"])}</span><b>اقرأ المزيد ←</b></a>' for a in spotlight)
    home = f'''<div class="magazine-index">
      {hero}
      <section class="magazine-section" aria-labelledby="magazine-latest-heading">
        <div class="magazine-section-heading"><div><span class="magazine-eyebrow">⟡ اكتشف عالم المغامرات</span><h2 id="magazine-latest-heading">مقالات تستحق القراءة</h2><p>من بداية الرحلة إلى اللحظات الحاسمة: اختر الموضوع الذي يثير فضولك.</p></div><span class="magazine-counter">{len(articles)} موضوعًا</span></div>
        <div class="magazine-toolbar"><label class="magazine-search-label" for="magazine-search">🔎 <input type="search" id="magazine-search" placeholder="ابحث عن قصة، شخصية، حلقة، كوكب…" autocomplete="off"></label><button type="button" id="magazine-saved-only" class="magazine-filter magazine-saved-filter" aria-pressed="false">☆ المحفوظة</button></div>
        <div class="magazine-filters" role="group" aria-label="تصفية موضوعات المجلة">{filters}</div>
        <div class="magazine-grid" id="magazine-grid">{cards}</div>
        <p class="magazine-no-results" id="magazine-no-results" hidden>لم نجد مقالًا مطابقًا. جرب كلمة أخرى أو غيّر التصنيف.</p>
      </section>
      <section class="magazine-section" aria-label="مقاطع من القناة الرسمية">
        <div class="magazine-section-heading"><div><span class="magazine-eyebrow">▶ من قناة سبيستون غو</span><h2>لقطات رسمية من فرسان المجرة</h2><p>شاهد لحظات حيان ونضال عبر مشغل يوتيوب بعد اختيارك، أو افتحها على القناة الموثّقة.</p></div></div>
        <div class="magazine-video-grid">{selected_videos}</div>
        <p class="magazine-editor-note">تنويه: الفيديوهات من قناة سبيستون غو الموثّقة؛ الموقع غير تابع لسبيستون ولا يعيد رفع المقاطع. تشغيل يوتيوب اختياري وقد لا يكون متاحًا في بعض المناطق.</p>
      </section>
      <section class="magazine-section" aria-label="قراءات عن الأبطال"><div class="magazine-section-heading"><div><span class="magazine-eyebrow">⭐ شخصيات نحبها</span><h2>تعرّف أكثر على أبطال الفريق</h2></div></div>
        <div class="magazine-spotlights">{spotlight_links}</div>
      </section>
      <section class="magazine-last-cta"><span>⚽</span><div><h2>هل انتهيت من القراءة؟</h2><p>جرّب تحديات من 104 أسئلة، أو سجل الحلقات التي شاهدتها كي تواصل رحلة المجرة.</p></div><div class="magazine-last-actions"><a href="/quiz/" class="btn primary">ابدأ التحدي</a><a href="/episodes/" class="btn secondary">دليل الحلقات</a></div></section>
    </div>'''
    render("/articles/","مقالات أبطال الكرة فرسان المجرة | مجلة عربية مصوّرة",
           "مقالات فرسان المجرة: قصة بيان وحيان وعقاب، دليل الحلقات الـ43، تحليل الشخصيات والمهارات، وصلة بمقاطع سبيستون غو الرسمية.",home,
           head='<script defer src="/assets/magazine.js?v=1"></script>')

    # Each article has a real introduction, visual cover, several substantive sections, related reading and an optional official clip.
    for a in articles:
        n = len(a["sections"])
        category = GROUPS[a["slug"]]
        toc = "".join(f'<li><a href="#mag-chapter-{i}">{h(title)}</a></li>' for i,(title,_) in enumerate(a["sections"],1))
        sections = []
        for i,(title,paragraph) in enumerate(a["sections"],1):
            sections.append(f'''<section class="magazine-chapter" id="mag-chapter-{i}">
            <span class="magazine-chapter-index">{i:02d}</span><h2>{h(title)}</h2><p>{h(paragraph)}</p></section>''')
            if i == 2 and len(a["sections"])>=4:
                # An original visual break improves scannability on long articles.
                second = cover(byslug[a["related"][0]]) if a.get("related") else "/assets/article-story.svg"
                sections.append(f'<figure class="magazine-figure"><img src="{second}" loading="lazy" width="1040" height="600" alt="رسم توضيحي أصلي متعلق بعالم فرسان المجرة"><figcaption>رسمة توضيحية خاصة بمجرة الفرسان — يمكن متابعة المواضيع المرتبطة من أسفل الصفحة.</figcaption></figure>')
        related_cards = "".join(f'<a class="magazine-related-card" href="/articles/{r}/"><img src="{cover(byslug[r])}" loading="lazy" width="250" height="140" alt="رسم خاص بالمقال"><span>{h(byslug[r]["title"])}</span></a>' for r in a["related"])
        video = video_card(a["video"],cover(a),"مقطع رسمي من قناة سبيستون غو؛ لا يبدأ التحميل حتى تختار تشغيل.",False) if a.get("video") else ""
        faq = f'''<details class="magazine-more-fact"><summary>💡 معلومة إضافية عن هذا الموضوع</summary><p>{h(a["fact"])}</p></details>'''
        cover_caption = f'لوحة فنية أصلية خاصة بموضوع «{h(a["title"])}»'
        detail = f'''<div class="magazine-reading-progress" aria-hidden="true"><div id="magazine-progress-fill"></div></div>
        <article class="magazine-detail" data-magazine-article="{h(a["slug"])}">
          <div class="magazine-detail-cover"><img src="{cover(a)}" width="1200" height="680" alt="{cover_caption}" fetchpriority="high">
            <div class="magazine-cover-label"><span class="magazine-category {CATEGORY_COLORS.get(category, 'cyan')}">{h(category)}</span><span>📖 {minutes(a)} دقائق قراءة</span><span>تحديث: 11 نوفمبر 2026</span></div>
          </div>
          <div class="magazine-detail-actions"><span>✦ مقال عربي مستقل لعشّاق أبطال الكرة: فرسان المجرة</span><button type="button" class="magazine-save-detail" data-magazine-save="{h(a["slug"])}" aria-pressed="false">☆ احفظ المقال للعودة إليه</button></div>
          <p class="magazine-article-intro">{h(a["lead"])}</p>
          <div class="magazine-detail-columns">
            <div class="magazine-detail-reading"><div class="magazine-mobile-toc"><details><summary>📑 فهرس المقال — {n} محاور</summary><ol>{toc}</ol></details></div>
              {''.join(sections)}
              {faq}
              {video}
              <aside class="magazine-safe-note"><strong>ملاحظة للقراء:</strong> هذا تحليل تحريري من موقع معجبين مستقل، وليس نصًا رسميًا من منتجي المسلسل. المشاهد واللقطات المتاحة على القنوات الرسمية تخضع لشروط أصحاب الحقوق.</aside>
              <div class="magazine-article-followup"><h2>واصل رحلتك في المجرة</h2><p>قد تعجبك هذه المواضيع أيضًا:</p><div class="magazine-related-grid">{related_cards}</div></div>
              <div class="magazine-article-end-cta"><a href="/articles/" class="btn secondary">جميع المقالات ←</a><a href="/quiz/" class="btn primary">اختبر معلوماتك 🎮</a></div>
            </div>
            <aside class="magazine-detail-aside" aria-label="فهرس ومواضيع أخرى">
              <div class="magazine-toc-box"><h2>في هذا المقال</h2><ol>{toc}</ol><span>⏱ {minutes(a)} دقائق قراءة</span></div>
              <div class="magazine-sidebar-cta"><strong>🌌 تحدي الفرسان</strong><p>اختبر ذاكرتك في أكثر من 100 سؤال عربي مصوّر.</p><a href="/quiz/" class="btn secondary">ابدأ اللعب ←</a></div>
            </aside>
          </div>
        </article>'''
        render("/articles/" + a["slug"] + "/",a["title"],a["excerpt"],detail,head=article_head(a,full_url))
    return len(articles)
