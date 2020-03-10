(function () {
  "use strict";
  
  const form = document.querySelector("#form");
  const fieldset = form.querySelector("fieldset");
  const notification = document.querySelector(".notification");
  const msg = notification.querySelector(".msg");
  const close = notification.querySelector(".close");
  
  form.onsubmit = (event) => {
    event.preventDefault();
    
    const body = new FormData(form);
    body.set("date", document.querySelector("#date").dataset.value);
    
    fieldset.setAttribute("disabled", "");
    notification.classList.add("show");
    
    fetch(form.action, {
      method: "POST",
      body: body
    })
      .then(res => res.json())
      .then((response) => {
        fieldset.removeAttribute("disabled");
        if (response.code === -1) {
          return Promise.reject(response.msg || "未知错误")
        }
      })
      .then(() => {
        let filename = '';
        
        fetch("/file", {
          method: "POST"
        })
          .then(res => {
            filename = res.headers.get("Content-Disposition").split(";")[1].split("filename=")[1];
            return res.blob()
          })
          .then((response) => {
            const a = document.createElement("a");
            a.href = URL.createObjectURL(response);
            a.download = filename;
            a.click();
            URL.revokeObjectURL(a.href);
            a.remove();
          });
        
        setTimeout(() => {
          notification.classList.add("fade");
          setTimeout(() => {
            notification.classList.remove("show", "fade");
          }, 700);
        }, 2000);
        
      })
      .catch((err) => {
        notification.classList.add("show-msg");
        msg.innerHTML = err;
      });
  };
  
  close.addEventListener("click", () => {
    notification.classList.add("fade");
    fieldset.removeAttribute("disabled");
    
    setTimeout(() => {
      notification.classList.remove("show", "show-msg", "fade");
    }, 700);
  });
})();