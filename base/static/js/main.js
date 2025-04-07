
// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
  const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
  const header = document.querySelector('.header');
  
  if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', function() {
      header.classList.toggle('mobile-menu-active');
    });
  }
  
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
