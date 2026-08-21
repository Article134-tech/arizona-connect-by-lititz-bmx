
const s=document.querySelector('[data-claim-search]'),c=document.querySelector('[data-category-filter]'),r=document.querySelector('[data-reset]'),cards=[...document.querySelectorAll('[data-claim-card]')],count=document.querySelector('[data-count]');
function apply(){if(!cards.length)return;const q=(s?.value||'').trim().toLowerCase(),cv=c?.value||'';let n=0;cards.forEach(x=>{const ok=(!q||x.dataset.search.includes(q))&&(!cv||x.dataset.category===cv);x.hidden=!ok;if(ok)n++});if(count)count.textContent=n}
s?.addEventListener('input',apply);c?.addEventListener('change',apply);r?.addEventListener('click',()=>{if(s)s.value='';if(c)c.value='';apply()});
