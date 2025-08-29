const tabs = Array.from(document.querySelectorAll('.tab'));
const panels = Array.from(document.querySelectorAll('.panel'));

function activateTab(tab) {
  tabs.forEach(t => {
    const isActive = t === tab;
    t.classList.toggle('is-active', isActive);
    t.setAttribute('aria-selected', String(isActive));
    const targetId = t.getAttribute('aria-controls');
    const panel = document.getElementById(targetId);
    if (panel) {
      panel.hidden = !isActive;
      panel.classList.toggle('is-active', isActive);
    }
  });
}

tabs.forEach(t => {
  t.addEventListener('click', () => activateTab(t));
  t.addEventListener('keydown', e => {
    const idx = tabs.indexOf(t);
    if (e.key === 'ArrowRight') {
      e.preventDefault();
      const next = tabs[(idx + 1) % tabs.length];
      next.focus();
      activateTab(next);
    }
    if (e.key === 'ArrowLeft') {
      e.preventDefault();
      const prev = tabs[(idx - 1 + tabs.length) % tabs.length];
      prev.focus();
      activateTab(prev);
    }
  });
});


