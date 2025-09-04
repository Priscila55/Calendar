
// wait for DOM to be fully loaded before execution
document.addEventListener("DOMContentLoaded", () => {
  // select elements from DOM
    const header = document.querySelector('.calendarC h3');
    const dates = document.querySelector('.dates');
  
    const months = [
        "January", 
        "February", 
        "March", 
        "April", 
        "May", 
        "June",
        "July", 
        "August", 
        "September",
        "October", 
        "November", 
        "December",
    ];

    // Get the current date, month and year
    let date = new Date();
    let month = date.getMonth();
    let year = date.getFullYear(); 

    // Enter tasks 
    let tasks = {}; 
    let goals = {};

    // render calendar based on current month and year
    function renderCalendar() {
        const start = new Date(year, month, 1).getDay();
        const endDate = new Date(year, month + 1, 0).getDate();
        const end = new Date(year, month, endDate).getDay();
        const endDatePrev = new Date(year, month, 0).getDate();
  
        let datesHtml = ""; // hold HTML for the calendar
  
        // Add previous month's days
        for(let i = start; i > 0; i--) {
            datesHtml += `<li class="inactive">${endDatePrev - i + 1}</li>`;
        }

        
  
        // Add current month's days
        for(let i = 1; i <= endDate; i++) {
            let className = 
                i === date.getDate() && 
                month === new Date().getMonth() &&
                year === new Date().getFullYear()
                ? ' class="today"' // if the date matches today, highlight
                : ""; 
            datesHtml += `<li${className}>${i}</li>`; 
        }
  
        // Add next month's days
        for(let i = end; i < 6; i++) {
            datesHtml += `<li class="inactive">${i - end + 1}</li>`;
        }
  
        dates.innerHTML = datesHtml;
        header.textContent = `${months[month]} ${year}`; 
    }

    // select the previous and next buttons for navigation
    const navs = [document.getElementById("prev"), document.getElementById("next")];

    // Add event listeners to the navigation buttons
    navs.forEach((nav) => {
        nav.addEventListener("click", (e) => {
          const btnId = e.target.id; // get the ID of the button clicked
    
          if (btnId === "prev" && month === 0) { // if month is january go to previous year
            year--;
            month = 11; // december
          } else if (btnId === "next" && month === 11) { // if month is december go to next year
            year++;
            month = 0;
          } 
          // otherwise move forward and backward
          else {
            month = btnId === "next" ? month + 1 : month - 1;
          }
          date = new Date(year, month, new Date().getDate());
          year = date.getFullYear();
          month = date.getMonth();

          // Re-render calendar with the new month and year
          renderCalendar();
        });
    });
  
    renderCalendar();
  });
