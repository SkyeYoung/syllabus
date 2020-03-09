/**
 * 暂时参考了这篇文章：https://www.jianshu.com/p/e7e7f38cc724
 */

(function () {
  window.datepicker = {
    calDate(date, gap) {
      if (!date.year || !date.month) {
        throw 'Error: 缺少年份或月份';
      }
      
      gap = Object.assign({}, {
        year: 0,
        month: 0,
      }, gap);
      
      const tempDate = new Date(date.year, date.month - 1);
      tempDate.setFullYear(tempDate.getFullYear() + gap.year);
      tempDate.setMonth(tempDate.getMonth() + gap.month);
      
      return {
        year: tempDate.getFullYear(),
        month: tempDate.getMonth() + 1,
      };
    },
    getMonthDate(year, month) {
      if (!year || !month) {
        const today = new Date();
        year = today.getFullYear();
        month = today.getMonth() + 1;
      }
      
      const firstDay = new Date(year, month - 1, 1);
      let firstDayWeekDay = firstDay.getDay();
      if (firstDayWeekDay === 0) {
        firstDayWeekDay = 7
      }
      
      const lastDayofLastMonth = new Date(year, month - 1, 0);
      const lastDateofLastMonth = lastDayofLastMonth.getDate();
      const preMonthDayCount = firstDayWeekDay - 1;
      const lastDay = new Date(year, month, 0);
      const lastDate = lastDay.getDate();
      
      let ret = [];
      
      for (let i = 0; i < 6 * 7; i++) {
        let date = i + 1 - preMonthDayCount;
        let showDate = date;
        let thisMonth = month;
        
        if (thisMonth === 13) thisMonth = 1;
        if (thisMonth === 0) thisMonth = 12;
        
        if (date <= 0) {
          thisMonth = month - 1;
          showDate = lastDateofLastMonth + date;
        } else if (date > lastDate) {
          thisMonth = month + 1;
          showDate = showDate - lastDate;
        }
        
        ret.push({
          date: date,
          month: thisMonth,
          showDate: showDate
        });
      }
      
      return {
        year: year,
        month: month,
        days: ret
      }
    },
    buildUI(year, month) {
      const monthDate = this.getMonthDate(year, month);
      
      let html = '<header>' +
        '<span class="icon"><i class="prev"></i></span>' +
        `<span>${monthDate.year} 年 ${monthDate.month} 月</span>` +
        '<span class="icon"><i class="next"></i></span>' +
        '</header>' +
        '<main>' +
        '<table>' +
        '<thead>' +
        '<tr>' +
        '<th>一</th>' +
        '<th>二</th>' +
        '<th>三</th>' +
        '<th>四</th>' +
        '<th>五</th>' +
        '<th>六</th>' +
        '<th>日</th>' +
        '</tr>' +
        '</thead>' +
        '<tbody>';
      
      const today = new Date();
      const isThisMonth = today.getFullYear() === monthDate.year && today.getMonth() === monthDate.month - 1;
      
      for (let i = 0; i < monthDate.days.length; i++) {
        const date = monthDate.days[i];
        if (i % 7 === 0) {
          html += '<tr>';
        }
        if (date.date <= 0 || date.date > date.showDate) {
          html += '<td ><span data-day = ' + date.date + ' class = "not-this-month">' + date.showDate + '</span></td>';
        } else if (isThisMonth && date.date === today.getDate()) {
          html += '<td ><span data-day = ' + date.date + ' class = "today" title="今天">' + date.showDate + '</span></td>';
        } else {
          html += '<td ><span data-day = ' + date.date + '>' + date.showDate + '</span></td>';
        }
        if (i % 7 === 6) {
          html += '</tr>'
        }
      }
      
      html += '</tbody>' +
        '</table>' +
        '</main>';
      
      return [html, monthDate];
    },
    render(year, month) {
      const [html, date] = this.buildUI(year, month);
      const datePicker = document.querySelector('.date-picker');
      datePicker.innerHTML = html;
      
      return date;
    },
    init() {
      const dateInput = document.querySelector('.date-input');
      dateInput.innerHTML += '<div class="date-picker"></div>';
      
      let date = this.render();
      
      const input = dateInput.querySelector('input');
      const datePicker = document.querySelector('.date-picker');
      datePicker.style.left = input.offsetWidth + 6 + 'px';
      
      window.addEventListener('click', () => {
        datePicker.classList.remove('visible');
      });
      
      input.addEventListener('click', (event) => {
        event.stopPropagation();
        datePicker.classList.add('visible');
      });
      
      datePicker.addEventListener('click', (event) => {
        const target = event.target;
        const targetClassList = target.classList;
        
        if (targetClassList.contains('prev')) {
          event.stopPropagation();
          const {
            year, month
          } = this.calDate(date, {month: -1});
          date = this.render(year, month);
        } else if (targetClassList.contains('next')) {
          event.stopPropagation();
          const {
            year, month
          } = this.calDate(date, {month: 1});
          date = this.render(year, month);
        }
        
        if (target.tagName.toLowerCase() === 'span') {
          if (!targetClassList.contains('not-this-month')) {
            input.value = `${date.year} 年 ${date.month} 月 ${target.dataset.day} 日`;
            input.dataset.value = `${date.year}-${date.month}-${target.dataset.day}`;
          } else {
            event.stopPropagation();
          }
        }
      });
    }
  }
})();