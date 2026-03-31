/**
 * 二次元博客动态特效
 * Anime Theme Dynamic Effects
 */

(function() {
  'use strict';

  // ========================
  // 1. 樱花飘落效果
  // ========================
  const createSakuraContainer = () => {
    const container = document.createElement('div');
    container.className = 'sakura-container';
    container.id = 'sakura-container';
    document.body.appendChild(container);
    return container;
  };

  const createSakura = () => {
    const sakura = document.createElement('div');
    sakura.className = 'sakura';
    
    // 随机起始位置和动画延迟
    const startX = Math.random() * window.innerWidth;
    const delay = Math.random() * 2;
    const duration = 8 + Math.random() * 4;
    
    sakura.style.cssText = `
      left: ${startX}px;
      top: -20px;
      animation-delay: ${delay}s;
      animation-duration: ${duration}s;
    `;
    
    return sakura;
  };

  const initSakura = () => {
    if (document.getElementById('sakura-container')) return;
    
    const container = createSakuraContainer();
    
    // 初始化樱花
    for (let i = 0; i < 15; i++) {
      container.appendChild(createSakura());
    }
    
    // 定期添加新樱花保持效果
    setInterval(() => {
      if (container.children.length < 20) {
        container.appendChild(createSakura());
      }
    }, 1000);
    
    // 移除动画完成的樱花
    container.addEventListener('animationend', (e) => {
      if (e.target.classList.contains('sakura')) {
        e.target.remove();
      }
    });
  };

  // ========================
  // 2. 页面加载动画
  // ========================
  const createLoadingAnimation = () => {
    const loader = document.createElement('div');
    loader.id = 'page-loader';
    loader.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 9999;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s ease;
    `;
    
    const spinner = document.createElement('div');
    spinner.style.cssText = `
      width: 50px;
      height: 50px;
      border: 4px solid rgba(255, 255, 255, 0.3);
      border-top: 4px solid white;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    `;
    
    loader.appendChild(spinner);
    document.body.appendChild(loader);
    
    // 页面加载完成后隐藏
    window.addEventListener('load', () => {
      setTimeout(() => {
        loader.style.opacity = '0';
        setTimeout(() => loader.remove(), 300);
      }, 500);
    });
  };

  // ========================
  // 3. 滚动进度条
  // ========================
  const createProgressBar = () => {
    const progressBar = document.createElement('div');
    progressBar.id = 'reading-progress';
    progressBar.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      height: 3px;
      background: linear-gradient(90deg, #FF69B4, #9370DB, #00CED1);
      z-index: 9998;
      transition: width 0.1s ease;
    `;
    document.body.appendChild(progressBar);
    
    window.addEventListener('scroll', () => {
      const scrollPercentage = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
      progressBar.style.width = scrollPercentage + '%';
    });
  };

  // ========================
  // 4. 鼠标粒子效果
  // ========================
  const createMouseParticles = () => {
    const particles = [];
    
    document.addEventListener('mousemove', (e) => {
      // 每 10 个鼠标移动事件创建一个粒子
      if (Math.random() > 0.9) {
        const particle = document.createElement('div');
        particle.style.cssText = `
          position: fixed;
          width: 8px;
          height: 8px;
          background: radial-gradient(circle, #FF69B4, #9370DB);
          border-radius: 50%;
          pointer-events: none;
          z-index: 999;
          left: ${e.clientX}px;
          top: ${e.clientY}px;
          opacity: 1;
          box-shadow: 0 0 8px rgba(255, 105, 180, 0.6);
          animation: fadeout 1s ease-out forwards;
        `;
        
        document.body.appendChild(particle);
        
        // 移除粒子
        setTimeout(() => particle.remove(), 1000);
      }
    });
  };

  // ========================
  // 5. 标题闪烁效果
  // ========================
  const addTitleGlowEffect = () => {
    const h1Elements = document.querySelectorAll('h1, h2, .post-title');
    h1Elements.forEach(el => {
      el.classList.add('glow');
    });
  };

  // ========================
  // 6. 代码块增强
  // ========================
  const enhanceCodeBlocks = () => {
    const codeBlocks = document.querySelectorAll('pre, code, figure.highlight');
    codeBlocks.forEach((block, index) => {
      block.classList.add('anime-card');
      
      // 添加复制按钮
      if (block.tagName === 'PRE' && !block.querySelector('.copy-btn')) {
        const copyBtn = document.createElement('button');
        copyBtn.className = 'copy-btn';
        copyBtn.textContent = '📋 复制';
        copyBtn.style.cssText = `
          position: absolute;
          top: 10px;
          right: 10px;
          background: linear-gradient(135deg, #FF69B4, #9370DB);
          color: white;
          border: none;
          padding: 5px 10px;
          border-radius: 5px;
          cursor: pointer;
          font-size: 12px;
          z-index: 10;
          transition: all 0.3s ease;
        `;
        
        copyBtn.addEventListener('click', () => {
          const text = block.innerText;
          navigator.clipboard.writeText(text).then(() => {
            copyBtn.textContent = '✓ 已复制';
            setTimeout(() => {
              copyBtn.textContent = '📋 复制';
            }, 2000);
          });
        });
        
        block.parentElement.style.position = 'relative';
        block.parentElement.appendChild(copyBtn);
      }
    });
  };

  // ========================
  // 7. 卡片Hover效果增强
  // ========================
  const enhanceCardEffects = () => {
    const cards = document.querySelectorAll('article, .post, .post-preview, .widget');
    cards.forEach(card => {
      card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-5px)';
        this.style.boxShadow = '0 12px 32px rgba(255, 105, 180, 0.3)';
      });
      
      card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = '';
      });
    });
  };

  // ========================
  // 8. 动画定义 (CSS in JS)
  // ========================
  const injectAnimations = () => {
    const style = document.createElement('style');
    style.textContent = `
      @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
      }
      
      @keyframes fadeout {
        from {
          opacity: 1;
          transform: translate(0, 0);
        }
        to {
          opacity: 0;
          transform: translate(${Math.random() * 100 - 50}px, -30px);
        }
      }
      
      @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
      }
    `;
    document.head.appendChild(style);
  };

  // ========================
  // 9. 打字机效果
  // ========================
  const typewriterEffect = (element, text, speed = 50) => {
    if (!element || !text) return;
    
    let index = 0;
    element.textContent = '';
    
    const type = () => {
      if (index < text.length) {
        element.textContent += text.charAt(index);
        index++;
        setTimeout(type, speed);
      }
    };
    
    type();
  };

  // ========================
  // 10. 初始化所有效果
  // ========================
  const init = () => {
    // 等待 DOM 完全加载
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', init);
      return;
    }

    // 依次初始化所有效果
    injectAnimations();
    createLoadingAnimation();
    createProgressBar();
    
    // 延迟初始化以避免性能问题
    setTimeout(() => {
      initSakura();
      createMouseParticles();
      addTitleGlowEffect();
      enhanceCodeBlocks();
      enhanceCardEffects();
    }, 500);

    console.log('✨ 二次元博客主题已激活！Anime theme activated!');
  };

  // 在页面加载时初始化
  init();

  // 暴露一些工具函数供外部使用
  window.AnimeTheme = {
    typewriterEffect,
    init
  };
})();
