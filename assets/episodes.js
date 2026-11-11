/* Galaxy Knights episode catalogue: opt-in Facebook player, no rehosting or login bypass. */
(()=>{'use strict';
const $=id=>document.getElementById(id);
const dataElement=$('episode-catalog-data');
if(!dataElement)return;
let catalogue;
try{catalogue=JSON.parse(dataElement.textContent);}catch{return;}
if(!Array.isArray(catalogue.episodes)||!Array.isArray(catalogue.videos)||!Array.isArray(catalogue.externalPosts))return;
const cards=[...document.querySelectorAll('[data-ep-item]')];
const search=$('episode-search-v2');
const filterButtons=[...document.querySelectorAll('button[data-ep-stage]')];
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
 for(const candidate of filterButtons){
   const active=candidate===button;
   candidate.classList.toggle('active',active);
   candidate.setAttribute('aria-pressed',String(active));
 }
 updateList();
});
function validFacebook(url){
 try{
   const u=new URL(url);
   return u.protocol==='https:'&&['facebook.com','www.facebook.com','web.facebook.com'].includes(u.hostname)&&
     (/^\/[^?#]*\/videos\//.test(u.pathname)||u.pathname.startsWith('/watch/')||u.pathname.startsWith('/reel/'));
 }catch{return false;}
}
function createPlayer(url,n){
 const frame=document.createElement('iframe');
 frame.src='https://www.facebook.com/plugins/video.php?href='+encodeURIComponent(url)+'&show_text=false&width=640&autoplay=false&allowfullscreen=true';
 frame.title='مشغّل فيديو فيسبوك المضمن للحلقة '+n;
 frame.loading='lazy';
 frame.setAttribute('allowfullscreen','');
 frame.setAttribute('allow','autoplay; encrypted-media; picture-in-picture; web-share');
 frame.referrerPolicy='strict-origin-when-cross-origin';
 frame.setAttribute('scrolling','no');
 frame.style.border='0';
 return frame;
}
const panel=$('ep-detail'),zone=$('ep-verified-video'),status=$('ep-play-status'),notes=$('ep-external-post');
for(const opener of document.querySelectorAll('[data-ep-open]'))opener.addEventListener('click',()=>{
 const n=Number(opener.dataset.epOpen);
 const episode=catalogue.episodes.find(e=>e.number===n);
 if(!episode)return;
 // Always unload the previous player before opening another episode.
 zone.replaceChildren();
 zone.hidden=true;
 notes.replaceChildren();
 notes.hidden=true;
 panel.hidden=false;
 $('ep-detail-title').textContent='الحلقة '+n+' — '+episode.title;
 $('ep-detail-phase').textContent=episode.phase;
 $('ep-detail-image').src=episode.art;
 $('ep-detail-image').alt='رسمة أصلية لأجواء الحلقة '+n;
 $('ep-detail-description').textContent='العنوان العربي: «'+episode.title+'». تنتمي الحلقة إلى مرحلة '+episode.phase+'. يمكنك تسجيل مشاهدتها من القائمة بعد إكمالها.';
 const official=catalogue.videos.find(v=>v.number===n&&validFacebook(v.url));
 const submitted=catalogue.externalPosts.find(v=>v.number===n&&validFacebook(v.url));
 const source=official||submitted;
 if(source){
   status.hidden=true;
   zone.hidden=false;
   const label=document.createElement('div');
   label.className='ep-player-heading';
   label.textContent='▶ شاهد الحلقة '+n+' هنا عبر مشغّل فيسبوك';
   const wrap=document.createElement('div');
   wrap.className='ep-facebook-frame';
   wrap.appendChild(createPlayer(source.url,n));
   const help=document.createElement('p');
   help.className='ep-player-help';
   help.textContent='يعمل الفيديو داخل هذه الصفحة إذا سمحت إعدادات فيسبوك بعرضه. قد تظهر رسالة تسجيل دخول أو عدم توفر الفيديو حسب الحساب والمنطقة وإعدادات الناشر.';
   const close=document.createElement('button');
   close.type='button';
   close.className='ep-player-stop';
   close.textContent='■ إيقاف الفيديو وإغلاق المشغّل';
   close.addEventListener('click',()=>{
      wrap.replaceChildren();
      zone.hidden=true;
      close.hidden=true;
   });
   zone.append(label,wrap,help,close);
   if(submitted&&!official){
      const note=document.createElement('p');
      note.textContent='المصدر: صفحة Old But Cold (منشور شاركه أحد المتابعين). لم يتم التحقق من حقوق نشر الحلقة لدى الصفحة؛ يستخدم الموقع مشغّل فيسبوك فقط ولا يستضيف نسخة من الفيديو.';
      notes.appendChild(note);
      notes.hidden=false;
   }
 }else{
   status.hidden=false;
   status.textContent='لا يتوفر حاليًا فيديو قابل للتضمين لهذه الحلقة. يمكنك متابعة دليل الحلقات وتسجيل ما شاهدته.';
 }
 panel.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'start'});
});
updateList();
})();