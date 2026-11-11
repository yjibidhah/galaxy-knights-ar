"""Arabic Galaxy Knights episode catalogue. Only embed independently verified official videos."""
from pathlib import Path
from html import escape
import json
from urllib.parse import urlparse

def esc(x):
    return escape(str(x),quote=True)

def verified_video(item):
    url = item.get("facebook_video_url")
    if not url: return None
    if item.get("source_status") != "authorized_verified": return None
    u=urlparse(url)
    if u.scheme != "https" or u.hostname not in {"www.facebook.com","facebook.com","web.facebook.com"}:
        raise ValueError("Video URL must be a verified official Facebook HTTPS link.")
    if not any(part in u.path for part in ("/videos/","/watch/","/reel/")):
        raise ValueError("Video URL must point to a single video post.")
    return url

def build_episodes(root):
    root=Path(root)
    source=json.loads((root/"episodes_data.json").read_text(encoding="utf-8"))
    episodes=source["episodes"]
    assert len(episodes)==43 and [e["number"] for e in episodes]==list(range(1,44))
    assert all((root/e["art"].lstrip("/")).exists() for e in episodes)
    labels=["الكل","بدايات الفريق والبطولة","رحلة الفضاء الأولى","الكواكب والاختبارات","المواجهات الأخيرة"]
    filters=''.join(f'<button class="ep-filter {"active" if i==0 else ""}" type="button" data-ep-stage="{esc(stage)}" aria-pressed="{"true" if i==0 else "false"}">{esc(stage)}</button>' for i,stage in enumerate(labels))
    cards=[]
    for e in episodes:
        verified=verified_video(e)
        cards.append(f'''<article class="ep-card" data-ep-item data-ep-number="{e["number"]}" data-ep-stage="{esc(e["phase"])}" data-ep-search="{esc(str(e["number"])+" "+e["title"]+" "+e["phase"])}">
          <button type="button" class="ep-card-open" data-ep-open="{e["number"]}" aria-label="عرض تفاصيل الحلقة {e["number"]}: {esc(e["title"])}">
            <span class="ep-thumb"><img src="{e["art"]}" width="320" height="190" loading="lazy" alt="رسمة أصلية تمثل أجواء الحلقة {e["number"]}"><span class="ep-number-chip">الحلقة {e["number"]:02d}</span></span>
            <span class="ep-card-info"><span class="ep-stage-name">{esc(e["phase"])}</span><strong>{esc(e["title"])}</strong><span class="ep-open-label">{'مشاهدة متاحة من المصدر الرسمي ▶' if verified else 'عرض تفاصيل الحلقة ←'}</span></span>
          </button>
          <button type="button" class="episode ep-watched-toggle" data-episode="{e["number"]}" aria-pressed="false"><span class="episode-status">لم أشاهدها</span></button>
        </article>''')
    # Only actual authorized video URLs can reach browser-side embed rendering.
    videos=[{"number":e["number"],"url":verified_video(e)} for e in episodes if verified_video(e)]
    player_data=json.dumps({"episodes":[{"number":e["number"],"title":e["title"],"phase":e["phase"],"art":e["art"]} for e in episodes],"videos":videos},ensure_ascii=False).replace("<","\\u003c")
    html=f'''<div class="episode-library">
      <section class="ep-welcome">
        <div class="ep-welcome-copy"><span class="home-eyebrow">⚽ دليل حلقات فرسان المجرة</span><h2>43 مغامرة… رحلة واحدة نحو النجوم!</h2>
        <p>استكشف حلقات أبطال الكرة: فرسان المجرة المدبلجة بالعربية، بالترتيب وبأسمائها العربية. تابع تقدمك في المشاهدة، واختر مرحلة للتعرّف على أحداث الرحلة.</p>
        <div class="ep-welcome-stats"><span>🎬 <strong>43</strong> حلقة عربية</span><span>🪐 <strong>4</strong> مراحل</span><span>✓ تقدّم محفوظ على جهازك</span></div></div>
        <img src="/assets/article-episodes.svg" width="570" height="350" alt="رسم زخرفي أصلي مستوحى من دليل الحلقات">
      </section>
      <section class="ep-progress-panel" aria-label="تقدم مشاهدة الحلقات">
        <div><h2>رحلتك حتى الآن: <span id="watched-count">0</span> / 43</h2><p>انقر «شاهدتها» عند الانتهاء من أي حلقة؛ تحفظ المتابعة محليًا على هذا الجهاز فقط.</p>
        <div class="ep-progress-track"><div class="progress-track" id="watch-progress" role="progressbar" aria-label="نسبة مشاهدة الحلقات" aria-valuemin="0" aria-valuemax="43" aria-valuenow="0"><div class="progress-bar"></div></div></div></div>
        <button id="reset-watch" type="button" class="btn secondary">إعادة ضبط التقدم</button>
      </section>
      <div class="ep-legality"><strong>عن مشاهدة الحلقات:</strong> تظهر روابط تشغيل الحلقات الكاملة فقط عندما نتحقق من أن الناشر مخوّل بإتاحتها وأن الفيديو العام يقبل التضمين. لم نتحقق بعد من رابط رسمي كامل لكل حلقة على فيسبوك؛ لذلك هذه القائمة دليل للحلقات وليست مكتبة بث. وقد يطلب فيسبوك تسجيل الدخول لبعض الفيديوهات.</div>
      <section class="ep-browse" aria-labelledby="ep-browser-title">
        <div class="ep-section-head"><h2 id="ep-browser-title">اختر حلقتك</h2><p>تصفح العناوين أو ابحث برقم الحلقة أو باسمها</p></div>
        <div class="ep-search-toolbar"><label for="episode-search-v2">🔎 <input id="episode-search-v2" type="search" placeholder="مثلاً: الحلقة 25 أو قصة ضياء" autocomplete="off"></label><span id="ep-count-label" aria-live="polite">43 حلقة</span></div>
        <div class="ep-filters" role="group" aria-label="تصفية الحلقات">{filters}</div>
        <div class="ep-grid" id="ep-grid">{''.join(cards)}</div>
        <p id="ep-no-results" class="ep-no-results" hidden>لم نعثر على حلقة بهذا الاسم أو الرقم.</p>
      </section>
      <section class="ep-detail" id="ep-detail" aria-labelledby="ep-detail-title" hidden>
        <div class="ep-detail-cover"><img id="ep-detail-image" src="/assets/article-episodes.svg" width="540" height="310" alt="رسمة أصلية للحلقة"></div>
        <div class="ep-detail-copy"><span id="ep-detail-phase" class="ep-stage-name">رحلة الأبطال</span><h2 id="ep-detail-title">تفاصيل الحلقة</h2>
        <p id="ep-detail-description">تابع تفاصيل الحلقة المدبلجة بالعربية، ثم سجّل مشاهدتها بعد الانتهاء منها.</p>
        <div id="ep-verified-video" class="ep-verified-video" hidden></div>
        <p id="ep-play-status" class="ep-play-status">لا يتوفر بعد فيديو كامل من ناشر مخوّل تم التحقق منه لهذه الحلقة.</p>
        <a href="/articles/watch-order/" class="btn secondary">دليل ترتيب مشاهدة الحلقات ←</a></div>
      </section>
      <script type="application/json" id="episode-catalog-data">{player_data}</script>
    </div>'''
    head='<script defer src="/assets/episodes.js?v=20261111"></script>'
    return html,head
