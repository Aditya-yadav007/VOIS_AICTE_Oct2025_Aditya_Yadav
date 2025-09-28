// VOIS AICTE Oct2025 · Landing Page Scripts
// Interactivity: mobile nav, smooth scroll, sample chart, dynamic year
(function(){
  const qs = (s,root=document)=>root.querySelector(s);
  const qsa = (s,root=document)=>Array.from(root.querySelectorAll(s));

  // Mobile nav toggle
  const toggle = qs('.nav__toggle');
  const menu = qs('.nav__menu');
  if (toggle && menu){
    toggle.addEventListener('click', ()=>{
      const expanded = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!expanded));
      menu.classList.toggle('show');
    });
    // Close menu when a link is clicked (mobile)
    qsa('a', menu).forEach(a=>a.addEventListener('click', ()=>{
      menu.classList.remove('show');
      toggle.setAttribute('aria-expanded','false');
    }));
  }

  // Smooth scroll offset for sticky header
  qsa('a[href^="#"]').forEach(link=>{
    link.addEventListener('click', (e)=>{
      const href = link.getAttribute('href');
      if (!href || href === '#' || href.startsWith('#') === false) return;
      const target = qs(href);
      if (target){
        e.preventDefault();
        const header = qs('.site-header');
        const top = target.getBoundingClientRect().top + window.scrollY - (header?.offsetHeight || 0) - 8;
        window.scrollTo({top, behavior:'smooth'});
      }
    });
  });

  // Dynamic year
  const yearEl = qs('#year');
  if (yearEl){ yearEl.textContent = String(new Date().getFullYear()); }

  // Sample Chart.js line chart in hero
  const ctx = qs('#heroChart');
  if (ctx && window.Chart){
    const gradient = ctx.getContext('2d').createLinearGradient(0,0,0,180);
    gradient.addColorStop(0, 'rgba(90,209,232,0.35)');
    gradient.addColorStop(1, 'rgba(90,209,232,0.02)');

    new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
        datasets: [{
          label: 'Avg Price Index',
          data: [82, 86, 90, 88, 96, 110, 124, 120, 112, 106, 98, 92],
          borderColor: '#5ad1e8',
          backgroundColor: gradient,
          tension: 0.35,
          pointRadius: 2,
          fill: true,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { intersect:false, mode:'index' }
        },
        scales: {
          x: { grid: { color: 'rgba(255,255,255,0.06)' }, ticks: { color: '#a9b0c7' } },
          y: { grid: { color: 'rgba(255,255,255,0.06)' }, ticks: { color: '#a9b0c7' } }
        }
      }
    });
    // Auto-size container height
    const card = ctx.closest('.chart-card');
    if (card){ card.style.height = '240px'; }
  }
})();
