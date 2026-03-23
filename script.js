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
async function handleSubmit(e) {
  e.preventDefault();
  const form    = e.target;
  const btn     = form.querySelector('button[type="submit"]');
  const success = document.getElementById('formSuccess');
  const error   = document.getElementById('formError');

  btn.textContent = 'Sending\u2026';
  btn.disabled = true;
  if (error) error.classList.remove('visible');

  try {
    const response = await fetch('https://formspree.io/f/xpqygnpq', {
      method:  'POST',
      headers: { 'Accept': 'application/json' },
      body:    new FormData(form)
    });

    if (response.ok) {
      form.reset();
      btn.style.display = 'none';
      success.classList.add('visible');
    } else {
      const data = await response.json();
      throw new Error(data.errors ? data.errors.map(err => err.message).join(', ') : 'Submission failed');
    }
  } catch (err) {
    btn.textContent = 'Send Message \u2192';
    btn.disabled = false;
    if (error) {
      error.textContent = 'Sorry, something went wrong. Please email us directly at hello@d2csoftware.com';
      error.classList.add('visible');
    }
  }
}
