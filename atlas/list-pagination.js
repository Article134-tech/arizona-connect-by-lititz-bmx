(function(){
const PAGE_SIZE=20;
document.querySelectorAll('[data-simple-paged-list]').forEach(list=>{
  const cards=[...list.querySelectorAll('[data-simple-paged-card]')]; if(cards.length<=PAGE_SIZE)return;
  const scope=list.closest('[data-paged-scope]')||list.parentElement;
  const statuses=[...scope.querySelectorAll('[data-range-status]')], pagers=[...scope.querySelectorAll('[data-page-controls]')]; let page=1;
  function mk(label,target,disabled,current){const b=document.createElement('button');b.type='button';b.textContent=label;b.disabled=disabled;if(current)b.setAttribute('aria-current','page');b.addEventListener('click',()=>{page=target;render();scope.scrollIntoView({block:'start'})});return b}
  function render(){const pages=Math.ceil(cards.length/PAGE_SIZE);page=Math.max(1,Math.min(page,pages));const start=(page-1)*PAGE_SIZE,end=Math.min(start+PAGE_SIZE,cards.length);cards.forEach((c,i)=>c.hidden=i<start||i>=end);statuses.forEach(x=>x.textContent=`Showing ${start+1}-${end} of ${cards.length}`);pagers.forEach(n=>{n.replaceChildren();n.append(mk('Previous',page-1,page===1,false));for(let i=1;i<=pages;i++)n.append(mk(String(i),i,false,i===page));n.append(mk('Next',page+1,page===pages,false))})}
  render();
});
})();