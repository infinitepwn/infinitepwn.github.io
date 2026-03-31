/**
 * 高级博客特效 - Premium Blog Effects
 * 设计理念：优雅、性能优化、现代化的交互体验
 */

(function() {
  'use strict';

  // ========================
  // 1. 页面加载进度条
  // ========================
  const createProgressBar = () => {
    const progressBar = document.createElement('div');
    progressBar.className = 'progress-bar';
    progressBar.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      height: 3px;
      background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #a8edea 100%);
      z-index: 9999;
      transition: width 0.3s ease;
      box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
    `;
    document.body.appendChild(progressBar);
    
    let width = 10;
    progressBar.style.width = width + '%';
    
    const interval = setInterval(() => {
      if (width < 90) {
        width += Math.random() * 30;
        progressBar.style.width = Math.min(width, 90) + '%';
      }
    }, 300);
    
    window.addEventListener('load', () => {
      clearInterval(interval);
      progressBar.style.width = '100%';
      setTimeout(() => {
        progressBar.style.opacity = '0';
        progressBar.style.transition = 'opacity 0.5s ease';
      }, 500);
    });
  };

  // ========================
  // 2. 鼠标粒子效果 - 优化版
  // ========================
  const createMouseParticles = () => {
    const canvas = document.createElement('canvas');
    canvas.className = 'mouse-particles';
    canvas.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 999;
    `;
    document.body.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    let particles = [];
    let mouseX = 0;
    let mouseY = 0;
    
    const Particle = function(x, y) {
      this.x = x;
      this.y = y;
      this.size = Math.random() * 2 + 1;
      this.speedX = (Math.random() - 0.5) * 3;
      this.speedY = (Math.random() - 0.5) * 3;
      this.opacity = 1;
      this.decay = Math.random() * 0.015 + 0.015;
    };
    
    Particle.prototype.draw = function() {
      ctx.fillStyle = `rgba(102, 126, 234, ${this.opacity})`;
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fill();
    };
    
    Particle.prototype.update = function() {
      this.x += this.speedX;
      this.y += this.speedY;
      this.opacity -= this.decay;
    };
    
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      particles.forEach((particle, index) => {
        particle.update();
        particle.draw();
        
        if (particle.opacity <= 0) {
          particles.splice(index, 1);
        }
      });
      
      if (particles.length > 0) {
        requestAnimationFrame(animate);
      }
    };
    
    document.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      
      for (let i = 0; i < 3; i++) {
        particles.push(new Particle(mouseX, mouseY));
      }
      
      if (particles.length > 0) {
        animate();
      }
    });
    
    window.addEventListener('resize', () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    });
  };

  // ========================
  // 3. 平滑滚动高亮
  // ========================
  const createScrollHighlight = () => {
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const target = document.querySelector(link.getAttribute('href'));
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  };

  // ========================
  // 4. 文章阅读进度条
  // ========================
  const createReadingProgress = () => {
    const article = document.querySelector('article');
    if (!article) return;
    
    const progressBar = document.createElement('div');
    progressBar.style.cssText = `
      position: fixed;
      left: 0;
      top: 0;
      height: 4px;
      background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #a8edea 100%);
      z-index: 9998;
      transition: width 0.2s ease;
    `;
    document.body.appendChild(progressBar);
    
    window.addEventListener('scroll', () => {
      const windowHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrolled = (window.scrollY / windowHeight) * 100;
      progressBar.style.width = scrolled + '%';
    });
  };

  // ========================
  // 5. 图片懒加载 + 加载动画
  // ========================
  const createImageLazyLoad = () => {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.onload = () => {
            img.style.opacity = '1';
          };
          imageObserver.unobserve(img);
        }
      });
    });
    
    images.forEach(img => {
      img.style.opacity = '0';
      img.style.transition = 'opacity 0.3s ease';
      imageObserver.observe(img);
    });
  };



  // ========================
  // 7. 标题ID自动生成 + 链接生成
  // ========================
  const createHeadingLinks = () => {
    const headings = document.querySelectorAll('h2, h3, h4, h5, h6');
    headings.forEach(heading => {
      if (!heading.id) {
        heading.id = heading.textContent
          .toLowerCase()
          .replace(/[^\w\s]/g, '')
          .replace(/\s+/g, '-');
      }
      
      const link = document.createElement('a');
      link.href = '#' + heading.id;
      link.className = 'heading-anchor';
      link.innerHTML = '🔗';
      link.style.cssText = `
        opacity: 0;
        margin-left: 8px;
        color: #667eea;
        text-decoration: none;
        transition: opacity 0.3s ease;
      `;
      
      heading.appendChild(link);
      heading.addEventListener('mouseenter', () => {
        link.style.opacity = '1';
      });
      heading.addEventListener('mouseleave', () => {
        link.style.opacity = '0';
      });
    });
  };

  // ========================
  // 8. 返回顶部按钮
  // ========================
  const createBackToTop = () => {
    const button = document.createElement('button');
    button.id = 'back-to-top';
    button.innerHTML = '↑';
    button.style.cssText = `
      position: fixed;
      bottom: 30px;
      right: 30px;
      width: 50px;
      height: 50px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      font-size: 24px;
      opacity: 0;
      transition: all 0.3s ease;
      z-index: 1000;
      box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
    `;
    
    document.body.appendChild(button);
    
    window.addEventListener('scroll', () => {
      if (window.scrollY > 300) {
        button.style.opacity = '1';
        button.style.pointerEvents = 'auto';
      } else {
        button.style.opacity = '0';
        button.style.pointerEvents = 'none';
      }
    });
    
    button.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    
    button.addEventListener('mouseenter', () => {
      button.style.transform = 'translateY(-4px)';
      button.style.boxShadow = '0 12px 32px rgba(102, 126, 234, 0.6)';
    });
    
    button.addEventListener('mouseleave', () => {
      button.style.transform = 'translateY(0)';
      button.style.boxShadow = '0 8px 24px rgba(102, 126, 234, 0.4)';
    });
  };



  // ========================
  // 10. 初始化所有特效
  // ========================
  const init = () => {
    // 等待 DOM 加载完成
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', init);
      return;
    }
    
    createProgressBar();
    createMouseParticles();
    createScrollHighlight();
    createReadingProgress();
    createImageLazyLoad();
    createHeadingLinks();
    createBackToTop();

    console.log('✨ 高级博客特效已加载');
  };

  init();
})();
