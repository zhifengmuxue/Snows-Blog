(function() {
  let isScrolling = false;

  const handleWheel = function(e) {
    const topImg = document.getElementById('page-header');
    const contentInner = document.getElementById('content-inner');
    const scrollDownBtn = document.getElementById('scroll-down');
    
    // 只有在首页（带有 full_page 类）、且在页面最顶部时触发
    if (topImg && topImg.classList.contains('full_page') && contentInner && scrollDownBtn) {
      if (window.scrollY === 0 && e.deltaY > 0) {
        if (!isScrolling) {
          isScrolling = true;
          // 平滑滚动到内容区域
          if (typeof btf !== 'undefined' && btf.scrollToDest) {
             btf.scrollToDest(contentInner.offsetTop, 300);
          } else {
             window.scrollTo({ top: contentInner.offsetTop, behavior: 'smooth' });
          }
          
          e.preventDefault();
          
          // 动画结束后解除锁定，允许正常滚动
          setTimeout(() => {
            isScrolling = false;
          }, 800);
        } else {
          // 正在动画期间，阻止默认滚动事件，防止页面抖动
          e.preventDefault();
        }
      }
    }
  };

  // 必须使用 passive: false 才能调用 preventDefault()
  window.addEventListener('wheel', handleWheel, { passive: false });
})();