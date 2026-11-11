/* Galaxy Knights home portal — accessible, anonymous and local-only interactions. */
(() => {
'use strict';
const $=id=>document.getElementById(id);
const buttons=[...document.querySelectorAll('[data-home-mission]')];
const missionInfo={
  watcher:{title:'ابدأ رحلة الحلقات',description:'تابع الحلقات الـ43 واحتفظ بما شاهدته على جهازك.',url:'/episodes/',button:'اكتشف الحلقات ←'},
  expert:{title:'اكتشف أسرار اللاعبين',description:'تعرّف على بيان وحيان وعقاب، ثم اختبر معلوماتك بالصور.',url:'/characters/',button:'تعرّف إلى الأبطال ←'},
  explorer:{title:'رحلتك بين الكواكب تبدأ هنا',description:'اقرأ عن العوالم الفضائية التي يزورها فريق الأرض في فرسان المجرة.',url:'/articles/galaxy-worlds/',button:'اكتشف الكواكب ←'}
};
const result=$('home-mission-result');
if(result){
 buttons.forEach(button=>button.addEventListener('click',()=>{
   const next=missionInfo[button.dataset.homeMission];if(!next)return;
   buttons.forEach(b=>{
      const active=b===button;
      b.classList.toggle('active',active);
      b.setAttribute('aria-pressed',String(active));
   });
   $('home-mission-label').textContent=next.title;
   $('home-mission-description').textContent=next.description;
   const link=$('home-mission-link');link.href=next.url;link.textContent=next.button;
 }));
}
const progress=$('home-watch-track');
if(progress){
 let watched=[];
 try{
   const data=JSON.parse(localStorage.getItem('galaxy-watched-v1')||'[]');
   if(Array.isArray(data))watched=[...new Set(data.filter(n=>Number.isInteger(n)&&n>=1&&n<=43))];
 }catch{}
 const value=watched.length;
 $('home-watched-number').textContent=String(value);
 $('home-watch-percent').textContent=Math.round(value*100/43)+'% مكتمل';
 $('home-watch-fill').style.width=(value*100/43)+'%';
 progress.setAttribute('aria-valuenow',String(value));
 const next=Array.from({length:43},(_,i)=>i+1).find(n=>!watched.includes(n));
 if(next){
   $('home-watch-message').textContent=value?'رائع! شاهدت '+value+' حلقة. الحلقة التالية في رحلتك: '+next+'.':'ابدأ من الحلقة الأولى، وحدّث تقدمك بعد كل مشاهدة.';
   $('home-watch-cta').textContent=value?'واصل عند الحلقة '+next+' ←':'ابدأ رحلة الحلقات ←';
 }else{
   $('home-watch-message').textContent='أكملت الحلقات الـ43! يمكنك استكشاف الشخصيات والمقالات أو إعادة المشاهدة.';
   $('home-watch-cta').href='/articles/';
   $('home-watch-cta').textContent='اكتشف المقالات ←';
 }
}
const raw=$('home-mini-bank');
if(!raw)return;
let bank=[];
try{bank=JSON.parse(raw.textContent);}catch{return;}
if(!Array.isArray(bank)||bank.length!==3||!bank.every(q=>Array.isArray(q.options)&&q.options.length===4&&Number.isInteger(q.answer)))return;
let step=0,score=0,answered=false;
const optionContainer=$('home-mini-options');
const panel=$('home-mini-finish');
function render(){
 const q=bank[step];answered=false;
 $('home-mini-question').textContent=q.question;
 $('home-mini-image').src=q.image;
 $('home-mini-image').alt='رسمة توضيحية مرتبطة بالسؤال '+(step+1);
 $('home-mini-count').textContent='السؤال '+(step+1)+' من '+bank.length;
 $('home-mini-score').textContent='⭐ '+score*10+' نقاط';
 $('home-mini-progress').setAttribute('aria-valuenow',String(step));
 $('home-mini-progress-fill').style.width=(step*100/bank.length)+'%';
 optionContainer.replaceChildren();
 q.options.forEach((option,i)=>{
   const button=document.createElement('button');
   button.type='button';
   button.dataset.homeAnswer=String(i);
   button.textContent=option;
   button.addEventListener('click',()=>answer(i));
   optionContainer.append(button);
 });
 const feedback=$('home-mini-feedback');feedback.hidden=true;feedback.textContent='';
 $('home-mini-next').hidden=true;
 panel.hidden=true;
}
function answer(selected){
 if(answered)return;
 answered=true;
 const q=bank[step];
 const correct=selected===q.answer;
 if(correct)score++;
 const options=[...optionContainer.querySelectorAll('button')];
 options.forEach((button,i)=>{
   button.disabled=true;
   if(i===q.answer)button.classList.add('correct');
   else if(i===selected)button.classList.add('wrong');
 });
 $('home-mini-score').textContent='⭐ '+score*10+' نقاط';
 const feedback=$('home-mini-feedback');
 feedback.hidden=false;
 feedback.textContent=(correct?'🎉 إجابة صحيحة! ':'💡 إجابة أخرى هذه المرة. ')+q.explanation;
 const next=$('home-mini-next');
 next.hidden=false;next.textContent=step===bank.length-1?'شاهد النتيجة ←':'السؤال التالي ←';
 next.focus({preventScroll:true});
}
function next(){
 if(!answered)return;
 step++;
 if(step>=bank.length){
   optionContainer.replaceChildren();
   $('home-mini-question').textContent='أحسنت، انتهى التحدي!';
   $('home-mini-feedback').hidden=true;
   $('home-mini-next').hidden=true;
   $('home-mini-progress').setAttribute('aria-valuenow',String(bank.length));
   $('home-mini-progress-fill').style.width='100%';
   $('home-mini-count').textContent='اكتملت الأسئلة الثلاثة';
   $('home-mini-final-score').textContent='🏅 نتيجتك: '+score+' من '+bank.length;
   panel.hidden=false;
   $('home-mini-restart').focus({preventScroll:true});
 }else{render();}
}
$('home-mini-next').addEventListener('click',next);
$('home-mini-restart').addEventListener('click',()=>{
 step=0;score=0;render();
 $('home-mini-question').focus?.({preventScroll:true});
});
render();
})();