(function () {
  "use strict";
  
  const page = document.querySelector("#page");
  const sections = page.querySelectorAll(".section");
  const pageCount = sections.length;
  
  /**
   * 添加页面指示器
   * @type {HTMLDivElement}
   */
  const nav = document.createElement("div");
  nav.id = "page-nav";
  
  let html = '<ul>';
  
  for (let i = 0; i < pageCount; i++) {
    html += `<li class="${i === 0 ? 'on' : ''}"><div><span class="title">${sections[i].dataset.title}</span>`
      + `<span class="dot"  data-num="${i}"></span></div></li>`;
  }
  
  html += '</ul>';
  
  nav.innerHTML = html;
  document.querySelector("body").appendChild(nav);
  // 获取页面指示器元素列表
  const navEle = nav.querySelectorAll("li");
  
  /**
   * 切换页面事件
   * @type {number}
   */
  let pageNum = 0;
  let isUsed = false;
  window.addEventListener("wheel", (event) => {
    const y = Math.floor(event.deltaY);
    
    if (!isUsed) {
      if (y < -30 && pageNum > 0) {
        navEle[pageNum].classList.remove("on");
        pageNum--;
        navEle[pageNum].classList.add("on");
        //加锁
        isUsed = true;
      } else if (y > 30 && pageNum > -1 && pageNum < pageCount - 1) {
        navEle[pageNum].classList.remove("on");
        pageNum++;
        navEle[pageNum].classList.add("on");
        //加锁
        isUsed = true;
      }
      
      page.style.transform = `translateY(-${pageNum * 100}vh)`;
    }
  });
  
  /**
   * 点击页面指示器切换事件
   */
  window.addEventListener("click", (event) => {
    const target = event.target;
    
    if (target.classList.contains("dot")) {
      navEle[pageNum].classList.remove("on");
      // 使用上面的 pageNum 存储
      pageNum = parseInt(target.dataset.num);
      navEle[pageNum].classList.add("on");
      
      page.style.transform = `translateY(-${pageNum * 100}vh)`;
    }
  });
  
  /**
   * 解锁
   */
  page.addEventListener("transitionend", () => {
    isUsed = false;
  });
})();