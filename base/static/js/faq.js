
document.addEventListener('DOMContentLoaded', function() {
  // FAQ accordion functionality
  const faqQuestions = document.querySelectorAll('.faq-question');
  
  if (faqQuestions.length > 0) {
    faqQuestions.forEach(question => {
      question.addEventListener('click', function() {
        const faqItem = this.parentElement;
        faqItem.classList.toggle('active');
        
        // Update the toggle symbol
        const toggleIcon = this.querySelector('.faq-toggle');
        toggleIcon.textContent = faqItem.classList.contains('active') ? '−' : '+';
      });
    });
  }
  
  // FAQ category filtering
  const faqCategories = document.querySelectorAll('.faq-category');
  const faqItems = document.querySelectorAll('.faq-item');
  
  if (faqCategories.length > 0) {
    faqCategories.forEach(category => {
      category.addEventListener('click', function() {
        // Remove active class from all categories
        faqCategories.forEach(c => c.classList.remove('active'));
        
        // Add active class to clicked category
        this.classList.add('active');
        
        const categoryFilter = this.dataset.category;
        
        // Show/hide FAQ items based on category
        faqItems.forEach(item => {
          if (categoryFilter === 'all' || item.dataset.category === categoryFilter) {
            item.style.display = 'block';
          } else {
            item.style.display = 'none';
          }
        });
      });
    });
  }
  
  // FAQ search functionality
  const faqSearch = document.getElementById('faqSearch');
  
  if (faqSearch) {
    faqSearch.addEventListener('input', function() {
      const searchTerm = this.value.toLowerCase();
      
      faqItems.forEach(item => {
        const questionText = item.querySelector('.faq-question h3').textContent.toLowerCase();
        const answerText = item.querySelector('.faq-answer').textContent.toLowerCase();
        
        if (questionText.includes(searchTerm) || answerText.includes(searchTerm)) {
          item.style.display = 'block';
        } else {
          item.style.display = 'none';
        }
      });
      
      // Reset category filters
      faqCategories.forEach(c => c.classList.remove('active'));
      document.querySelector('.faq-category[data-category="all"]').classList.add('active');
    });
  }
});
