
document.addEventListener('DOMContentLoaded', function() {
  // Profile tab switching
  const profileTabs = document.querySelectorAll('.profile-tab');
  const profileTabContents = document.querySelectorAll('.profile-tab-content');
  
  if (profileTabs.length > 0) {
    profileTabs.forEach(tab => {
      tab.addEventListener('click', function() {
        // Remove active class from all tabs and contents
        profileTabs.forEach(t => t.classList.remove('active'));
        profileTabContents.forEach(c => c.classList.remove('active'));
        
        // Add active class to clicked tab
        this.classList.add('active');
        
        // Show corresponding content
        const tabId = this.dataset.tab;
        document.getElementById(tabId).classList.add('active');
      });
    });
  }
  
  // Handle profile form submission
  const settingsForm = document.querySelector('.settings-form');
  
  if (settingsForm) {
    settingsForm.addEventListener('submit', function(e) {
      e.preventDefault();
      alert('Profile settings updated successfully!');
    });
  }
  
  // Handle withdraw button
  const withdrawButton = document.querySelector('.profile-actions .btn-primary');
  
  if (withdrawButton) {
    withdrawButton.addEventListener('click', function() {
      alert('Withdrawal feature will be implemented soon!');
    });
  }
});
