/* ─── STICKY NAV SHADOW ──────────────────────────────────────── */
const navWrapper = document.querySelector('.nav-wrapper');
window.addEventListener('scroll', () => {
  navWrapper.style.boxShadow = window.scrollY > 20
    ? '0 4px 32px rgba(0,0,0,0.5)'
    : 'none';
});

/* ─── SCROLL FADE-IN ─────────────────────────────────────────── */
const fadeEls = document.querySelectorAll('.service-card, .exp-badge, .contact-form');
fadeEls.forEach(el => el.classList.add('fade-in'));

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      const idx = Array.from(fadeEls).indexOf(entry.target);
      setTimeout(() => entry.target.classList.add('visible'), 80 * (idx % 5));
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -32px 0px' });

fadeEls.forEach(el => observer.observe(el));

/* ─── CONTACT FORM ───────────────────────────────────────────── */
function handleSubmit(e) {
  e.preventDefault();
  const btn = e.target.querySelector('button[type="submit"]');
  const success = document.getElementById('formSuccess');
  btn.textContent = 'Sending...';
  btn.disabled = true;
  setTimeout(() => {
    e.target.reset();
    btn.style.display = 'none';
    success.classList.add('visible');
  }, 1200);
}
