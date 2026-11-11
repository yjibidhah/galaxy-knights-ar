"""Build the playful, accessible Arabic homepage from existing published content."""
from pathlib import Path
from html import escape
import json

def h(value):
    return escape(str(value), quote=True)

def build_home_sections(root):
    root = Path(root)
    chars = {x["slug"]: x for x in json.loads((root/"characters_data.json").read_text(encoding="utf-8"))["characters"]}
    articles = {a["slug"]: a for a in json.loads((root/"articles_data.json").read_text(encoding="utf-8"))["articles"]}
    raw = (root/"assets/quiz-data.js").read_text(encoding="utf-8")
    quiz = json.loads(raw.split("window.GALAXY_QUIZ_BANK = ",1)[1].rsplit(";",1)[0])
    quiz_count = len(quiz["questions"])
    episodes = 43
    mini_questions = [
        {"question":"كم عدد حلقات أبطال الكرة: فرسان المجرة المدبلجة بالعربية؟","options":["26 حلقة","43 حلقة","52 حلقة","13 حلقة"],"answer":1,"explanation":"عدد حلقات فرسان المجرة بالعربية هو 43 حلقة.","image":"/assets/article-episodes.svg"},
        {"question":"من القائد الذي يشجع أعضاء الفريق على المحاولة والعمل معًا؟","options":["بيان","عقاب","نضال","براء"],"answer":0,"explanation":"بيان يقود الأبطال بحماسه وثقته في زملائه.","image":"/assets/article-bayan-leadership.svg"},
        {"question":"من صانع الألعاب الذي يحب التفكير في تحركات الفريق قبل التمرير؟","options":["براء","ضياء","حيان","ورقة"],"answer":2,"explanation":"حيان يبرز في تنظيم الهجمات وقراءة تحركات الملعب.","image":"/assets/article-hayyan-spotlight.svg"},
    ]
    for q in mini_questions:
        assert (root / q["image"].lstrip("/")).exists()
        assert len(q["options"]) == 4 and len(set(q["options"])) == 4
    quiz_json = json.dumps(mini_questions,ensure_ascii=False).replace("<","\\u003c")

    shortcuts=[
       ("🎮","اختبر معرفتك","أسئلة عربية مصوّرة وتحديات بمستويات مختلفة.","/quiz/","/assets/quiz-cosmos.svg",f"{quiz_count} سؤالًا"),
       ("🎬","رحلة الحلقات","تابع مغامرة الأبطال من الحلقة الأولى إلى الأخيرة.","/episodes/","/assets/article-episodes.svg","43 حلقة"),
       ("👥","أبطال المجرة","صور ومعلومات وشخصيات الدبلجة العربية.","/characters/","/assets/article-characters.svg",f"{len(chars)} شخصية"),
       ("📚","مجلة الفرسان","قصص وشروحات ومواضيع ستجعلك تفهم الأحداث أكثر.","/articles/","/assets/article-story.svg",f"{len(articles)} مقالًا"),
       ("🌌","الكواكب والفرق","تعرّف إلى محطات الرحلة والخصوم الجدد.","/articles/galaxy-worlds/","/assets/article-galaxy-worlds.svg","دليل الكواكب"),
       ("⚡","القوى والمهارات","افهم أساليب اللاعبين والقدرات الخيالية.","/articles/powers/","/assets/article-powers.svg","دليل المهارات"),
    ]
    shortcut_html="".join(f'''<a class="home-world-card" href="{url}">
          <div class="home-world-image"><img src="{image}" loading="lazy" width="480" height="260" alt="رسمة أصلية خاصة بعالم {h(title)}"></div>
          <div class="home-world-copy"><span class="home-world-badge">{h(badge)}</span><h3>{icon} {h(title)}</h3><p>{h(desc)}</p><span class="home-world-action">انطلق للاستكشاف ←</span></div>
        </a>''' for icon,title,desc,url,image,badge in shortcuts)
    featured = []
    for slug in ("bayan","hayyan","oqab"):
        c=chars[slug]
        featured.append(f'''<a class="home-character-card" href="/characters/{slug}/">
          <div class="home-character-picture">
            <img src="{h(c["portrait"])}" referrerpolicy="no-referrer" decoding="async" loading="lazy" width="340" height="330" alt="صورة شخصية {h(c["name"])}"
            onerror="this.onerror=null;this.src='/assets/portrait-fallback.svg';this.classList.add('home-character-fallback')">
          </div>
          <div class="home-character-info"><span class="home-character-role">{h(c["position"].split(" · ")[0])}</span><h3>{h(c["name"])}</h3><p>{h(c["intro"].split("؛")[0][:105])}</p><span>اكتشف قصته ←</span></div>
        </a>''')
    article_cards=[]
    for slug in ("story","team-guide","hayyan-spotlight"):
        a=articles[slug]
        article_cards.append(f'''<a class="home-editor-card" href="/articles/{slug}/">
          <img src="/assets/article-{slug}.svg" loading="lazy" width="490" height="295" alt="رسمة أصلية لموضوع {h(a["title"])}">
          <div><span>✦ مقال عربي</span><h3>{h(a["title"])}</h3><p>{h(a["excerpt"])}</p><b>اقرأ المقال ←</b></div>
        </a>''')
    from magazine import video_card
    videos=[]
    for slug in ("hayyan-spotlight","nidal-spotlight"):
        a=articles[slug]
        assert a.get("video"),slug
        videos.append(video_card(a["video"],f"/assets/article-{slug}.svg",a["excerpt"],compact=True))
    body=f'''<div class="home-portal">
        <div class="home-portal-topline shell">
          <span>🌌 بوابتك إلى عالم فرسان المجرة</span><span>مساحة عربية مستقلة لمحبي أبطال الكرة</span>
        </div>
        <div class="shell">
          <nav class="home-quicklinks" aria-label="اختصارات سريعة">
            <a href="#home-worlds">🪐 اكتشف العالم</a><a href="#home-mini-quiz">⚡ سؤال سريع</a><a href="#home-characters">⭐ الأبطال</a><a href="#home-videos">▶ فيديوهات سبيستون</a>
          </nav>
          <section class="home-section home-intro-section" id="home-worlds" aria-labelledby="home-worlds-title">
            <div class="home-heading"><div><span class="home-eyebrow">🎯 اختر وجهتك</span><h2 id="home-worlds-title">ستة عوالم في انتظارك</h2><p>ماذا تريد أن تفعل اليوم؟ لكل بطل مغامرته الخاصة، وأنت تختار الطريق!</p></div><span class="home-section-stamp">✦ عالم مليء بالمغامرات</span></div>
            <div class="home-world-grid">{shortcut_html}</div>
          </section>
          <section class="home-section home-mission-section" aria-labelledby="home-mission-title">
            <div class="home-mission-visual" aria-hidden="true"><img src="/assets/article-galaxy-worlds.svg" loading="lazy" width="520" height="460" alt=""></div>
            <div class="home-mission-content"><span class="home-eyebrow">🎮 حدد نوع مغامرتك</span><h2 id="home-mission-title">أي نوع من أبطال المجرة أنت اليوم؟</h2><p>اختر ما تحب، وسنقترح لك مكانًا مناسبًا تبدأ منه. يمكنك تغيير اختيارك في أي وقت.</p>
              <div class="home-mission-options" role="group" aria-label="اختر مغامرتك">
                <button type="button" class="home-mission-tab active" data-home-mission="watcher" aria-pressed="true">🎬 محب الحلقات</button>
                <button type="button" class="home-mission-tab" data-home-mission="expert" aria-pressed="false">🏆 خبير الأبطال</button>
                <button type="button" class="home-mission-tab" data-home-mission="explorer" aria-pressed="false">🪐 مستكشف الكواكب</button>
              </div>
              <div class="home-mission-result" id="home-mission-result" aria-live="polite"><strong id="home-mission-label">ابدأ رحلة الحلقات</strong><p id="home-mission-description">تابع الحلقات الـ43 واحتفظ بما شاهدته على جهازك.</p><a id="home-mission-link" class="btn primary" href="/episodes/">انطلق الآن ←</a></div>
            </div>
          </section>
          <section class="home-section home-mini-section" id="home-mini-quiz" aria-labelledby="home-mini-title">
            <div class="home-heading"><div><span class="home-eyebrow">⚡ تحدٍ قصير</span><h2 id="home-mini-title">ثلاثة أسئلة… هل تعرف الإجابة؟</h2><p>العب تحديًا سريعًا دون توقيت أو تسجيل، واكتشف معلومة بعد كل إجابة.</p></div><a class="home-text-link" href="/quiz/">كل تحديات الفرسان ←</a></div>
            <div class="home-mini-layout" id="home-mini-area">
               <div class="home-mini-art"><img id="home-mini-image" src="/assets/article-episodes.svg" width="650" height="440" loading="lazy" alt="رسمة توضيحية للسؤال الحالي"><span class="home-mini-visual-caption">🏅 تدريب الفرسان</span></div>
               <div class="home-mini-play">
                 <div class="home-mini-top"><span id="home-mini-count">السؤال 1 من 3</span><strong id="home-mini-score">⭐ 0 نقاط</strong></div>
                 <div class="home-mini-progress" role="progressbar" aria-label="تقدم التحدي" aria-valuemin="0" aria-valuemax="3" aria-valuenow="0" id="home-mini-progress"><span id="home-mini-progress-fill"></span></div>
                 <h3 id="home-mini-question">{h(mini_questions[0]["question"])}</h3>
                 <div id="home-mini-options" class="home-mini-options" role="group" aria-label="إجابات التحدي">
                  {''.join(f'<button type="button" data-home-answer="{i}">{h(v)}</button>' for i,v in enumerate(mini_questions[0]["options"]))}
                 </div>
                 <p id="home-mini-feedback" class="home-mini-feedback" role="status" aria-live="polite" hidden></p>
                 <button type="button" id="home-mini-next" class="btn primary home-mini-next" hidden>السؤال التالي ←</button>
                 <div id="home-mini-finish" class="home-mini-finish" hidden><strong id="home-mini-final-score"></strong><p>أحسنت! يمكنك تجربة المزيد من الأسئلة في مركز التحديات.</p><div><button id="home-mini-restart" class="btn secondary" type="button">🔁 العب مجددًا</button><a href="/quiz/" class="btn primary">ابدأ التحدي الكبير ←</a></div></div>
               </div>
            </div>
          </section>
          <section class="home-section home-progress-section" aria-labelledby="home-progress-title">
             <div class="home-watch-card">
                <div><span class="home-eyebrow">🎬 دليل حلقاتك</span><h2 id="home-progress-title">أين وصلت في مغامرة المجرة؟</h2>
                  <p id="home-watch-message">تابع مشاهدتك من حيث توقفت. هذه المعلومات تُحفظ على جهازك فقط.</p>
                  <div class="home-watch-stats"><strong><span id="home-watched-number">0</span> / 43</strong><span id="home-watch-percent">0% مكتمل</span></div>
                  <div class="home-watch-track" role="progressbar" aria-label="تقدم مشاهدة الحلقات" aria-valuemin="0" aria-valuemax="43" aria-valuenow="0" id="home-watch-track"><span id="home-watch-fill"></span></div>
                  <a href="/episodes/" class="btn primary" id="home-watch-cta">ابدأ مشاهدة الحلقات ←</a>
                  <p class="home-small-privacy">لا حسابات، ولا مشاركة علنية لنتائجك أو تقدمك.</p>
                </div>
                <img src="/assets/article-episodes.svg" loading="lazy" width="470" height="300" alt="رسم أصلي لدليل الحلقات"/>
             </div>
          </section>
          <section class="home-section" id="home-characters" aria-labelledby="home-characters-title">
            <div class="home-heading"><div><span class="home-eyebrow">⭐ تعرّف إلى فريقك</span><h2 id="home-characters-title">ثلاثة أبطال… وحكايات لا تُنسى</h2><p>بيان، حيان، وعقاب. اختر بطلًا لتكتشف قصته ومهاراته في الدبلجة العربية.</p></div><a href="/characters/" class="home-text-link">جميع الشخصيات ←</a></div>
            <div class="home-characters-grid">{''.join(featured)}</div>
          </section>
          <section class="home-section" aria-labelledby="home-read-title">
            <div class="home-heading"><div><span class="home-eyebrow">📚 من مجلة الفرسان</span><h2 id="home-read-title">قصص ومقالات تستحق الاكتشاف</h2><p>اقرأ عن المغامرة، وروح الفريق، واللحظات التي تجعل كل لاعب مميزًا.</p></div><a href="/articles/" class="home-text-link">جميع المقالات ←</a></div>
            <div class="home-editor-grid">{''.join(article_cards)}</div>
          </section>
          <section class="home-section" id="home-videos" aria-labelledby="home-videos-title">
            <div class="home-heading"><div><span class="home-eyebrow">▶ من سبيستون غو</span><h2 id="home-videos-title">شاهد لحظات من فرسان المجرة</h2><p>مقاطع رسمية من يوتيوب تشاهدها باختيارك. لا يبدأ التحميل قبل الضغط على تشغيل.</p></div></div>
            <div class="home-video-grid">{''.join(videos)}</div>
            <p class="home-video-disclaimer">مقاطع منشورة على القناة الرسمية؛ الموقع مستقل وغير تابع لسبيستون. تتوفر روابط لفتح الفيديوهات على يوتيوب إذا تعذّر تشغيلها هنا.</p>
          </section>
          <section class="home-section home-help" aria-labelledby="home-help-title">
             <div class="home-heading"><div><span class="home-eyebrow">💡 هل تعلم؟</span><h2 id="home-help-title">أجوبة سريعة للفرسان الجدد</h2></div></div>
             <div class="home-faq">
               <details><summary>كم عدد حلقات أبطال الكرة: فرسان المجرة؟</summary><p>تتكون الدبلجة العربية من 43 حلقة. يمكنك فتح <a href="/episodes/">دليل الحلقات</a> وتسجيل ما شاهدته.</p></details>
               <details><summary>هل يمكن لعب التحديات دون حساب؟</summary><p>نعم، الأسئلة متاحة دون حساب أو اسم أو بريد إلكتروني. تُحفظ بعض النتائج والتقدم محليًا في متصفحك فقط.</p></details>
               <details><summary>هل مجرة الفرسان موقع رسمي لسبيستون؟</summary><p>لا، نحن موقع معجبين مستقل. المقاطع المشار إليها من قنوات الناشرين الرسمية على يوتيوب، ولا نرفع الحلقات أو نوزع نسخًا غير مرخصة.</p></details>
             </div>
          </section>
          <div class="home-bottom-cta"><div><span>⚽ جاهز لرحلة جديدة؟</span><h2>اختر مغامرتك وابدأ!</h2><p>كل لاعب له طريقته في الفوز. اكتشف عالم فرسان المجرة بأمان ومتعة.</p></div><a class="btn primary" href="/quiz/">اختبر معلوماتك الآن ✨</a></div>
        </div>
      </div>
      <script id="home-mini-bank" type="application/json">{quiz_json}</script>'''
    head = '<script defer src="/assets/home.js?v=home-portal-20261111"></script><script defer src="/assets/magazine.js?v=1"></script>'
    return body,head

