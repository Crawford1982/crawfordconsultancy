(function () {
  'use strict';

  function toggleFaq(btn) {
    var answer = btn.nextElementSibling;
    var isOpen = answer && answer.classList.contains('open');
    document.querySelectorAll('.faq-a').forEach(function (a) {
      a.classList.remove('open');
    });
    document.querySelectorAll('.faq-q').forEach(function (q) {
      q.classList.remove('open');
    });
    if (!isOpen && answer) {
      answer.classList.add('open');
      btn.classList.add('open');
    }
  }
  window.toggleFaq = toggleFaq;

  var navToggle = document.getElementById('nav-toggle');
  var mainNav = document.getElementById('main-nav');
  if (navToggle && mainNav) {
    navToggle.addEventListener('click', function () {
      var open = mainNav.classList.toggle('nav-open');
      navToggle.classList.toggle('open', open);
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        mainNav.classList.remove('nav-open');
        navToggle.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      }
    });
    mainNav.querySelectorAll('.nav-links a').forEach(function (a) {
      a.addEventListener('click', function () {
        mainNav.classList.remove('nav-open');
        navToggle.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  var contactForm = document.getElementById('contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var first = contactForm.querySelector('[name="firstname"]');
      var service = contactForm.querySelector('[name="service"]');
      var message = contactForm.querySelector('[name="message"]');
      var subj = 'Website enquiry' + (first && first.value ? ' from ' + first.value : '');
      var body =
        (service && service.value ? 'Service: ' + service.value + '\n\n' : '') +
        (message && message.value ? message.value : '');
      contactForm.reset();
      window.location.href =
        'mailto:hello@crawfordconsultancy.co.uk?subject=' +
        encodeURIComponent(subj) +
        '&body=' +
        encodeURIComponent(body);
    });
  }

  var COOKIE = 'cc_analytics';
  var GA_ID = 'G-EXKS1Y6D2Y';

  function getCookie(name) {
    var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
  }

  function hideBanner(banner) {
    if (banner) banner.classList.add('hidden');
  }

  function loadGA() {
    window.dataLayer = window.dataLayer || [];
    function gtag() {
      window.dataLayer.push(arguments);
    }
    window.gtag = gtag;
    gtag('js', new Date());
    gtag('config', GA_ID, { send_page_view: true });
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(script);
    document.addEventListener('click', function (e) {
      var el = e.target.closest('a');
      if (!el) return;
      var href = el.href || '';
      var text = (el.innerText || el.textContent || '').trim();
      if (href.indexOf('/contact/') > -1 || text.toLowerCase().indexOf('book a free call') > -1) {
        gtag('event', 'cta_click', {
          event_category: 'CTA',
          event_label: text || 'Book a Free Call',
          page: window.location.pathname
        });
      }
      if (href.indexOf('mailto:') === 0) {
        gtag('event', 'email_click', { event_category: 'Contact', event_label: href });
      }
    });
  }

  var banner = document.getElementById('cookie-banner');
  var accept = document.getElementById('cookie-accept');
  var reject = document.getElementById('cookie-reject');
  var choice = getCookie(COOKIE);

  if (choice === '1') {
    hideBanner(banner);
    loadGA();
  } else if (choice === '0') {
    hideBanner(banner);
  } else {
    if (accept) {
      accept.addEventListener('click', function () {
        document.cookie = COOKIE + '=1; path=/; max-age=31536000; SameSite=Lax';
        hideBanner(banner);
        loadGA();
      });
    }
    if (reject) {
      reject.addEventListener('click', function () {
        document.cookie = COOKIE + '=0; path=/; max-age=31536000; SameSite=Lax';
        hideBanner(banner);
      });
    }
  }
})();
