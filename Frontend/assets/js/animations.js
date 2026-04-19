/**
 * ═══════════════════════════════════════════════════════════════════════════
 * SKILLLENS AI — Premium Animations Engine
 * Lightweight, GPU-accelerated, 120fps-smooth animations
 * Zero dependencies, performance-first design
 * ═══════════════════════════════════════════════════════════════════════════
 */

(function() {
  'use strict';

  // ═══════════════════════════════════════════════════════════════════════════
  // CONFIGURATION
  // ═══════════════════════════════════════════════════════════════════════════
  
  const CONFIG = {
    // Animation settings
    SCORE_ANIMATION_DURATION: 1500,    // ms
    PROGRESS_ANIMATION_DURATION: 1200, // ms
    FADE_IN_DURATION: 600,             // ms
    STAGGER_DELAY: 100,                // ms
    
    // Performance
    USE_RAF: true,                     // Use requestAnimationFrame
    RESPECT_REDUCED_MOTION: true,      // Accessibility
    
    // Easing functions
    EASING: {
      easeOutExpo: (t) => t === 1 ? 1 : 1 - Math.pow(2, -10 * t),
      easeOutQuart: (t) => 1 - Math.pow(1 - t, 4),
      easeOutCubic: (t) => 1 - Math.pow(1 - t, 3),
      easeInOutQuad: (t) => t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2,
      spring: (t) => 1 - Math.cos(t * Math.PI * 0.5) * Math.exp(-t * 3)
    }
  };

  // ═══════════════════════════════════════════════════════════════════════════
  // UTILITY FUNCTIONS
  // ═══════════════════════════════════════════════════════════════════════════

  /**
   * Check if user prefers reduced motion
   */
  function prefersReducedMotion() {
    return CONFIG.RESPECT_REDUCED_MOTION && 
           window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  /**
   * Clamp a value between min and max
   */
  function clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
  }

  /**
   * Create a debounced function
   */
  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  /**
   * Create a throttled function using RAF
   */
  function throttleRAF(func) {
    let rafId = null;
    return function(...args) {
      if (rafId) return;
      rafId = requestAnimationFrame(() => {
        func.apply(this, args);
        rafId = null;
      });
    };
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // CORE ANIMATION ENGINE
  // ═══════════════════════════════════════════════════════════════════════════

  /**
   * Animate a value from start to end
   * @param {Object} options - Animation options
   * @returns {Function} Cancel function
   */
  function animate(options) {
    const {
      from = 0,
      to = 100,
      duration = 1000,
      easing = CONFIG.EASING.easeOutExpo,
      onUpdate = () => {},
      onComplete = () => {}
    } = options;

    if (prefersReducedMotion()) {
      onUpdate(to);
      onComplete();
      return () => {};
    }

    let startTime = null;
    let rafId = null;
    let cancelled = false;

    function step(timestamp) {
      if (cancelled) return;
      
      if (!startTime) startTime = timestamp;
      const elapsed = timestamp - startTime;
      const progress = clamp(elapsed / duration, 0, 1);
      const easedProgress = easing(progress);
      const currentValue = from + (to - from) * easedProgress;

      onUpdate(currentValue);

      if (progress < 1) {
        rafId = requestAnimationFrame(step);
      } else {
        onUpdate(to);
        onComplete();
      }
    }

    rafId = requestAnimationFrame(step);

    // Return cancel function
    return () => {
      cancelled = true;
      if (rafId) cancelAnimationFrame(rafId);
    };
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // SCORE COUNTER ANIMATION
  // ═══════════════════════════════════════════════════════════════════════════

  /**
   * Animate a score counter with count-up effect
   * @param {HTMLElement} element - The element to animate
   * @param {number} targetScore - Target score value (0-100)
   * @param {Object} options - Animation options
   */
  function animateScoreCounter(element, targetScore, options = {}) {
    if (!element) return;

    const {
      duration = CONFIG.SCORE_ANIMATION_DURATION,
      suffix = '',
      prefix = '',
      decimals = 0
    } = options;

    const startValue = 0;
    const endValue = clamp(targetScore, 0, 100);

    animate({
      from: startValue,
      to: endValue,
      duration,
      easing: CONFIG.EASING.easeOutExpo,
      onUpdate: (value) => {
        element.textContent = prefix + value.toFixed(decimals) + suffix;
      }
    });
  }

  /**
   * Animate circular progress (SVG)
   * @param {SVGCircleElement} circle - The SVG circle element
   * @param {number} percentage - Target percentage (0-100)
   * @param {Object} options - Animation options
   */
  function animateCircularProgress(circle, percentage, options = {}) {
    if (!circle) return;

    const {
      duration = CONFIG.PROGRESS_ANIMATION_DURATION,
      radius = 90
    } = options;

    const circumference = 2 * Math.PI * radius;
    const targetOffset = circumference - (percentage / 100) * circumference;

    // Set initial state
    circle.style.strokeDasharray = circumference;
    circle.style.strokeDashoffset = circumference;

    animate({
      from: circumference,
      to: targetOffset,
      duration,
      easing: CONFIG.EASING.easeOutQuart,
      onUpdate: (value) => {
        circle.style.strokeDashoffset = value;
      }
    });
  }

  /**
   * Animate linear progress bar
   * @param {HTMLElement} bar - The progress bar fill element
   * @param {number} percentage - Target percentage (0-100)
   * @param {Object} options - Animation options
   */
  function animateProgressBar(bar, percentage, options = {}) {
    if (!bar) return;

    const {
      duration = CONFIG.PROGRESS_ANIMATION_DURATION
    } = options;

    bar.style.transformOrigin = 'left';
    bar.style.transform = 'scaleX(0)';

    animate({
      from: 0,
      to: percentage / 100,
      duration,
      easing: CONFIG.EASING.easeOutQuart,
      onUpdate: (value) => {
        bar.style.transform = `scaleX(${value})`;
      }
    });
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // INTERSECTION OBSERVER FOR SCROLL ANIMATIONS
  // ═══════════════════════════════════════════════════════════════════════════

  /**
   * Initialize scroll-triggered animations
   */
  function initScrollAnimations() {
    if (!('IntersectionObserver' in window)) return;

    const animatedElements = document.querySelectorAll('[data-sl-animate]');
    if (!animatedElements.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const el = entry.target;
            const animation = el.dataset.slAnimate || 'fade-in-up';
            const delay = parseInt(el.dataset.slDelay || '0', 10);

            setTimeout(() => {
              el.classList.add('sl-animated', `sl-animate-${animation}`);
            }, delay);

            observer.unobserve(el);
          }
        });
      },
      {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
      }
    );

    animatedElements.forEach((el) => observer.observe(el));
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // STAGGER ANIMATIONS
  // ═══════════════════════════════════════════════════════════════════════════

  /**
   * Animate a list of elements with staggered timing
   * @param {NodeList|Array} elements - Elements to animate
   * @param {string} animationClass - CSS class to add
   * @param {Object} options - Animation options
   */
  function animateStaggered(elements, animationClass, options = {}) {
    if (!elements || !elements.length) return;

    const {
      staggerDelay = CONFIG.STAGGER_DELAY,
      initialDelay = 0
    } = options;

    if (prefersReducedMotion()) {
      elements.forEach((el) => el.classList.add(animationClass));
      return;
    }

    elements.forEach((el, index) => {
      const delay = initialDelay + index * staggerDelay;
      setTimeout(() => {
        el.classList.add(animationClass);
      }, delay);
    });
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // HOVER GLOW EFFECT
  // ═══════════════════════════════════════════════════════════════════════════

  /**
   * Initialize interactive glow effect that follows cursor
   * @param {HTMLElement} element - Element to apply effect to
   */
  function initGlowEffect(element) {
    if (!element || prefersReducedMotion()) return;

    const handleMouseMove = throttleRAF((e) => {
      const rect = element.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      element.style.setProperty('--sl-glow-x', `${x}px`);
      element.style.setProperty('--sl-glow-y', `${y}px`);
    });

    element.addEventListener('mousemove', handleMouseMove, { passive: true });
    element.addEventListener('mouseleave', () => {
      element.style.removeProperty('--sl-glow-x');
      element.style.removeProperty('--sl-glow-y');
    }, { passive: true });
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // TYPING ANIMATION
  // ═══════════════════════════════════════════════════════════════════════════

  /**
   * Simple typing animation for text
   * @param {HTMLElement} element - Element to animate
   * @param {string} text - Text to type
   * @param {Object} options - Animation options
   */
  function typeText(element, text, options = {}) {
    if (!element) return;

    const {
      speed = 50,
      delay = 0,
      onComplete = () => {}
    } = options;

    if (prefersReducedMotion()) {
      element.textContent = text;
      onComplete();
      return;
    }

    element.textContent = '';
    let index = 0;

    setTimeout(() => {
      const interval = setInterval(() => {
        if (index < text.length) {
          element.textContent += text[index];
          index++;
        } else {
          clearInterval(interval);
          onComplete();
        }
      }, speed);
    }, delay);
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // STREAMLIT INTEGRATION
  // ═══════════════════════════════════════════════════════════════════════════

  /**
   * Initialize all SkillLens animations
   * Called automatically on DOM ready and Streamlit reruns
   */
  function initSkillLensAnimations() {
    // Score counters
    document.querySelectorAll('[data-sl-score]').forEach((el) => {
      const score = parseFloat(el.dataset.slScore || '0');
      animateScoreCounter(el, score, { suffix: '%' });
    });

    // Circular progress
    document.querySelectorAll('[data-sl-circular-progress]').forEach((el) => {
      const progress = parseFloat(el.dataset.slCircularProgress || '0');
      animateCircularProgress(el, progress);
    });

    // Progress bars
    document.querySelectorAll('[data-sl-progress]').forEach((el) => {
      const progress = parseFloat(el.dataset.slProgress || '0');
      animateProgressBar(el, progress);
    });

    // Scroll animations
    initScrollAnimations();

    // Glow effects
    document.querySelectorAll('[data-sl-glow]').forEach((el) => {
      initGlowEffect(el);
    });

    // Staggered animations
    document.querySelectorAll('[data-sl-stagger-parent]').forEach((parent) => {
      const children = parent.querySelectorAll('[data-sl-stagger-child]');
      animateStaggered(children, 'sl-animated');
    });
  }

  /**
   * Observe Streamlit content changes and re-initialize
   */
  function observeStreamlitChanges() {
    const targetNode = document.querySelector('[data-testid="stAppViewContainer"]') || document.body;

    const observer = new MutationObserver(
      debounce(() => {
        initSkillLensAnimations();
      }, 100)
    );

    observer.observe(targetNode, {
      childList: true,
      subtree: true
    });
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // PUBLIC API
  // ═══════════════════════════════════════════════════════════════════════════

  window.SkillLensAI = {
    // Core
    init: initSkillLensAnimations,
    
    // Animations
    animate,
    animateScoreCounter,
    animateCircularProgress,
    animateProgressBar,
    animateStaggered,
    typeText,
    
    // Effects
    initGlowEffect,
    
    // Utilities
    prefersReducedMotion,
    
    // Configuration
    config: CONFIG
  };

  // ═══════════════════════════════════════════════════════════════════════════
  // AUTO-INITIALIZATION
  // ═══════════════════════════════════════════════════════════════════════════

  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      initSkillLensAnimations();
      observeStreamlitChanges();
    });
  } else {
    initSkillLensAnimations();
    observeStreamlitChanges();
  }

})();
