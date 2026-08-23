(function(){
  const interactive='a,button,input,select,textarea,label,summary';
  function activateTile(tile,selector){
    if(!tile||tile.matches('a[href]'))return;
    const link=tile.querySelector(selector);
    if(!link)return;
    tile.setAttribute('role','link');
    if(!tile.hasAttribute('tabindex'))tile.tabIndex=0;
    tile.dataset.primaryHref=link.getAttribute('href');
    const go=()=>{window.location.href=link.href};
    tile.addEventListener('click',event=>{if(event.target.closest(interactive))return;go()});
    tile.addEventListener('keydown',event=>{
      if((event.key==='Enter'||event.key===' ')&&!event.target.closest(interactive)){
        event.preventDefault();go();
      }
    });
  }
  document.querySelectorAll('.event-card').forEach(tile=>activateTile(tile,'.event-title-link'));
  document.querySelectorAll('.media-card').forEach(tile=>activateTile(tile,'a.primary'));
  document.querySelectorAll('.tp-claim').forEach(tile=>activateTile(tile,'a[href*="/research/claims/"]'));
})();
