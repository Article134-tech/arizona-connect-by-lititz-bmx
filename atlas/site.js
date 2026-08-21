
const q=document.querySelector('[data-track-search]'),f=document.querySelector('[data-track-filter]'),r=document.querySelector('[data-reset]'),cards=[...document.querySelectorAll('[data-track-card]')],count=document.querySelector('[data-count]');
function apply(){if(!cards.length)return;const s=(q?.value||'').toLowerCase().trim(),g=f?.value||'';let n=0;cards.forEach(c=>{const ok=(!s||c.dataset.search.includes(s))&&(!g||c.dataset.group===g);c.hidden=!ok;if(ok)n++});if(count)count.textContent=n}
q?.addEventListener('input',apply);f?.addEventListener('change',apply);r?.addEventListener('click',()=>{if(q)q.value='';if(f)f.value='';apply()});

const histToggle=document.querySelector('[data-historical-toggle]');
histToggle?.addEventListener('click',()=>{
  const on=histToggle.getAttribute('aria-pressed')==='true';
  histToggle.setAttribute('aria-pressed',String(!on));
  document.querySelectorAll('.historical-pin').forEach(x=>x.classList.toggle('is-hidden',on));
});
