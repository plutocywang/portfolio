(() => {
  'use strict';
  document.documentElement.classList.remove('no-js');
  const menuButton = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.main-nav');
  const workMenu = document.querySelector('.work-menu');
  const workTrigger = workMenu?.querySelector('summary');
  function closeWorkMenu(restoreFocus = false) {
    if (workMenu) workMenu.open = false;
    if (restoreFocus) workTrigger?.focus();
  }
  function closeMenu(restoreFocus = false) {
    closeWorkMenu();
    nav?.classList.remove('open');
    menuButton?.setAttribute('aria-expanded', 'false');
    if (menuButton) menuButton.querySelector('.menu-label').textContent = 'Menu';
    if (restoreFocus) menuButton?.focus();
  }
  menuButton?.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.querySelector('.menu-label').textContent = open ? 'Close' : 'Menu';
    nav.classList.toggle('open', open);
  });
  nav?.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    if (workMenu?.open) closeWorkMenu(true);
    else if (nav?.classList.contains('open')) closeMenu(true);
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.site-header')) closeMenu();
  });
  matchMedia('(min-width: 641px)').addEventListener('change', event => { if(event.matches) closeMenu(); });
  workMenu?.addEventListener('pointerenter', event => {
    if (event.pointerType === 'mouse' && matchMedia('(min-width: 641px)').matches) workMenu.open = true;
  });
  workMenu?.addEventListener('pointerleave', event => {
    if (event.pointerType === 'mouse' && matchMedia('(min-width: 641px)').matches) closeWorkMenu();
  });
  workMenu?.addEventListener('focusout', event => {
    if (!workMenu.contains(event.relatedTarget)) closeWorkMenu();
  });

  const grid = document.querySelector('#project-grid');
  const filters = [...document.querySelectorAll('.filter-button')];
  if (grid && filters.length) {
    const cards = [...grid.querySelectorAll('.project-card')];
    const status = document.querySelector('#work-count');
    const selectedOrder = grid.dataset.selectedOrder.split(',');
    const allButton = document.querySelector('#view-all');
    document.querySelector('.filter-bar').hidden = false;
    allButton.hidden = false;
    function filterWork(value, updateUrl = false) {
      if (!filters.some(button => button.dataset.filter === value)) value = 'selected';
      filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === value)));
      document.querySelectorAll('[data-work-filter]').forEach(link => {
        if (link.dataset.workFilter === value) link.setAttribute('aria-current', 'true');
        else link.removeAttribute('aria-current');
      });
      grid.dataset.view = value;
      let visible = 0;
      const ordered = [...cards].sort((a,b) => value === 'selected' ? (selectedOrder.indexOf(a.dataset.slug) < 0 ? 999 : selectedOrder.indexOf(a.dataset.slug)) - (selectedOrder.indexOf(b.dataset.slug) < 0 ? 999 : selectedOrder.indexOf(b.dataset.slug)) : Number(a.dataset.order) - Number(b.dataset.order));
      grid.replaceChildren(...ordered);
      ordered.forEach(card => {
        const show = value === 'all' || (value === 'selected' ? card.dataset.selected === 'true' : card.dataset.category === value);
        card.hidden = !show;

        if (show) visible++;
      });
      status.textContent = `${String(visible).padStart(2, '0')} ${value === 'selected' ? 'selected projects' : 'projects'} / ${String(cards.length).padStart(2, '0')} in the archive`;
      allButton.textContent = value === 'all' ? 'Back to selected work ↗' : `Explore all ${cards.length} projects ↗`;
      allButton.dataset.target = value === 'all' ? 'selected' : 'all';
      if (updateUrl) {
        const url = new URL(location.href);
        if (value === 'selected') url.searchParams.delete('view'); else url.searchParams.set('view', value);
        url.hash = 'work';
        history.pushState({}, '', url);
      }
    }
    filters.forEach(button => button.addEventListener('click', () => filterWork(button.dataset.filter, true)));
    document.querySelectorAll('[data-work-filter]').forEach(link => {
      link.addEventListener('click', event => {
        if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        const value = link.dataset.workFilter;
        filterWork(value, true);
        closeMenu();
        document.querySelector('#work').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
        filters.find(button => button.dataset.filter === value)?.focus({preventScroll:true});
      });
    });
    allButton.addEventListener('click', () => {
      filterWork(allButton.dataset.target, true);
      document.querySelector('#work').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
      filters.find(button => button.getAttribute('aria-pressed') === 'true').focus({preventScroll:true});
    });
    const restoreFilter = () => filterWork(new URL(location.href).searchParams.get('view') || 'selected');
    addEventListener('popstate', restoreFilter);
    restoreFilter();
  }

  document.querySelectorAll('[data-video-id]').forEach(button => {
    button.addEventListener('click', () => {
      const shell = button.closest('.video-shell');
      const iframe = document.createElement('iframe');
      const url = new URL(`https://www.youtube-nocookie.com/embed/${button.dataset.videoId}`);
      url.searchParams.set('autoplay', '1');
      url.searchParams.set('rel', '0');
      url.searchParams.set('playsinline', '1');
      url.searchParams.set('origin', location.origin);
      iframe.src = url.href;
      iframe.title = button.dataset.videoTitle;
      iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
      iframe.allowFullscreen = true;
      iframe.referrerPolicy = 'strict-origin-when-cross-origin';
      shell.replaceChildren(iframe);
      iframe.focus();
    });
  });

  document.querySelectorAll('.copy-email').forEach(button => {
    button.hidden = false;
    button.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText('pluto.cywang@gmail.com');
        button.textContent = 'Copied ✓';
      } catch {
        button.textContent = 'Select email to copy';
        const email = document.querySelector('.contact-email a');
        const selection = getSelection();
        if (selection && email) {const range = document.createRange();range.selectNodeContents(email);selection.removeAllRanges();selection.addRange(range);}
      }
      clearTimeout(button.resetTimer);
      button.resetTimer = setTimeout(() => {button.textContent = 'Copy email';}, 3000);
    });
  });
  document.querySelectorAll('[data-year]').forEach(el => {el.textContent = new Date().getFullYear();});
  if ('IntersectionObserver' in window) {
    const sections = [...document.querySelectorAll('section[id="work"],section[id="about"],section[id="contact"]')];
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if(entry.isIntersecting) nav?.querySelectorAll(':scope > a, .work-trigger').forEach(a => {
          if(a.hash === `#${entry.target.id}` || (a === workTrigger && entry.target.id === 'work')) a.setAttribute('aria-current','location');
          else a.removeAttribute('aria-current');
        });
      });
    }, {rootMargin:'-15% 0px -65% 0px'});
    sections.forEach(section => observer.observe(section));
  }
})();
