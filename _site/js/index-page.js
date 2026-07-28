/* Externalized from index.html inline script (CSP: script-src 'self'). */
function showTab(e, name) {
        document.querySelectorAll('.media-panel').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.media-tabs button').forEach(b => b.classList.remove('active'));
        document.getElementById('tab-' + name).classList.add('active');
        e.currentTarget.classList.add('active');
    }
    // Hamburger menu: toggle aria-expanded
    document.querySelector('.menu-btn').addEventListener('click', function() {
        const expanded = this.getAttribute('aria-expanded') === 'true';
        this.setAttribute('aria-expanded', !expanded);
    });
    // Scroll-based nav highlighting
    const sections = document.querySelectorAll('section[id], div[id]');
    const navLinks = document.querySelectorAll('.nav-links a:not(.nav-art-link)');
    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(s => { if (window.scrollY >= s.offsetTop - 100) current = s.id; });
        navLinks.forEach(a => { a.classList.toggle('active', a.getAttribute('href') === '#' + current); });
    });
    // Animate on scroll (respects prefers-reduced-motion)
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (!prefersReducedMotion.matches) {
        const observer = new IntersectionObserver(entries => {
            entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('animate'); });
        }, { threshold: 0.08 });
        document.querySelectorAll('.card,.stat,.pub-item,.art-card,.connect-card').forEach(el => observer.observe(el));
    }
    <!-- Service Worker registration -->
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js').catch(() => {});
        }
