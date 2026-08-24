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
  stage?.classList.toggle('all-on',view==='all');
  if(list) list.hidden=view!=='list';
  if(map) map.hidden=view==='list';
}
viewButtons.forEach(b=>b.addEventListener('click',()=>setView(b.dataset.view)));

const search=document.getElementById('trackSearch');
const filter=document.getElementById('trackFilter');
const locationFilter=document.getElementById('locationFilter');
const cards=[...document.querySelectorAll('[data-track-card]')];
const resultCount=document.getElementById('resultCount');
const mappedIds=new Set([...document.querySelectorAll('[data-map-pin]')].map(x=>x.dataset.trackId));
const statuses=[...document.querySelectorAll('#explore [data-range-status]')];
const pagers=[...document.querySelectorAll('#explore [data-page-controls]')];
const PAGE_SIZE=20; let page=1;
function matchedCards(){
  const q=(search?.value||'').trim().toLowerCase(),group=filter?.value||'',loc=locationFilter?.value||'';
  return cards.filter(card=>{const mapped=mappedIds.has(card.id.replace('card-',''));return (!q||card.dataset.search.includes(q))&&(!group||card.dataset.group===group)&&(!loc||(loc==='mapped'?mapped:!mapped))});
}
function pageButton(label,target,disabled,current){const b=document.createElement('button');b.type='button';b.textContent=label;b.disabled=disabled;if(current)b.setAttribute('aria-current','page');b.addEventListener('click',()=>{page=target;apply();document.getElementById('explore')?.scrollIntoView({block:'start'})});return b}
function apply(resetPage=false){
  const matches=matchedCards(); if(resetPage)page=1; const pages=Math.max(1,Math.ceil(matches.length/PAGE_SIZE)); page=Math.max(1,Math.min(page,pages));
  cards.forEach(c=>c.hidden=true); const start=(page-1)*PAGE_SIZE,end=Math.min(start+PAGE_SIZE,matches.length); matches.slice(start,end).forEach(c=>c.hidden=false);
  if(resultCount)resultCount.textContent=`${matches.length} record${matches.length===1?'':'s'}`;
  const label=matches.length?`Showing ${start+1}-${end} of ${matches.length}`:'Showing 0-0 of 0'; statuses.forEach(x=>x.textContent=label);
  pagers.forEach(n=>{n.replaceChildren();if(pages<=1){n.hidden=true;return}n.hidden=false;n.append(pageButton('Previous',page-1,page===1,false));for(let i=1;i<=pages;i++)n.append(pageButton(String(i),i,false,i===page));n.append(pageButton('Next',page+1,page===pages,false))});
}
const params=new URLSearchParams(location.search);const focusTrack=params.get('track');if(focusTrack&&cards.some(c=>c.id===`card-${focusTrack}`)){if(search)search.value=focusTrack;}
search?.addEventListener('input',()=>apply(true));filter?.addEventListener('change',()=>apply(true));locationFilter?.addEventListener('change',()=>apply(true));apply(true);if(focusTrack){requestAnimationFrame(()=>document.getElementById(`card-${focusTrack}`)?.scrollIntoView({block:'center'}));}

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
