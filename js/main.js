/* ========== ANDRÉS PÉREZ CORONADO — MAIN JS ==========
   Forked from web_site_fastanalytics/js/main.js on 2026-07-05.
   Changes: (1) per-page titles read from window.PAGE_TITLES instead of a hardcoded
   single-site dictionary, (2) defensive null-guards around nav elements so a markup
   slip on one page can't break the script on every page. */

(function () {
  'use strict';

  // ========== LANGUAGE TOGGLE ==========
  const langToggle = document.getElementById('langToggle');
  let currentLang = 'es';

  if (langToggle) {
    var langOptions = langToggle.querySelectorAll('.lang-option');

    var setLanguage = function (lang) {
      currentLang = lang;
      document.documentElement.lang = lang;

      // Update toggle buttons
      langOptions.forEach(function (opt) {
        opt.classList.toggle('active', opt.dataset.lang === lang);
      });

      // Update all translatable elements
      document.querySelectorAll('[data-' + lang + ']').forEach(function (el) {
        var text = el.getAttribute('data-' + lang);
        if (text) {
          el.innerHTML = text;
        }
      });

      // Update page title (each page defines window.PAGE_TITLES = {es, en, fr} before this script)
      var titles = window.PAGE_TITLES || {
        es: 'Andrés Pérez Coronado',
        en: 'Andrés Pérez Coronado',
        fr: 'Andrés Pérez Coronado'
      };
      document.title = titles[lang] || titles.es;
    };

    var langCycle = ['es', 'en', 'fr'];

    langToggle.addEventListener('click', function (e) {
      var option = e.target.closest('.lang-option');
      if (option) {
        setLanguage(option.dataset.lang);
      } else {
        // Cycle through languages
        var idx = langCycle.indexOf(currentLang);
        setLanguage(langCycle[(idx + 1) % langCycle.length]);
      }
    });
  }

  // ========== NAVBAR SCROLL ==========
  var navbar = document.getElementById('navbar');
  if (navbar) {
    window.addEventListener('scroll', function () {
      navbar.classList.toggle('scrolled', window.scrollY > 20);
    }, { passive: true });
  }

  // ========== MOBILE MENU ==========
  var hamburger = document.getElementById('hamburger');
  var navLinks = document.getElementById('navLinks');

  if (hamburger && navLinks) {
    hamburger.addEventListener('click', function () {
      hamburger.classList.toggle('active');
      navLinks.classList.toggle('active');
      document.body.style.overflow = navLinks.classList.contains('active') ? 'hidden' : '';
    });

    // Close mobile menu on link click
    navLinks.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        hamburger.classList.remove('active');
        navLinks.classList.remove('active');
        document.body.style.overflow = '';
      });
    });
  }

  // ========== SMOOTH SCROLL (same-page anchors only) ==========
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var href = this.getAttribute('href');
      if (href === '#') return;
      var target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        var navHeight = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--nav-height'));
        var targetPosition = target.getBoundingClientRect().top + window.scrollY - navHeight;
        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });
      }
    });
  });

  // ========== SCROLL ANIMATIONS ==========
  var animatedElements = document.querySelectorAll('.animate-on-scroll');

  if (animatedElements.length) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -40px 0px'
    });

    animatedElements.forEach(function (el) {
      observer.observe(el);
    });
  }

  // ========== ACTIVE NAV LINK ON SCROLL ==========
  var sections = document.querySelectorAll('section[id]');

  if (navLinks && sections.length) {
    var sectionObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var id = entry.target.id;
          navLinks.querySelectorAll('a').forEach(function (link) {
            link.classList.toggle('active', link.getAttribute('href') === '#' + id);
          });
        }
      });
    }, {
      threshold: 0.3,
      rootMargin: '-80px 0px -50% 0px'
    });

    sections.forEach(function (section) {
      sectionObserver.observe(section);
    });
  }

  // ========== LIGHTBOX ==========
  var lightbox = document.getElementById('lightbox');
  if (lightbox) {
    var lightboxImage = document.getElementById('lightboxImage');
    var lightboxClose = document.getElementById('lightboxClose');
    var lightboxPrev = document.getElementById('lightboxPrev');
    var lightboxNext = document.getElementById('lightboxNext');
    var lightboxCounter = document.getElementById('lightboxCounter');

    var currentGallery = [];
    var currentIndex = 0;

    function updateLightbox() {
      var img = currentGallery[currentIndex];
      lightboxImage.src = img.src;
      lightboxImage.alt = img.alt || '';
      lightboxCounter.textContent = (currentIndex + 1) + ' / ' + currentGallery.length;
      var multiple = currentGallery.length > 1;
      lightboxPrev.style.display = multiple ? 'flex' : 'none';
      lightboxNext.style.display = multiple ? 'flex' : 'none';
      lightboxCounter.style.display = multiple ? 'block' : 'none';
    }

    function openLightbox(gallery, index) {
      currentGallery = gallery;
      currentIndex = index;
      updateLightbox();
      lightbox.classList.add('active');
      lightbox.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
      lightbox.classList.remove('active');
      lightbox.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }

    function prevImage() {
      currentIndex = (currentIndex - 1 + currentGallery.length) % currentGallery.length;
      updateLightbox();
    }

    function nextImage() {
      currentIndex = (currentIndex + 1) % currentGallery.length;
      updateLightbox();
    }

    var gallerySelectors = ['.alejo-screenshots', '.vigia-screenshots', '.tavodebate-screenshots'];
    gallerySelectors.forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (gallery) {
        var images = Array.prototype.slice.call(gallery.querySelectorAll('img'));
        images.forEach(function (img, idx) {
          img.addEventListener('click', function () {
            openLightbox(images, idx);
          });
        });
      });
    });

    lightboxClose.addEventListener('click', closeLightbox);
    lightboxPrev.addEventListener('click', prevImage);
    lightboxNext.addEventListener('click', nextImage);

    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox) {
        closeLightbox();
      }
    });

    document.addEventListener('keydown', function (e) {
      if (!lightbox.classList.contains('active')) return;
      if (e.key === 'Escape') closeLightbox();
      else if (e.key === 'ArrowLeft') prevImage();
      else if (e.key === 'ArrowRight') nextImage();
    });
  }

  // ========== RESULTS CAROUSEL ==========
  var track = document.querySelector('.results-track');
  if (track) {
    var slides = track.querySelectorAll('.result-slide');
    var dots = document.querySelectorAll('.results-dot');
    var prevBtn = document.querySelector('.results-prev');
    var nextBtn = document.querySelector('.results-next');
    var total = slides.length;
    var current = 0;

    var goTo = function (i) {
      current = (i + total) % total;
      track.style.transform = 'translateX(-' + (current * 100) + '%)';
      dots.forEach(function (dot, idx) { dot.classList.toggle('active', idx === current); });
    };

    if (prevBtn) prevBtn.addEventListener('click', function () { goTo(current - 1); });
    if (nextBtn) nextBtn.addEventListener('click', function () { goTo(current + 1); });
    dots.forEach(function (dot, idx) {
      dot.addEventListener('click', function () { goTo(idx); });
    });

    var timer = setInterval(function () { goTo(current + 1); }, 5000);
    var carousel = track.closest('.results-carousel');
    carousel.addEventListener('mouseenter', function () { clearInterval(timer); });
    carousel.addEventListener('mouseleave', function () { timer = setInterval(function () { goTo(current + 1); }, 5000); });

    var startX = 0;
    track.addEventListener('touchstart', function (e) { startX = e.touches[0].clientX; clearInterval(timer); }, { passive: true });
    track.addEventListener('touchend', function (e) {
      var diff = startX - e.changedTouches[0].clientX;
      if (Math.abs(diff) > 50) goTo(current + (diff > 0 ? 1 : -1));
      timer = setInterval(function () { goTo(current + 1); }, 5000);
    }, { passive: true });
  }

})();
