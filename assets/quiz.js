/* Galaxy Knights Arabic Quiz Arcade — local-only, child-friendly, accessible. */
(()=>{'use strict';
const bank=window.GALAXY_QUIZ_BANK;
const hub=document.getElementById('quiz-hub');
const play=document.getElementById('quiz-play');
const end=document.getElementById('quiz-end');
if(!hub||!play||!end||!bank||!Array.isArray(bank.questions))return;
const $=(id)=>document.getElementById(id);
const KEY='galaxy-quiz-arcade-v1';
const STORAGE_DEFAULT={best:{},plays:{},seen:{}};
function readStorage(){try{const v=JSON.parse(localStorage.getItem(KEY));return v&&typeof v==='object'?{...STORAGE_DEFAULT,...v}:structuredClone(STORAGE_DEFAULT);}catch{return {best:{},plays:{},seen:{}};}}
let storage=readStorage();
if(!storage.best||typeof storage.best!=='object')storage.best={};
if(!storage.plays||typeof storage.plays!=='object')storage.plays={};
if(!storage.seen||typeof storage.seen!=='object')storage.seen={};
function save(){try{localStorage.setItem(KEY,JSON.stringify(storage));}catch{}}
function shuffle(list){const out=list.slice();for(let i=out.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[out[i],out[j]]=[out[j],out[i]];}return out;}
function sourceFor(cat){return bank.categories.find(c=>c.id===cat)||null;}
const escapeText=(t)=>String(t??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const reducedMotion=()=>window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function scrollToNode(node){node.scrollIntoView({block:'start',behavior:reducedMotion()?'instant':'smooth'});}
let state=null;
function choose(cat,count){
 let pool=bank.questions.filter(q=>cat==='marathon'||q.category===cat);
 if(cat==='marathon'){
   const lists=bank.categories.map(c=>shuffle(bank.questions.filter(q=>q.category===c.id)));
   let picked=[];
   for(let round=0;round<5&&picked.length<count;round++){for(const list of lists){if(list[round])picked.push(list[round]);}}
   pool=shuffle(picked.length>=count?picked:bank.questions);
 }
 const past=new Set(Array.isArray(storage.seen[cat])?storage.seen[cat]:[]);
 let unseen=shuffle(pool.filter(q=>!past.has(q.id)));
 let seen=shuffle(pool.filter(q=>past.has(q.id)));
 if(unseen.length<count){unseen=unseen.concat(seen);}
 const chosen=unseen.slice(0,Math.min(count,pool.length));
 const knownIds=new Set(bank.questions.filter(q=>cat==='marathon'||q.category===cat).map(q=>q.id));
 let history=(storage.seen[cat]||[]).filter(id=>knownIds.has(id));
 if(history.length>=knownIds.size)history=[];
 const historySet=new Set(history);
 chosen.forEach(q=>historySet.add(q.id));
 storage.seen[cat]=[...historySet].slice(-160);
 save();
 return chosen;
}
function show(which){hub.hidden=which!=='hub';play.hidden=which!=='play';end.hidden=which!=='end';}
function updateDashboard(){
 const total=Object.values(storage.plays).reduce((sum,v)=>sum+(Number(v)||0),0);
 if($('quiz-total-plays'))$('quiz-total-plays').textContent=String(total);
 document.querySelectorAll('[data-quiz-best]').forEach(el=>{
   const cat=el.getAttribute('data-quiz-best'),best=Number(storage.best[cat]||0);
   el.textContent=best?('أفضل نتيجة: '+best+' / '+(cat==='marathon'?20:10)):'ابدأ أول تحدٍّ';
 });
}
function startQuiz(cat){
 if(cat!=='marathon'&&!sourceFor(cat))return;
 const total=cat==='marathon'?20:10;
 const selected=choose(cat,total);
 if(!selected.length)return;
 const category=sourceFor(cat);
 state={cat,questions:selected,index:0,correct:0,locked:false,missed:[],streak:0,maxStreak:0};
 $('quiz-mode-name').textContent=category?category.title:'الملحمة الكونية';
 $('quiz-mode-description').textContent='أجب عن الأسئلة بالترتيب واكتشف الإجابة الصحيحة بعد كل محاولة.';
 show('play');renderQuestion();scrollToNode(play);
}
function renderQuestion(){
 if(!state)return;
 const q=state.questions[state.index];state.locked=false;
 $('quiz-question-counter').textContent='السؤال '+(state.index+1)+' من '+state.questions.length;
 $('quiz-score').textContent='⭐ '+state.correct*10+' نقطة';
 $('quiz-streak').textContent=state.streak>=2?'🔥 '+state.streak+' متتالية':'✨ اكتشف الإجابة';
 const fraction=(state.index/state.questions.length)*100;
 $('quiz-progress-fill').style.width=fraction+'%';
 $('quiz-progress-track').setAttribute('aria-valuenow',String(state.index));
 $('quiz-progress-track').setAttribute('aria-valuemax',String(state.questions.length));
 $('quiz-question').textContent=q.question;
 $('quiz-topic').textContent=(sourceFor(q.category)||{title:'تحدي المعرفة'}).title;
 const picture=$('quiz-question-image');
 picture.src=q.image;
 picture.alt=q.imageAlt||'رسم توضيحي للسؤال';
 picture.classList.toggle('quiz-portrait-image',q.imageType==='portrait');
 picture.classList.toggle('quiz-themed-image',q.imageType!=='portrait');
 const fallback=q.localFallback||'/assets/quiz-cosmos.svg';
 picture.onerror=()=>{picture.onerror=null;picture.src=fallback;};
 $('quiz-answers').replaceChildren();
 q.options.forEach((option,i)=>{
    const button=document.createElement('button');
    button.type='button';button.className='quiz-choice';
    const mark=document.createElement('span');mark.className='choice-letter';mark.textContent=['أ','ب','ج','د'][i];
    const label=document.createElement('span');label.className='choice-label';label.textContent=option;
    button.append(mark,label);
    button.addEventListener('click',()=>selectAnswer(i));
    $('quiz-answers').append(button);
 });
 const feedback=$('quiz-feedback');
 feedback.hidden=true;
 feedback.className='quiz-feedback';
 feedback.textContent='';
 const next=$('quiz-next');
 next.hidden=true;
 next.textContent=state.index===state.questions.length-1?'مشاهدة نتيجتي ←':'السؤال التالي ←';
 $('quiz-answer-help').textContent='اختر إجابة واحدة من الخيارات الأربعة.';
}
function selectAnswer(index){
 if(!state||state.locked)return;
 const q=state.questions[state.index];
 state.locked=true;
 const right=index===q.answer;
 const buttons=[...$('quiz-answers').querySelectorAll('button')];
 buttons.forEach((button,i)=>{
    button.disabled=true;
    if(i===q.answer)button.classList.add('correct');
    else if(i===index)button.classList.add('incorrect');
    if(i===q.answer||i===index)button.setAttribute('aria-label',button.innerText+(i===q.answer?' — الإجابة الصحيحة':' — اختيار غير صحيح'));
 });
 if(right){state.correct++;state.streak++;state.maxStreak=Math.max(state.maxStreak,state.streak);}
 else{state.streak=0;state.missed.push({question:q.question,selected:q.options[index],correct:q.options[q.answer],explanation:q.explanation});}
 $('quiz-score').textContent='⭐ '+state.correct*10+' نقطة';
 const feedback=$('quiz-feedback');
 feedback.hidden=false;
 feedback.classList.add(right?'positive':'neutral');
 feedback.innerHTML='<strong>'+(right?'🌟 إجابة رائعة!':'💡 تعلّم شيئًا جديدًا!')+'</strong><p>'+escapeText(q.explanation)+'</p>';
 $('quiz-answer-help').textContent=right?'أحسنت، واصل التحدي!':'يمكنك متابعة التحدي؛ الأخطاء فرصة للتعلّم.';
 $('quiz-next').hidden=false;
 $('quiz-next').focus({preventScroll:true});
}
function finishQuiz(){
 if(!state)return;
 const s=state,n=s.questions.length,accuracy=Math.round(100*s.correct/n);
 const currentBest=Number(storage.best[s.cat]||0);
 storage.best[s.cat]=Math.max(s.correct,currentBest);
 storage.plays[s.cat]=Number(storage.plays[s.cat]||0)+1;
 save();updateDashboard();
 $('quiz-finish-icon').textContent=accuracy>=90?'🏆':accuracy>=60?'🌟':'💪';
 $('quiz-finish-title').textContent=accuracy>=90?'أنت من أساطير المجرة!':accuracy>=60?'إنجاز رائع يا بطل!':'رحلتك نحو الاحتراف بدأت!';
 $('quiz-finish-score').textContent=s.correct+' / '+n;
 $('quiz-finish-percent').textContent=accuracy+'%';
 $('quiz-finish-streak').textContent=String(s.maxStreak);
 $('quiz-finish-best').textContent=String(storage.best[s.cat]);
 $('quiz-finish-caption').textContent='حصلت على '+s.correct*10+' نقطة من أصل '+n*10+'. اختر تحديًا آخر أو راجع الإجابات لتتعلم أكثر.';
 const review=$('quiz-mistakes');
 review.replaceChildren();
 if(s.missed.length){
   s.missed.forEach((miss,i)=>{
      const card=document.createElement('details');card.className='quiz-review-item';
      const summary=document.createElement('summary');summary.textContent=(i+1)+'. '+miss.question;
      const answer=document.createElement('p');answer.innerHTML='<strong>الإجابة الصحيحة:</strong> '+escapeText(miss.correct);
      const explain=document.createElement('p');explain.textContent=miss.explanation;
      card.append(summary,answer,explain);review.append(card);
   });
   $('quiz-mistakes-title').textContent='راجع '+s.missed.length+' إجابات وتعلّم منها';
 }else{$('quiz-mistakes-title').textContent='رائع! أجبت عن كل الأسئلة بشكل صحيح 🎉';}
 $('quiz-retry-wrong').hidden=!s.missed.length;
 show('end');scrollToNode(end);
}
function nextQuestion(){
 if(!state||!state.locked)return;
 state.index++;
 if(state.index>=state.questions.length)finishQuiz();
 else{renderQuestion();scrollToNode(play);}
}
document.querySelectorAll('[data-start-category]').forEach(button=>button.addEventListener('click',()=>startQuiz(button.dataset.startCategory)));
$('quiz-next').addEventListener('click',nextQuestion);
$('quiz-exit').addEventListener('click',()=>{state=null;show('hub');updateDashboard();scrollToNode(hub);});
$('quiz-again').addEventListener('click',()=>{if(state)startQuiz(state.cat);});
$('quiz-back').addEventListener('click',()=>{state=null;show('hub');scrollToNode(hub);});
$('quiz-retry-wrong').addEventListener('click',()=>{
 if(!state||!state.missed.length)return;
 const missedQuestions=state.questions.filter(q=>state.missed.some(m=>m.question===q.question));
 state={cat:state.cat,questions:shuffle(missedQuestions),index:0,correct:0,locked:false,missed:[],streak:0,maxStreak:0};
 $('quiz-mode-name').textContent='مراجعة الأخطاء';
 $('quiz-mode-description').textContent='تدرب على الأسئلة التي أخطأت فيها فقط.';
 show('play');renderQuestion();scrollToNode(play);
});
$('quiz-share').addEventListener('click',async()=>{
 if(!state)return;
 const message='أنهيت تحدي أبطال الكرة فرسان المجرة وحصلت على '+state.correct+' من '+state.questions.length+'! ⚽🌌\nhttps://galaxy-knights-ar.pages.dev/quiz/';
 try{
   if(navigator.share)await navigator.share({title:'تحدي مجرة الفرسان',text:message});
   else if(navigator.clipboard){await navigator.clipboard.writeText(message);$('quiz-share').textContent='تم نسخ النتيجة ✓';}
 }catch(err){if(err&&err.name!=='AbortError')$('quiz-share').textContent='لم نتمكن من المشاركة';}
});
updateDashboard();
})();
