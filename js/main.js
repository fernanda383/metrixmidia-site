// METRIX MIDIA - MAIN JS

document.addEventListener('DOMContentLoaded', () => {
  const navbar = document.getElementById('navbar');
  const handleScroll = () => {
    if (!navbar) return;
    navbar.classList.toggle('scrolled', window.scrollY > 50);
  };
  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();

  // mobile menu
  const navToggle = document.getElementById('navToggle');
  const navMenu = document.getElementById('navMenu');
  if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
      navToggle.classList.toggle('active');
      navMenu.classList.toggle('active');
      document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
    });
    navMenu.querySelectorAll('.nav-link, .nav-cta').forEach(link => {
      link.addEventListener('click', () => {
        navToggle.classList.remove('active');
        navMenu.classList.remove('active');
        document.body.style.overflow = '';
      });
    });
  }

  // animate-on-scroll
  const animated = document.querySelectorAll('.animate-on-scroll');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -60px 0px' });
  animated.forEach(el => observer.observe(el));

  // active nav link
  const sections = document.querySelectorAll('.section');
  const navLinks = document.querySelectorAll('.nav-link');
  const updateActiveLink = () => {
    const scrollPos = window.scrollY + 200;
    sections.forEach(section => {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      const id = section.getAttribute('id');
      if (scrollPos >= top && scrollPos < top + height) {
        navLinks.forEach(link => {
          link.classList.toggle('active', link.getAttribute('href') === `#${id}`);
        });
      }
    });
  };
  window.addEventListener('scroll', updateActiveLink, { passive: true });
  updateActiveLink();

  // smooth anchors
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const targetId = anchor.getAttribute('href');
      if (targetId === '#') return;
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        const navHeight = navbar ? navbar.offsetHeight : 0;
        const targetPos = target.getBoundingClientRect().top + window.scrollY - navHeight - 12;
        window.scrollTo({ top: targetPos, behavior: 'smooth' });
      }
    });
  });

  // cases hub render
  const caseList = document.getElementById('caseList');
  if (caseList) {
    fetch('/data/cases.json')
      .then(r => r.json())
      .then(cases => {
        caseList.innerHTML = '';
        cases.forEach(item => {
          const card = document.createElement('a');
          card.href = `/case/${item.slug}/`;
          card.className = 'group block p-8 rounded-[2rem] glass-panel card-hover flex flex-col justify-between cursor-pointer';
          card.innerHTML = `
            <div>
              <div class="relative w-full h-48 rounded-[1.5rem] mb-6 overflow-hidden bg-black/50 border border-white/5">
                <img src="${item.thumb}" alt="Thumb ${item.title}" loading="lazy" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105">
                <div class="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent"></div>
              </div>
              <div class="text-[10px] font-medium text-[#F2E846] mb-3 tracking-widest uppercase">${item.segment}</div>
              <div class="text-xl font-medium mb-4 text-white transition-colors leading-snug">${item.title}</div>
              <div class="flex flex-wrap gap-2 mb-6">
                ${item.results.map(r => `<span class="text-xs bg-white/5 border border-white/10 px-2 py-1 rounded-md text-gray-300 font-medium">${r}</span>`).join('')}
              </div>
              <div class="text-xs text-gray-500 mb-6 font-light">${item.tags.join(' • ')}</div>
            </div>
            <div class="mt-auto">
              <span class="inline-block w-full py-3 rounded-full bg-white/5 border border-white/10 text-center text-sm font-medium group-hover:bg-white/10 text-white transition-colors">Ver case detalhado</span>
            </div>`;
          caseList.appendChild(card);
        });
      })
      .catch(() => {
        caseList.innerHTML = '<p class="placeholder">Não foi possível carregar os cases.</p>';
      });
  }
});
