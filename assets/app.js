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
const count=$('#watched-count'),bar=$('#watch-progress');if(count)count.textContent=String(watched.size);if(bar){bar.style.width=(watched.size/43*100)+'%';bar.setAttribute('aria-valuenow',String(watched.size));}
}
if(episodeButtons.length){
episodeButtons.forEach(b=>b.addEventListener('click',()=>{const n=Number(b.dataset.episode);watched.has(n)?watched.delete(n):watched.add(n);safeSave('galaxy-watched-v1',[...watched].sort((a,b)=>a-b));updateEpisodes();}));
const reset=$('#reset-watch');if(reset)reset.addEventListener('click',()=>{if(confirm('هل تريد مسح تقدم المشاهدة المحفوظ على هذا الجهاز فقط؟')){watched.clear();safeSave('galaxy-watched-v1',[]);updateEpisodes();}});
updateEpisodes();
}
const filter=$('#episode-filter');if(filter)filter.addEventListener('input',()=>{const q=filter.value.trim().replace(/[٠-٩]/g,x=>'٠١٢٣٤٥٦٧٨٩'.indexOf(x)).replace(/[۰-۹]/g,x=>'۰۱۲۳۴۵۶۷۸۹'.indexOf(x));episodeButtons.forEach(b=>{b.hidden=!!q&&!String(b.dataset.episode).includes(q);});});
const quizArea=$('#quiz-area');
const questions=[
{q:'ما الرياضة الأساسية في أبطال الكرة: فرسان المجرة؟',a:['كرة القدم','كرة السلة','السباحة','التنس'],c:0},
{q:'إلى أي سلسلة أنمي ينتمي فرسان المجرة؟',a:['ون بيس','أبطال الكرة','ناروتو','دراغون بول'],c:1},
{q:'ما الاسم الياباني لسلسلة فرسان المجرة؟',a:['Inazuma Eleven GO Galaxy','Captain Tsubasa','Blue Lock','Haikyu'],c:0},
{q:'كم عدد حلقات النسخة اليابانية الأصلية من GO Galaxy؟',a:['12 حلقة','26 حلقة','43 حلقة','100 حلقة'],c:2},
{q:'أي من هذه الشخصيات تظهر في قسم الشخصيات بالموقع؟',a:['بيان','لوفي','غوكو','تانجيرو'],c:0},
{q:'ماذا تعني «المجرة» في عنوان الأنمي؟',a:['محيط','Galaxy','غابة','صحراء'],c:1},
{q:'أين يمكنك حفظ تقدم مشاهدة الحلقات في هذا الموقع؟',a:['في دفتر ورقي فقط','في متتبع الحلقات','على خادم الموقع','عبر حساب مدفوع'],c:1},
{q:'ما أفضل طريقة للاستمتاع بالأنمي مع الأصدقاء؟',a:['احترام الآخرين والروح الرياضية','التنمر على المنافسين','مشاركة معلومات خاصة','كسر قواعد اللعب'],c:0}
];
let qi=0,score=0,locked=false;
const quizSaved=safeRead('galaxy-best-quiz-v1',0);
function showQuiz(){
if(!quizArea)return;
if(qi>=questions.length){quizArea.innerHTML='<h2>انتهى التحدي! 🏆</h2><p class="quiz-status">نتيجتك: '+score+' من '+questions.length+'</p><p>أحسنت! شارك التحدي مع أصدقائك واستمر في التعلم واللعب بروح رياضية.</p><button class="btn primary" type="button" id="quiz-restart">العب من جديد</button>';const best=Math.max(score,quizSaved);safeSave('galaxy-best-quiz-v1',best);$('#quiz-restart').addEventListener('click',()=>{qi=0;score=0;showQuiz()});return;}
const item=questions[qi];locked=false;quizArea.innerHTML='<div class="meta">السؤال '+(qi+1)+' من '+questions.length+'</div><h2>'+item.q+'</h2><div class="answers">'+item.a.map((a,i)=>'<label><input type="radio" name="answer" value="'+i+'"> '+a+'</label>').join('')+'</div><button type="button" class="btn primary" id="quiz-next">تأكيد الإجابة</button><div class="quiz-status" id="quiz-feedback" role="status"></div>';
$('#quiz-next').addEventListener('click',()=>{if(locked){qi++;showQuiz();return;}const chosen=$('input[name="answer"]:checked');if(!chosen){$('#quiz-feedback').textContent='اختر إجابة أولًا.';return;}const right=Number(chosen.value)===item.c;if(right)score++;locked=true;$$('input[name="answer"]').forEach(x=>x.disabled=true);$('#quiz-feedback').textContent=right?'إجابة صحيحة! 🌟':'الإجابة الصحيحة: '+item.a[item.c];$('#quiz-next').textContent=qi===questions.length-1?'شاهد النتيجة':'السؤال التالي';});
}
if(quizArea)showQuiz();
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