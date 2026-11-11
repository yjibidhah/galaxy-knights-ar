/* Galaxy Knights original magazine: search, filters, bookmarks and opt-in official videos. */
(() => {
'use strict';
const query = (selector, root = document) => root.querySelector(selector);
const all = (selector, root = document) => [...root.querySelectorAll(selector)];
const SAVED_KEY = 'galaxy-magazine-bookmarks-v1';
function getSaved() {
  try {
    const saved = JSON.parse(localStorage.getItem(SAVED_KEY) || '[]');
    return new Set(Array.isArray(saved) ? saved.filter(x => typeof x === 'string').slice(0, 100) : []);
  } catch {return new Set();}
}
const saved = getSaved();
function persist() {
  try {localStorage.setItem(SAVED_KEY, JSON.stringify([...saved]));} catch {}
}
const cards = all('[data-magazine-card]');
const filterButtons = all('[data-magazine-filter]');
const search = query('#magazine-search');
const favorites = query('#magazine-saved-only');
let group = 'الكل';
let onlySaved = false;
function normalizeArabic(text){
  return String(text||'').toLocaleLowerCase('ar')
    .replace(/[ًٌٍَُِّْـ]/g,'')
    .replace(/[أإآ]/g,'ا').replace(/ى/g,'ي').replace(/ة/g,'ه');
}
function updateBookmarks(){
  all('[data-magazine-save]').forEach(button=>{
    const slug = button.dataset.magazineSave;
    const isSaved = saved.has(slug);
    button.setAttribute('aria-pressed',String(isSaved));
    button.classList.toggle('is-saved',isSaved);
    button.textContent = button.classList.contains('magazine-save-detail')
      ? (isSaved?'★ المقال محفوظ على هذا الجهاز':'☆ احفظ المقال للعودة إليه')
      : (isSaved?'★':'☆');
    button.title = isSaved?'إزالة المقال من المحفوظة':'احفظ المقال على هذا الجهاز';
  });
}
function applyFilters(){
  if(!cards.length)return;
  const needle = normalizeArabic(search?.value.trim()||'');
  let visible = 0;
  cards.forEach(card=>{
    const matchesGroup = group === 'الكل' || card.dataset.magazineGroup === group;
    const matchesText = !needle || normalizeArabic(card.innerText).includes(needle);
    const matchesSaved = !onlySaved || saved.has(card.dataset.magazineSlug);
    const show = matchesGroup && matchesText && matchesSaved;
    card.hidden = !show;
    if(show)visible++;
  });
  const none = query('#magazine-no-results');
  if(none) none.hidden = visible!==0;
}
all('[data-magazine-save]').forEach(button=>{
  button.addEventListener('click',()=>{
    const slug = button.dataset.magazineSave;
    if(saved.has(slug))saved.delete(slug);else saved.add(slug);
    persist();updateBookmarks();applyFilters();
  });
});
filterButtons.forEach(button=>{
  button.addEventListener('click',()=>{
    group = button.dataset.magazineFilter;
    filterButtons.forEach(item=>{
      const pressed = item===button;
      item.classList.toggle('active', pressed);
      item.setAttribute('aria-pressed',String(pressed));
    });
    applyFilters();
  });
});
if(search)search.addEventListener('input',applyFilters);
if(favorites)favorites.addEventListener('click',()=>{
  onlySaved = !onlySaved;
  favorites.classList.toggle('active',onlySaved);
  favorites.setAttribute('aria-pressed',String(onlySaved));
  favorites.textContent = onlySaved?'★ المحفوظة فقط':'☆ المحفوظة';
  applyFilters();
});
updateBookmarks();
applyFilters();

const validIds = new Set(['XD2dxQenE2Q','A8-y6Gie4rE']);
all('[data-load-video]').forEach(button=>{
  button.addEventListener('click',()=>{
    const id = button.dataset.loadVideo;
    if(!validIds.has(id))return;
    const videoBox = button.closest('[data-video-container]');
    if(!videoBox)return;
    const target = query('[data-video-player]',videoBox);
    const preview = query('.magazine-video-preview',videoBox);
    if(!target||!preview)return;
    const frame = document.createElement('iframe');
    frame.src = 'https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0';
    frame.title = 'مشغل فيديو رسمي من قناة سبيستون غو';
    frame.setAttribute('allow','accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; web-share');
    frame.setAttribute('referrerpolicy','strict-origin-when-cross-origin');
    frame.setAttribute('allowfullscreen','');
    frame.setAttribute('loading','lazy');
    frame.style.border='0';
    target.replaceChildren(frame);
    preview.hidden = true;
    target.hidden = false;
  },{once:true});
});
const article = query('[data-magazine-article]');
const readingFill = query('#magazine-progress-fill');
if(article&&readingFill){
  let scheduled = false;
  function measure(){
    const bounds = article.getBoundingClientRect();
    const beginning = window.scrollY + bounds.top;
    const full = Math.max(article.offsetHeight-window.innerHeight*0.75,1);
    const current = Math.max(0,Math.min(1,(window.scrollY-beginning)/full));
    readingFill.style.width = (current*100).toFixed(1)+'%';
    scheduled=false;
  }
  window.addEventListener('scroll',()=>{
    if(!scheduled){scheduled=true;window.requestAnimationFrame(measure);}
  },{passive:true});
  window.addEventListener('resize',measure,{passive:true});
  measure();
}
})();
