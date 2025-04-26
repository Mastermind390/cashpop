
// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
  // const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
  const header = document.querySelector('.header');
  
  
  
  // Notification button popover (placeholder for future implementation)
  const notificationButton = document.querySelector('.btn-notification');
  if (notificationButton) {
    notificationButton.addEventListener('click', function() {
      alert('Notifications feature coming soon!');
    });
  }
  
  // Add smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      
      if (href !== '#') {
        e.preventDefault();
        
        const targetElement = document.querySelector(href);
        if (targetElement) {
          targetElement.scrollIntoView({
            behavior: 'smooth'
          });
        }
      }
    });
  });
});

let dropDownBtn = document.getElementById("dropdown-button")
let dropDownContent = document.getElementById("dropdown-content")
// dropDownBtn.addEventListener("click", ()=>{
//   let computedStyle = window.getComputedStyle(dropDownContent);
//   if (computedStyle.display === "none") {
//     dropDownContent.style.display = "block";
//   } else {
//     dropDownContent.style.display = "none";
//   }
//   console.log(computedStyle)
// })

dropDownBtn.addEventListener("click", (event) => {
  event.stopPropagation(); // Prevent click from bubbling to document
  dropDownContent.classList.toggle("active");
});

// Close dropdown when clicking outside
document.addEventListener("click", (event) => {
  if (!dropDownContent.contains(event.target) && !dropDownBtn.contains(event.target)) {
    dropDownContent.classList.remove("active");
  }
});
