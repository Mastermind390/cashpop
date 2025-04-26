
document.addEventListener('DOMContentLoaded', function() {
  // Initialize the earnings chart
  const ctx = document.getElementById('earningsChart');
  
  if (ctx) {
    // Sample data for the chart
    const chartData = {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      datasets: [{
        label: 'Earnings ($)',
        data: [2.50, 1.75, 3.00, 0.50, 1.25, 2.00, 1.50],
        fill: true,
        backgroundColor: 'rgba(155, 135, 245, 0.2)',
        borderColor: 'rgba(155, 135, 245, 1)',
        tension: 0.4
      }]
    };
    
    const config = {
      type: 'line',
      data: chartData,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: function(value) {
                return '$' + value.toFixed(2);
              }
            }
          }
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: function(context) {
                return '$' + context.parsed.y.toFixed(2);
              }
            }
          }
        }
      }
    };
    
    new Chart(ctx, config);
  }
  
  // Task category filtering
  const categoryFilters = document.querySelectorAll('.category-filter');
  const taskCards = document.querySelectorAll('.task-card');
  
  if (categoryFilters.length > 0) {
    categoryFilters.forEach(filter => {
      filter.addEventListener('click', function() {
        // Remove active class from all filters
        categoryFilters.forEach(f => f.classList.remove('active'));
        
        // Add active class to clicked filter
        this.classList.add('active');
        
        const category = this.dataset.category;
        
        // Show/hide task cards based on category
        taskCards.forEach(card => {
          if (category === 'all' || card.dataset.category === category) {
            card.style.display = 'flex';
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }
  
  // Task button click handler
  const taskButtons = document.querySelectorAll('.btn-task');
  
  if (taskButtons.length > 0) {
    taskButtons.forEach(button => {
      button.addEventListener('click', function() {
        const taskTitle = this.closest('.task-card').querySelector('.task-title').textContent;
        alert(`Starting task: ${taskTitle}\nThis feature will be implemented soon!`);
      });
    });
  }


});

let dropDownBtn = document.getElementById("dropdown-button")
let dropDownContent = document.getElementById("dropdown-content")

dropDownBtn.addEventListener("click", ()=>{
  if (dropDownContent.style.display == "none") {
    dropDownContent.style.display == "block"
  } else {
    dropDownContent.style.display == "none"
  }
  console.log("it working")
})