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
  // 6. 代码块复制按钮
  // ========================
  const createCodeCopyButton = () => {
    document.querySelectorAll('pre').forEach(pre => {
      const button = document.createElement('button');
      button.className = 'copy-code-btn';
      button.innerHTML = '📋 复制';
      button.style.cssText = `
        position: absolute;
        top: 10px;
        right: 10px;
        padding: 6px 12px;
        background: rgba(102, 126, 234, 0.8);
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 12px;
        transition: all 0.3s ease;
        z-index: 10;
      `;
      
      button.addEventListener('mouseenter', () => {
        button.style.background = 'rgba(102, 126, 234, 1)';
      });
      
      button.addEventListener('mouseleave', () => {
        button.style.background = 'rgba(102, 126, 234, 0.8)';
      });
      
      button.addEventListener('click', () => {
        const code = pre.textContent;
        navigator.clipboard.writeText(code).then(() => {
          const originalText = button.innerHTML;
          button.innerHTML = '✅ 已复制';
          setTimeout(() => {
            button.innerHTML = originalText;
          }, 2000);
        });
      });
      
      pre.style.position = 'relative';
      pre.appendChild(button);
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
  // 9. 高质量樱花飘落特效
  // ========================
  const createSakuraEffect = () => {
    // 高质量的樱花图片URL（使用可靠CDN的免费樱花图片）
    const sakuraImages = [
      'https://images.unsplash.com/photo-1512790182412-b19e6d62bc39?w=300&h=300&fit=crop&auto=format',
      'https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?w=300&h=300&fit=crop&auto=format',
      'https://images.unsplash.com/photo-1519751138087-5bf79df62d5b?w=300&h=300&fit=crop&auto=format',
      'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=300&fit=crop&auto=format',
      'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=300&h=300&fit=crop&auto=format',
      'https://images.unsplash.com/photo-1513081040458-8c6d6d4b2e3f?w=300&h=300&fit=crop&auto=format'
    ];

    // 樱花飘落对象
    class Sakura {
      constructor() {
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.canvas.style.cssText = `
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          pointer-events: none;
          z-index: 999;
        `;
        document.body.appendChild(this.canvas);
        
        this.sakuraImages = [];
        this.sakuraParticles = [];
        this.resize();
        this.loadImages();
      }
      
      resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
      }
      
      loadImages() {
        let loadedCount = 0;
        sakuraImages.forEach((src, index) => {
          const img = new Image();
          img.crossOrigin = 'anonymous';
          img.src = src;
          img.onload = () => {
            loadedCount++;
            this.sakuraImages[index] = img;
            if (loadedCount === sakuraImages.length) {
              this.initSakura();
              this.animate();
            }
          };
          img.onerror = () => {
            // 如果图片加载失败，使用简单的圆形替代
            this.sakuraImages[index] = null;
            loadedCount++;
            if (loadedCount === sakuraImages.length) {
              this.initSakura();
              this.animate();
            }
          };
        });
      }
      
      initSakura() {
        // 根据屏幕大小合理设置樱花数量
        const count = Math.min(Math.floor(this.canvas.width * this.canvas.height / 15000), 25);
        for (let i = 0; i < count; i++) {
          this.createSakura();
        }
      }
      
      createSakura() {
        const imgIndex = Math.floor(Math.random() * this.sakuraImages.length);
        const sakuraImg = this.sakuraImages[imgIndex];
        
        const particle = {
          x: Math.random() * this.canvas.width,
          y: Math.random() * this.canvas.height,
          size: Math.random() * 15 + 8, // 减小樱花大小，更精致
          speedX: Math.random() * 0.4 - 0.2, // 减慢水平速度
          speedY: Math.random() * 0.4 + 0.2, // 减慢下落速度
          rotation: Math.random() * Math.PI * 2,
          rotationSpeed: Math.random() * 0.015 - 0.0075, // 减慢旋转
          opacity: Math.random() * 0.4 + 0.6, // 提高透明度，更通透
          wobble: Math.random() * 0.03, // 减小摇摆幅度
          wobbleSpeed: Math.random() * 0.008 + 0.004,
          img: sakuraImg,
          wobbleOffset: Math.random() * Math.PI * 2,
          useFallback: !sakuraImg
        };
        
        this.sakuraParticles.push(particle);
      }
      
      updateSakura(particle) {
        particle.x += particle.speedX + Math.sin(particle.wobbleOffset + Date.now() * particle.wobbleSpeed) * particle.wobble;
        particle.y += particle.speedY;
        particle.rotation += particle.rotationSpeed;
        particle.wobbleOffset += particle.wobbleSpeed;
        
        // 边界检查
        if (particle.x > this.canvas.width + 50) particle.x = -50;
        if (particle.x < -50) particle.x = this.canvas.width + 50;
        if (particle.y > this.canvas.height + 50) {
          particle.y = -50;
          particle.x = Math.random() * this.canvas.width;
        }
      }
      
      drawSakura(particle) {
        this.ctx.save();
        this.ctx.globalAlpha = particle.opacity;
        this.ctx.translate(particle.x, particle.y);
        this.ctx.rotate(particle.rotation);
        
        if (particle.img && !particle.useFallback) {
          // 绘制图片樱花
          this.ctx.drawImage(
            particle.img,
            -particle.size / 2,
            -particle.size / 2,
            particle.size,
            particle.size
          );
        } else {
          // 备用：绘制精美的卡通风格樱花
          const gradient1 = this.ctx.createRadialGradient(0, 0, 0, 0, 0, particle.size / 2);
          gradient1.addColorStop(0, 'rgba(255, 240, 245, 0.95)'); // 极浅粉色
          gradient1.addColorStop(0.5, 'rgba(255, 182, 193, 0.8)'); // 浅粉色
          gradient1.addColorStop(1, 'rgba(219, 112, 147, 0.7)'); // 中粉色
          
          const gradient2 = this.ctx.createRadialGradient(0, 0, 0, 0, 0, particle.size / 3);
          gradient2.addColorStop(0, 'rgba(255, 255, 255, 0.9)');
          gradient2.addColorStop(1, 'rgba(255, 240, 245, 0.8)');
          
          // 绘制主花瓣
          this.ctx.fillStyle = gradient1;
          this.ctx.beginPath();
          
          // 绘制五瓣樱花
          for (let i = 0; i < 5; i++) {
            const angle = (i * Math.PI * 2) / 5;
            const nextAngle = ((i + 1) * Math.PI * 2) / 5;
            
            if (i === 0) {
              this.ctx.moveTo(Math.cos(angle) * particle.size * 0.5, Math.sin(angle) * particle.size * 0.5);
            }
            
            const cp1x = Math.cos(angle) * particle.size * 0.3;
            const cp1y = Math.sin(angle) * particle.size * 0.3;
            const cp2x = Math.cos(nextAngle) * particle.size * 0.3;
            const cp2y = Math.sin(nextAngle) * particle.size * 0.3;
            const x = Math.cos(nextAngle) * particle.size * 0.5;
            const y = Math.sin(nextAngle) * particle.size * 0.5;
            
            this.ctx.bezierCurveTo(cp1x, cp1y, cp2x, cp2y, x, y);
          }
          this.ctx.closePath();
          this.ctx.fill();
          
          // 绘制中心花蕊
          this.ctx.fillStyle = gradient2;
          this.ctx.beginPath();
          this.ctx.arc(0, 0, particle.size * 0.15, 0, Math.PI * 2);
          this.ctx.fill();
          
          // 添加简单的高光
          this.ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
          this.ctx.beginPath();
          this.ctx.arc(-particle.size * 0.15, -particle.size * 0.15, particle.size * 0.08, 0, Math.PI * 2);
          this.ctx.fill();
        }
        
        this.ctx.restore();
      }
      
      animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.sakuraParticles.forEach(particle => {
          this.updateSakura(particle);
          this.drawSakura(particle);
        });
        
        requestAnimationFrame(() => this.animate());
      }
    }
    
    const sakura = new Sakura();
    
    window.addEventListener('resize', () => {
      sakura.resize();
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
    createCodeCopyButton();
    createHeadingLinks();
    createBackToTop();
    createSakuraEffect(); // 添加樱花特效
    
    console.log('✨ 高级博客特效已加载');
  };

  init();
})();
