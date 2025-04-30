
document.addEventListener('DOMContentLoaded', function() {
  // Login form handling
  const loginForm = document.getElementById('loginForm');
  
  if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      
      // Basic validation
      if (!email || !password) {
        alert('Please fill in all fields');
        return;
      }
      
      // In a real app, this would make an API call to authenticate
      console.log('Login attempt:', { email });
      
      // Simulate successful login
      alert('Login successful! Redirecting to dashboard...');
      window.location.href = 'dashboard/';
    });
  }
  
  // Registration form handling
  const registerForm = document.getElementById('registerForm');
  
  if (registerForm) {
    registerForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const fullName = document.getElementById('fullName').value;
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      const terms = document.getElementById('terms').checked;
      
      // Basic validation
      if (!fullName || !email || !password) {
        alert('Please fill in all fields');
        return;
      }
      
      if (!terms) {
        alert('Please accept the Terms of Service and Privacy Policy');
        return;
      }
      
      // Password validation
      if (password.length < 8) {
        alert('Password must be at least 8 characters long');
        return;
      }
      
      // In a real app, this would make an API call to register the user
      console.log('Registration attempt:', { fullName, email });
      
      // Simulate successful registration
      alert('Registration successful! Redirecting to dashboard...');
      window.location.href = 'http://127.0.0.1:8000/dashboard/';
    });
  }
});
