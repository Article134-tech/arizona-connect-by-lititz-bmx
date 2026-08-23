const menuButton=document.querySelector('.menu-toggle');
const nav=document.getElementById('primaryNav');
menuButton?.addEventListener('click',()=>{const open=menuButton.getAttribute('aria-expanded')==='true';menuButton.setAttribute('aria-expanded',String(!open));nav?.classList.toggle('open',!open)});

const stage=document.getElementById('mapStage');
const map=document.getElementById('azMap');
const list=document.getElementById('accessibleMapList');
const viewButtons=[...document.querySelectorAll('[data-view]')];
function setView(view){
  viewButtons.forEach(b=>{const active=b.dataset.view===view;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active))});
  stage?.classList.toggle('historical-on',view==='historical');
  if(list) list.hidden=view!=='list';
  if(map) map.hidden=view==='list';
}
viewButtons.forEach(b=>b.addEventListener('click',()=>setView(b.dataset.view)));

const search=document.getElementById('trackSearch');
const filter=document.getElementById('trackFilter');
const locationFilter=document.getElementById('locationFilter');
const cards=[...document.querySelectorAll('[data-track-card]')];
const resultCount=document.getElementById('resultCount');
const loadMore=document.getElementById('loadMore');
const mappedIds=new Set([...document.querySelectorAll('[data-map-pin]')].map(x=>x.dataset.trackId));
let expanded=false;
function apply(){
  const q=(search?.value||'').trim().toLowerCase();
  const group=filter?.value||'';
  const loc=locationFilter?.value||'';
  const matches=[];
  cards.forEach(card=>{
    const mapped=mappedIds.has(card.id.replace('card-',''));
    const ok=(!q||card.dataset.search.includes(q))&&(!group||card.dataset.group===group)&&(!loc||(loc==='mapped'?mapped:!mapped));
    if(ok) matches.push(card);
    card.hidden=!ok;
  });
  const limit=expanded?matches.length:Math.min(matches.length,8);
  matches.forEach((card,i)=>card.hidden=i>=limit);
  if(resultCount) resultCount.textContent=`${matches.length} record${matches.length===1?'':'s'}`;
  if(loadMore){loadMore.hidden=matches.length<=8;loadMore.textContent=expanded?'Show first 8':'Show all '+matches.length+' records'}
}
search?.addEventListener('input',apply);filter?.addEventListener('change',apply);locationFilter?.addEventListener('change',apply);loadMore?.addEventListener('click',()=>{expanded=!expanded;apply();if(!expanded)document.getElementById('explore')?.scrollIntoView({behavior:'smooth'})});
apply();

function activateTrackCards(){
  const interactive='a,button,input,select,textarea,label,summary';
  document.querySelectorAll('[data-track-card]').forEach(card=>{
    const link=card.querySelector('.card-link');
    if(!link)return;
    card.setAttribute('role','link');
    if(!card.hasAttribute('tabindex'))card.tabIndex=0;
    card.dataset.primaryHref=link.getAttribute('href');
    const go=()=>{window.location.href=link.href};
    card.addEventListener('click',event=>{if(event.target.closest(interactive))return;go()});
    card.addEventListener('keydown',event=>{
      if((event.key==='Enter'||event.key===' ')&&!event.target.closest(interactive)){
        event.preventDefault();go();
      }
    });
  });
}
activateTrackCards();
