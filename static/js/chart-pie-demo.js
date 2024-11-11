document.addEventListener('DOMContentLoaded', function () {
  var ctx = document.getElementById('donationByDonorTypePieChart').getContext('2d');
  if (!ctx) {
      console.log('Canvas context not found');
      return;
  }
  var myPieChart = new Chart(ctx, {
      type: 'pie',
      data: {
          labels: Object.keys(pieChartData),
          datasets: [{
              data: Object.values(pieChartData),
              backgroundColor: ['#007bff', '#dc3545'],
          }],
      }
  });
});