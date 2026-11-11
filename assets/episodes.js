/* Episode catalogue: accessible filtering, local progress, opt-in verified publisher video embeds. */
(()=>{'use strict';
const $=id=>document.getElementById(id);
const dataElement=$('episode-catalog-data');
if(!dataElement)return;
let catalogue;
try{catalogue=JSON.parse(dataElement.textContent);}catch{return;}
if(!Array.isArray(catalogue.episodes)||!Array.isArray(catalogue.videos))return;
const cards=[...document.querySelectorAll('[data-ep-item]')];
const search=$('episode-search-v2');
const filterButtons=[...document.querySelectorAll('[data-ep-stage]')].filter(x=>x.tagName==='BUTTON');
let stage='الكل';
function normalize(str){return String(str||'').toLocaleLowerCase('ar').replace(/[أإآ]/g,'ا').replace(/ى/g,'ي').replace(/ة/g,'ه').replace(/[ًٌٍَُِّْـ]/g,'');}
function updateList(){
 const q=normalize(search?.value.trim()||'');let num=0;
 for(const card of cards){
   const show=(stage==='الكل'||card.dataset.epStage===stage)&&(!q||normalize(card.dataset.epSearch).includes(q));
   card.hidden=!show;if(show)num++;
 }
 $('ep-count-label').textContent=num+' حلقة';
 $('ep-no-results').hidden=num!==0;
}
search?.addEventListener('input',updateList);
for(const button of filterButtons)button.addEventListener('click',()=>{
 stage=button.dataset.epStage;
 for(const candidate of filterButtons){const active=candidate===button;candidate.classList.toggle('active',active);candidate.setAttribute('aria-pressed',String(active));}
 updateList();
});
const validFacebook=url=>{
 try{const u=new URL(url);return u.protocol==='https:'&&['facebook.com','www.facebook.com','web.facebook.com'].includes(u.hostname)&&(/^\/[^?#]*\/videos\//.test(u.pathname)||u.pathname.startsWith('/watch/')||u.pathname.startsWith('/reel/'));}catch{return false;}
};
for(const opener of document.querySelectorAll('[data-ep-open]'))opener.addEventListener('click',()=>{
 const n=Number(opener.dataset.epOpen),e=catalogue.episodes.find(x=>x.number===n);if(!e)return;
 const panel=$('ep-detail');panel.hidden=false;
 $('ep-detail-title').textContent='الحلقة '+n+' — '+e.title;
 $('ep-detail-phase').textContent=e.phase;
 $('ep-detail-image').src=e.art;
 $('ep-detail-image').alt='رسمة أصلية لأجواء الحلقة '+n;
 $('ep-detail-description').textContent='العنوان العربي: «'+e.title+'». تنتمي الحلقة إلى مرحلة '+e.phase+'. يمكنك تسجيل مشاهدتها من القائمة أعلاه.';
 const zone=$('ep-verified-video'),status=$('ep-play-status');
 zone.replaceChildren();zone.hidden=true;status.hidden=false;
 const source=catalogue.videos.find(v=>v.number===n&&validFacebook(v.url));
 if(source){
  status.hidden=true;zone.hidden=false;
  const button=document.createElement('button');
  button.type='button';button.className='btn primary';
  button.textContent='▶ تشغيل الفيديو من صفحة الناشر المعتمدة';
  button.addEventListener('click',()=>{
   const frame=document.createElement('iframe');
   frame.src='https://www.facebook.com/plugins/video.php?href='+encodeURIComponent(source.url)+'&show_text=0&width=640';
   frame.title='مشغل الحلقة '+n+' عبر فيسبوك';
   frame.loading='lazy';
   frame.setAttribute('allowfullscreen','');
   frame.setAttribute('allow','autoplay; encrypted-media; picture-in-picture; web-share');
   frame.referrerPolicy='strict-origin-when-cross-origin';
   frame.style.border='0';
   const iframeWrap=document.createElement('div');iframeWrap.className='ep-facebook-frame';iframeWrap.appendChild(frame);
   const link=document.createElement('a');link.href=source.url;link.target='_blank';link.rel='noopener noreferrer';link.textContent='فتح الفيديو الأصلي على فيسبوك ↗';
   zone.replaceChildren(iframeWrap,link);
  },{once:true});
  zone.appendChild(button);
 }
 panel.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'start'});
});
updateList();
})();