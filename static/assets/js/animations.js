/**
 * ═══════════════════════════════════════════════════════════════════════════
 * SKILLLENS AI — PREMIUM ANIMATION ENGINE
 * 120fps-Optimized | GPU-Accelerated | Zero-Jank
 * ═══════════════════════════════════════════════════════════════════════════
 */

(function() {
  'use strict';

  // ═══════════════════════════════════════════════════════════════════════════
  // CONFIGURATION
  // ═══════════════════════════════════════════════════════════════════════════
  const CONFIG = {
    animationDuration: 1500,
    counterStep: 20,
    staggerDelay: 100,
    easing: 'cubic-bezier(0.34, 1.56, 0.64, 1)'
  };

  // ═══════════════════════════════════════════════════════════════════════════
  // DRAG & DROP UPLOAD
  // ═══════════════════════════════════════════════════════════════════════════
  function initDragDrop() {
    const uploadCard = document.querySelector('.sl-upload-card');
    const fileInput = document.getElementById('resumeFile');
    
    if (!uploadCard || !fileInput) return;

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      uploadCard.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
      e.preventDefault();
      e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
      uploadCard.addEventListener(eventName, () => {
        uploadCard.classList.add('dragging');
      }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      uploadCard.addEventListener(eventName, () => {
        uploadCard.classList.remove('dragging');
      }, false);
    });

    uploadCard.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      const files = dt.files;
      if (files.length) {
        fileInput.files = files;
        handleFileUpload(files[0]);
      }
    }, false);

    fileInput.addEventListener('change', (e) => {
      if (e.target.files.length) {
        handleFileUpload(e.target.files[0]);
      }
    });
  }

  function handleFileUpload(file) {
    const uploadCard = document.querySelector('.sl-upload-card');
    const icon = uploadCard.querySelector('.sl-upload-icon');
    
    // Animate upload confirmation
    uploadCard.classList.add('analyzing');
    icon.innerHTML = '<div class="sl-scan-line"></div>⚡';
    
    // Create ripple effect
    createRipple(uploadCard, event);
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // TYPING PLACEHOLDER ANIMATION
  // ═══════════════════════════════════════════════════════════════════════════
  function typeWriter(element, text, speed = 50) {
    let i = 0;
    element.placeholder = '';
    
    function type() {
      if (i < text.length) {
        element.placeholder += text.charAt(i);
        i++;
        setTimeout(type, speed);
      }
    }
    
    type();
  }

  function initTypingPlaceholder() {
    const textarea = document.getElementById('jdText');
    if (textarea && !textarea.dataset.typed) {
      textarea.dataset.typed = 'true';
      const placeholderText = 'Paste the job description here...';
      
      setTimeout(() => {
        typeWriter(textarea, placeholderText, 40);
      }, 1000);
    }
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // CHARACTER COUNTER
  // ═══════════════════════════════════════════════════════════════════════════
  function initCharCounter() {
    const textarea = document.getElementById('jdText');
    const inputGroup = textarea?.parentElement;
    
    if (!textarea || !inputGroup) return;

    const counter = document.createElement('div');
    counter.className = 'sl-char-counter';
    counter.textContent = '0 characters';
    inputGroup.appendChild(counter);

    textarea.addEventListener('input', () => {
      const length = textarea.value.length;
      counter.textContent = `${length.toLocaleString()} character${length !== 1 ? 's' : ''}`;
    });
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // BUTTON RIPPLE EFFECT
  // ═══════════════════════════════════════════════════════════════════════════
  function createRipple(button, event) {
    const circle = document.createElement('span');
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;

    const rect = button.getBoundingClientRect();
    const x = (event?.clientX || rect.left + rect.width / 2) - rect.left - radius;
    const y = (event?.clientY || rect.top + rect.height / 2) - rect.top - radius;

    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${x}px`;
    circle.style.top = `${y}px`;
    circle.style.position = 'absolute';
    circle.style.borderRadius = '50%';
    circle.style.background = 'rgba(255, 255, 255, 0.3)';
    circle.style.transform = 'scale(0)';
    circle.style.animation = 'ripple 600ms ease-out';
    circle.style.pointerEvents = 'none';

    const ripple = button.querySelector('.ripple');
    if (ripple) {
      ripple.remove();
    }

    circle.classList.add('ripple');
    button.style.position = 'relative';
    button.style.overflow = 'hidden';
    button.appendChild(circle);

    setTimeout(() => circle.remove(), 600);
  }

  function initButtonRipples() {
    const buttons = document.querySelectorAll('.sl-btn-primary, .sl-upload-card');
    buttons.forEach(button => {
      button.addEventListener('click', (e) => {
        createRipple(button, e);
      });
    });
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // SMOOTH NUMBER COUNTING
  // ═══════════════════════════════════════════════════════════════════════════
  function animateValue(element, start, end, duration, suffix = '') {
    const range = end - start;
    const increment = range / (duration / CONFIG.counterStep);
    let current = start;
    const timer = setInterval(() => {
      current += increment;
      if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
        current = end;
        clearInterval(timer);
      }
      element.textContent = Math.round(current) + suffix;
    }, CONFIG.counterStep);
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // INTERSECTION OBSERVER — SCROLL ANIMATIONS
  // ═══════════════════════════════════════════════════════════════════════════
  function initScrollAnimations() {
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            observer.unobserve(entry.target);
          }
        });
      }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
      });

      document.querySelectorAll('[data-animate]').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
      });
    }
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // FLOATING LABEL EFFECT
  // ═══════════════════════════════════════════════════════════════════════════
  function initFloatingLabels() {
    const inputGroups = document.querySelectorAll('.sl-input-group');
    
    inputGroups.forEach(group => {
      const input = group.querySelector('textarea, input');
      const label = group.querySelector('label');
      
      if (!input || !label) return;

      input.addEventListener('focus', () => {
        label.style.transform = 'translateY(-4px)';
        label.style.color = 'var(--sl-cyan-400)';
      });

      input.addEventListener('blur', () => {
        if (!input.value) {
          label.style.transform = 'translateY(0)';
          label.style.color = 'var(--sl-text-secondary)';
        }
      });
    });
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // PARALLAX MOUSE EFFECT
  // ═══════════════════════════════════════════════════════════════════════════
  function initParallax() {
    const hero = document.querySelector('.sl-hero');
    const logo = document.querySelector('.sl-logo-container');
    
    if (!hero || !logo) return;

    let rafId;
    
    hero.addEventListener('mousemove', (e) => {
      if (rafId) return;
      
      rafId = requestAnimationFrame(() => {
        const { clientX, clientY } = e;
        const { left, top, width, height } = hero.getBoundingClientRect();
        
        const x = (clientX - left) / width - 0.5;
        const y = (clientY - top) / height - 0.5;
        
        logo.style.transform = `translate(${x * 20}px, ${y * 20}px) scale(1.02)`;
        rafId = null;
      });
    });

    hero.addEventListener('mouseleave', () => {
      logo.style.transform = 'translate(0, 0) scale(1)';
    });
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // PERFORMANCE OPTIMIZATION
  // ═══════════════════════════════════════════════════════════════════════════
  function optimizePerformance() {
    // Reduce animations on low-end devices
    if (navigator.hardwareConcurrency <= 4) {
      document.body.style.setProperty('--sl-duration-slow', '200ms');
      document.body.style.setProperty('--sl-duration-slower', '300ms');
    }

    // Disable animations on battery saver mode
    if ('getBattery' in navigator) {
      navigator.getBattery().then(battery => {
        if (!battery.charging && battery.level < 0.2) {
          document.body.classList.add('power-saver-mode');
        }
      });
    }

    // Respect prefers-reduced-motion
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (prefersReducedMotion.matches) {
      document.body.classList.add('reduced-motion');
    }
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // LOADING STATE MANAGEMENT
  // ═══════════════════════════════════════════════════════════════════════════
  function enhanceLoadingState() {
    const form = document.getElementById('analyzeForm');
    const button = form?.querySelector('.sl-btn-primary');
    
    if (!form || !button) return;

    form.addEventListener('submit', () => {
      button.classList.add('loading');
      button.disabled = true;
      
      const btnText = button.querySelector('.sl-btn-text') || button.childNodes[0];
      if (btnText) {
        btnText.textContent = 'Analyzing...';
      }
    });
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // INITIALIZATION
  // ═══════════════════════════════════════════════════════════════════════════
  function init() {
    // Wait for DOM to be fully loaded
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', init);
      return;
    }

    // Initialize all features
    optimizePerformance();
    // initDragDrop(); // Handled in index.html
    initTypingPlaceholder();
    // initCharCounter(); // Handled in index.html
    initButtonRipples();
    initScrollAnimations();
    initFloatingLabels();
    initParallax();
    // enhanceLoadingState(); // Handled in index.html

    console.log('✨ SkillLens AI animations initialized');
  }

  // Add ripple animation to stylesheet
  const style = document.createElement('style');
  style.textContent = `
    @keyframes ripple {
      to {
        transform: scale(4);
        opacity: 0;
      }
    }
    
    .power-saver-mode * {
      animation-duration: 0.1s !important;
      transition-duration: 0.1s !important;
    }
    
    .reduced-motion * {
      animation-duration: 0.01ms !important;
      transition-duration: 0.01ms !important;
    }
  `;
  document.head.appendChild(style);

  // Start initialization
  init();

  // Export for manual re-initialization if needed
  window.SkillLensAnimations = { init };

})();
