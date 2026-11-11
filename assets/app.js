(()=>{'use strict';
const $=(q,root=document)=>root.querySelector(q), $$=(q,root=document)=>[...root.querySelectorAll(q)];
const menu=$('#menu-btn'),nav=$('#main-nav');
if(menu&&nav){menu.addEventListener('click',()=>{const open=nav.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));});}
const safeRead=(k,defaultValue)=>{try{return JSON.parse(localStorage.getItem(k))??defaultValue}catch{return defaultValue}};
const safeSave=(k,v)=>{try{localStorage.setItem(k,JSON.stringify(v))}catch{}};
const episodeButtons=$$('[data-episode]');
let watched=new Set(safeRead('galaxy-watched-v1',[]).filter(n=>Number.isInteger(n)&&n>=1&&n<=43));
function updateEpisodes(){
episodeButtons.forEach(b=>{const n=Number(b.dataset.episode),done=watched.has(n);b.classList.toggle('done',done);b.setAttribute('aria-pressed',String(done));$('.episode-status',b).textContent=done?'✓ شاهدتها':'لم أشاهدها';});
const count=$('#watched-count'),bar=$('#watch-progress');if(count)count.textContent=String(watched.size);if(bar){const fill=$('.progress-bar',bar);if(fill)fill.style.width=(watched.size/43*100)+'%';bar.setAttribute('aria-valuenow',String(watched.size));}
}
if(episodeButtons.length){
episodeButtons.forEach(b=>b.addEventListener('click',()=>{const n=Number(b.dataset.episode);watched.has(n)?watched.delete(n):watched.add(n);safeSave('galaxy-watched-v1',[...watched].sort((a,b)=>a-b));updateEpisodes();}));
const reset=$('#reset-watch');if(reset)reset.addEventListener('click',()=>{if(confirm('هل تريد مسح تقدم المشاهدة المحفوظ على هذا الجهاز فقط؟')){watched.clear();safeSave('galaxy-watched-v1',[]);updateEpisodes();}});
updateEpisodes();
}
const filter=$('#episode-filter');if(filter)filter.addEventListener('input',()=>{const q=filter.value.trim().replace(/[٠-٩]/g,x=>'٠١٢٣٤٥٦٧٨٩'.indexOf(x)).replace(/[۰-۹]/g,x=>'۰۱۲۳۴۵۶۷۸۹'.indexOf(x));episodeButtons.forEach(b=>{b.hidden=!!q&&!String(b.dataset.episode).includes(q);});});
// The illustrated quiz arcade has its own script, loaded only on /quiz/.
const searchable=$$('[data-search]'),search=$('#search-site'),charFilters=$$('[data-char-filter]');
let selectedCharacterGroup='all';
function applySiteSearch(){
  if(!search)return;
  const q=search.value.trim().toLocaleLowerCase('ar');
  let visible=0;
  searchable.forEach(el=>{
    const matchText=(el.textContent+' '+(el.getAttribute('aria-label')||'')).toLocaleLowerCase('ar').includes(q);
    const group=el.dataset.characterGroup;
    const matchGroup=!group||selectedCharacterGroup==='all'||group===selectedCharacterGroup;
    const show=matchText&&matchGroup;
    el.hidden=!show;
    if(show)visible++;
  });
  const message=$('#search-empty');if(message)message.hidden=visible!==0;
}
if(search)search.addEventListener('input',applySiteSearch);
charFilters.forEach(button=>button.addEventListener('click',()=>{
  selectedCharacterGroup=button.dataset.charFilter;
  charFilters.forEach(b=>{
    const active=b===button;
    b.classList.toggle('active',active);
    b.setAttribute('aria-pressed',String(active));
  });
  applySiteSearch();
}));
})();