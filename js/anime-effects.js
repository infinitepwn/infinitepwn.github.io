(() => {
  function init() {
    const controls = [
      ['#toggle-menu .site-page', '打开导航菜单'],
      ['#search-button .search', '站内搜索']
    ]
    for (const [selector, label] of controls) {
      const control = document.querySelector(selector)
      if (!control || control.tagName !== 'SPAN') continue
      control.setAttribute('role', 'button')
      control.setAttribute('aria-label', label)
      control.tabIndex = 0
      control.addEventListener('keydown', event => {
        if (event.key !== 'Enter' && event.key !== ' ') return
        event.preventDefault()
        control.click()
      })
    }

    for (const image of document.querySelectorAll('img[data-src]')) {
      image.loading = 'lazy'
      image.src = image.dataset.src
    }

    const article = document.querySelector('article#article-container')
    if (!article) return

    const progress = document.createElement('div')
    progress.setAttribute('aria-hidden', 'true')
    progress.style.cssText = `
      position: fixed;
      inset: 0 0 auto;
      height: 3px;
      z-index: 9998;
      pointer-events: none;
      background: var(--ipn-accent, #5054a3);
      transform-origin: left;
    `
    document.body.append(progress)

    function updateProgress() {
      const bounds = article.getBoundingClientRect()
      const remaining = bounds.bottom - window.innerHeight
      const range = Math.max(bounds.height - window.innerHeight, 1)
      const fraction = Math.min(1, Math.max(0, 1 - remaining / range))
      progress.style.transform = `scaleX(${fraction})`
    }

    updateProgress()
    window.addEventListener('scroll', updateProgress, { passive: true })
    window.addEventListener('resize', updateProgress)
    if ('ResizeObserver' in window) new ResizeObserver(updateProgress).observe(article)
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true })
  } else {
    init()
  }
})()
