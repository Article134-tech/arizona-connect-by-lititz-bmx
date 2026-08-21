(() => {
  const STORAGE_LAST_APP = 'arizonaConnectLastApp';
  const STORAGE_BOOTED = 'arizonaConnectBooted';
  const boot = document.getElementById('boot');
  const bootStatus = document.getElementById('boot-status');
  const main = document.getElementById('connection');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hasBooted = sessionStorage.getItem(STORAGE_BOOTED) === '1';
  const delay = reduceMotion ? 50 : (hasBooted ? 450 : 1650);

  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';

  if (hasBooted) {
    bootStatus.textContent = 'Waking Arizona Connect…';
  } else {
    setTimeout(() => { bootStatus.textContent = 'Loading applications…'; }, 450);
    setTimeout(() => { bootStatus.textContent = 'Ready.'; }, 1150);
  }

  setTimeout(() => {
    boot.classList.add('is-hidden');
    sessionStorage.setItem(STORAGE_BOOTED, '1');
    main.focus({preventScroll:true});
  }, delay);

  const resume = document.getElementById('resume');
  const resumeLink = document.getElementById('resume-link');
  const clearResume = document.getElementById('clear-resume');
  const appCards = [...document.querySelectorAll('.app-card')];

  const appRoutes = new Map(appCards.map(card => [
    card.dataset.app,
    {
      name: card.querySelector('.app-title')?.textContent.trim() || card.dataset.app,
      url: card.href,
      target: card.target || ''
    }
  ]));

  function clearRememberedApp() {
    localStorage.removeItem(STORAGE_LAST_APP);
    resume.hidden = true;
    resumeLink.removeAttribute('href');
    resumeLink.removeAttribute('target');
    resumeLink.removeAttribute('rel');
    resumeLink.textContent = '';
  }

  function showResume() {
    try {
      const last = JSON.parse(localStorage.getItem(STORAGE_LAST_APP));
      const appKey = last?.app || last?.name;
      const route = appKey ? appRoutes.get(appKey) : null;
      if (!route) {
        clearRememberedApp();
        return;
      }
      resume.hidden = false;
      resumeLink.textContent = route.name;
      resumeLink.href = route.url;
      if (route.target === '_blank') {
        resumeLink.target = '_blank';
        resumeLink.rel = 'noopener noreferrer';
      } else {
        resumeLink.removeAttribute('target');
        resumeLink.removeAttribute('rel');
      }
    } catch (_) {
      clearRememberedApp();
    }
  }

  clearResume.addEventListener('click', clearRememberedApp);

  appCards.forEach(card => {
    card.addEventListener('click', event => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      const appKey = card.dataset.app;
      const route = appRoutes.get(appKey);
      if (!route) return;

      localStorage.setItem(STORAGE_LAST_APP, JSON.stringify({app: appKey, savedAt: Date.now()}));

      // Preserve the Hall of Fame as a true external destination.
      if (route.target === '_blank') return;

      event.preventDefault();
      card.classList.add('is-launching');
      const overlay = document.createElement('div');
      overlay.className = 'launch-overlay';
      overlay.setAttribute('role', 'status');
      overlay.innerHTML = `<strong>Opening ${route.name}</strong>`;
      document.body.appendChild(overlay);
      setTimeout(() => { window.location.assign(route.url); }, reduceMotion ? 50 : 460);
    });
  });

  function restoreArizonaHome() {
    document.querySelectorAll('.launch-overlay').forEach(overlay => overlay.remove());
    document.querySelectorAll('.app-card.is-launching').forEach(card => card.classList.remove('is-launching'));
    showResume();
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        window.scrollTo({top:0,left:0,behavior:'auto'});
        main.focus({preventScroll:true});
      });
    });
  }

  window.addEventListener('pageshow', event => {
    const navigation = performance.getEntriesByType('navigation')[0];
    const returnedByBackButton = event.persisted || navigation?.type === 'back_forward';
    if (returnedByBackButton) restoreArizonaHome();
  });

  showResume();

  let deferredPrompt;
  const installButton = document.getElementById('install-button');
  window.addEventListener('beforeinstallprompt', event => {
    event.preventDefault();
    deferredPrompt = event;
    installButton.hidden = false;
  });
  installButton.addEventListener('click', async () => {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    await deferredPrompt.userChoice;
    deferredPrompt = null;
    installButton.hidden = true;
  });

  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => navigator.serviceWorker.register('./service-worker.js', {updateViaCache:'none'}));
  }
})();
