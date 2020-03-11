(function () {
  "use strict";
  const page = document.querySelector("#page");
  const sections = page.querySelectorAll(".section");
  const pageCount = sections.length;
  const nav = document.querySelector("#page-nav");
  
  let html = '<ul>';
  
  for (let i = 0; i < pageCount; i++) {
    html += `<li ${i === 0 ? 'class="on"' : ''}><div><span class="title">${sections[i].dataset.title}</span>`
      + '<span class="dot"></span></div></li>';
  }
  
  html += '</ul>';
  
  nav.innerHTML += html;
  const navEle = nav.querySelectorAll("li");
  
  /**
   * 切换页面
   * @type {number}
   */
  let transY = 0, pageNum = 0;
  window.addEventListener("wheel", (event) => {
    const y = Math.floor(event.deltaY);
    
    if (y < -30 && pageNum > 0) {
      navEle[pageNum].classList.remove("on");
      pageNum--;
      navEle[pageNum].classList.add("on");
      transY = pageNum * 100;
    } else if (y > 30 && pageNum > -1 && pageNum < pageCount - 1) {
      navEle[pageNum].classList.remove("on");
      pageNum++;
      navEle[pageNum].classList.add("on");
      transY = pageNum * 100;
    }
    
    page.style.transform = `translateY(-${transY}vh)`;
  });
  
})();