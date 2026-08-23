const PAGE_SIZE=20;
const INTERACTIVE='a,button,input,select,textarea,label,summary';

function activateCard(card,primarySelector){
  if(!card||card.matches('a[href]'))return;
  const link=card.querySelector(primarySelector);
  if(!link)return;
  card.setAttribute('role','link');
  if(!card.hasAttribute('tabindex'))card.tabIndex=0;
  const go=()=>{window.location.href=link.href};
  card.addEventListener('click',event=>{
    if(event.target.closest(INTERACTIVE))return;
    go();
  });
  card.addEventListener('keydown',event=>{
    if((event.key==='Enter'||event.key===' ')&&!event.target.closest(INTERACTIVE)){
      event.preventDefault();go();
    }
  });
}
function activateCards(selector,primarySelector){
  document.querySelectorAll(selector).forEach(card=>activateCard(card,primarySelector));
}
activateCards('.claim-card','.card-actions a.primary');
activateCards('.category-card','a[href*="claims/index.html"]');

const s=document.querySelector('[data-claim-search]');
const c=document.querySelector('[data-category-filter]');
const r=document.querySelector('[data-reset]');
const cards=[...document.querySelectorAll('[data-claim-card]')];
const count=document.querySelector('[data-count]');
const statusEls=[...document.querySelectorAll('[data-range-status]')];
const pagerEls=[...document.querySelectorAll('[data-page-controls]')];
let currentPage=1;

function matchingCards(){
  const q=(s?.value||'').trim().toLowerCase();
  const cv=c?.value||'';
  return cards.filter(card=>(!q||card.dataset.search.includes(q))&&(!cv||card.dataset.category===cv));
}
function setPage(page){
  const total=Math.max(1,Math.ceil(matchingCards().length/PAGE_SIZE));
  currentPage=Math.max(1,Math.min(page,total));
  apply();
  document.querySelector('.filters')?.scrollIntoView({block:'start'});
}
function pageButton(label,page,disabled=false,current=false){
  const b=document.createElement('button');
  b.type='button';b.textContent=label;b.disabled=disabled;b.dataset.pageTarget=String(page);
  if(current)b.setAttribute('aria-current','page');
  b.addEventListener('click',()=>setPage(page));
  return b;
}
function renderPager(total){
  const pages=Math.ceil(total/PAGE_SIZE);
  pagerEls.forEach(nav=>{
    nav.replaceChildren();
    if(pages<=1){nav.hidden=true;return}
    nav.hidden=false;
    nav.append(pageButton('Previous',currentPage-1,currentPage===1));
    for(let p=1;p<=pages;p++)nav.append(pageButton(String(p),p,false,p===currentPage));
    nav.append(pageButton('Next',currentPage+1,currentPage===pages));
  });
}
function apply(resetPage=false){
  if(!cards.length)return;
  const matches=matchingCards();
  if(resetPage)currentPage=1;
  const pages=Math.max(1,Math.ceil(matches.length/PAGE_SIZE));
  currentPage=Math.min(currentPage,pages);
  cards.forEach(card=>card.hidden=true);
  const start=(currentPage-1)*PAGE_SIZE;
  const end=Math.min(start+PAGE_SIZE,matches.length);
  matches.slice(start,end).forEach(card=>card.hidden=false);
  if(count)count.textContent=matches.length;
  const label=matches.length?`Showing ${start+1}-${end} of ${matches.length}`:'Showing 0-0 of 0';
  statusEls.forEach(el=>el.textContent=label);
  renderPager(matches.length);
}

if(c){
  const category=new URLSearchParams(window.location.search).get('category');
  if(category&&[...c.options].some(option=>option.value===category))c.value=category;
}
s?.addEventListener('input',()=>apply(true));
c?.addEventListener('change',()=>apply(true));
r?.addEventListener('click',()=>{if(s)s.value='';if(c)c.value='';apply(true)});
apply();
