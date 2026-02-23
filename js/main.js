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
          const card = document.createElement('article');
          card.className = 'case-card';
          card.innerHTML = `
            <div class="case-thumb">
              <img src="${item.thumb}" alt="Thumb ${item.title}" loading="lazy" onerror="this.style.display='none'">
            </div>
            <div class="case-body">
              <div class="case-title">${item.title}</div>
              <div class="case-segment">${item.segment}</div>
              <div class="case-results">${item.results.map(r => `<span class='badge'>${r}</span>`).join('')}</div>
              <div class="tag">${item.tags.join(' • ')}</div>
            </div>
            <div class="case-footer">
              <a class="btn btn-outline" href="/case/${item.slug}/">Ver case</a>
            </div>`;
          caseList.appendChild(card);
        });
      })
      .catch(() => {
        caseList.innerHTML = '<p class="placeholder">Não foi possível carregar os cases.</p>';
      });
  }
});
