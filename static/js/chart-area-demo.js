// // Set new default font family and font color to mimic Bootstrap's default styling
// Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
// Chart.defaults.global.defaultFontColor = '#292b2c';

// // Area Chart Example
// var ctx = document.getElementById("myAreaChart");
// var myLineChart = new Chart(ctx, {
//   type: 'line',
//   data: {
//     labels: ["Mar 1", "Mar 2", "Mar 3", "Mar 4", "Mar 5", "Mar 6", "Mar 7", "Mar 8", "Mar 9", "Mar 10", "Mar 11", "Mar 12", "Mar 13"],
//     datasets: [{
//       label: "Sessions",
//       lineTension: 0.3,
//       backgroundColor: "rgba(2,117,216,0.2)",
//       borderColor: "rgba(2,117,216,1)",
//       pointRadius: 5,
//       pointBackgroundColor: "rgba(2,117,216,1)",
//       pointBorderColor: "rgba(255,255,255,0.8)",
//       pointHoverRadius: 5,
//       pointHoverBackgroundColor: "rgba(2,117,216,1)",
//       pointHitRadius: 50,
//       pointBorderWidth: 2,
//       data: [10000, 30162, 26263, 18394, 18287, 28682, 31274, 33259, 25849, 24159, 32651, 31984, 38451],
//     }],
//   },
//   options: {
//     scales: {
//       xAxes: [{
//         time: {
//           unit: 'date'
//         },
//         gridLines: {
//           display: false
//         },
//         ticks: {
//           maxTicksLimit: 7
//         }
//       }],
//       yAxes: [{
//         ticks: {
//           min: 0,
//           max: 40000,
//           maxTicksLimit: 5
//         },
//         gridLines: {
//           color: "rgba(0, 0, 0, .125)",
//         }
//       }],
//     },
//     legend: {
//       display: false
//     }
//   }
// });

document.addEventListener('DOMContentLoaded', function () {
  // Context for Pie Chart
  var pieCtx = document.getElementById("donationByDonorTypePieChart");
  var pieData = JSON.parse(document.getElementById('pieChartData').textContent);

  // Initialize Pie Chart
  var myPieChart = new Chart(pieCtx, {
      type: 'pie',
      data: {
          labels: pieData.labels,
          datasets: [{
              data: pieData.data,
              backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745'],
          }],
      },
  });

  // Context for Bar Chart
  var barCtx = document.getElementById("fundsRaisedByDonorTypeChart");
  var barData = JSON.parse(document.getElementById('barChartData').textContent);

  // Initialize Bar Chart
  var myBarChart = new Chart(barCtx, {
      type: 'bar',
      data: {
          labels: barData.labels,
          datasets: [{
              label: "Revenue",
              backgroundColor: "rgba(2,117,216,1)",
              borderColor: "rgba(2,117,216,1)",
              data: barData.data,
          }],
      },
      options: {
          scales: {
              xAxes: [{ time: { unit: 'month' }, gridLines: { display: false }, ticks: { maxTicksLimit: 6 } }],
              yAxes: [{ ticks: { min: 0, max: 15000, maxTicksLimit: 5 }, gridLines: { display: true } }],
          },
          legend: { display: false }
      }
  });

  // Context for Line Chart
  var lineCtx = document.getElementById("futureDonationsPredictionChart");
  var lineData = JSON.parse(document.getElementById('lineChartData').textContent);

  // Initialize Line Chart
  var myLineChart = new Chart(lineCtx, {
      type: 'line',
      data: {
          labels: lineData.labels,
          datasets: [{
              label: "Predictions",
              lineTension: 0.3,
              backgroundColor: "rgba(2,117,216,0.2)",
              borderColor: "rgba(2,117,216,1)",
              pointRadius: 5,
              pointBackgroundColor: "rgba(2,117,216,1)",
              pointBorderColor: "rgba(255,255,255,0.8)",
              pointHoverRadius: 5,
              pointHoverBackgroundColor: "rgba(2,117,216,1)",
              pointHitRadius: 50,
              pointBorderWidth: 2,
              data: lineData.data,
          }],
      },
      options: {
          scales: {
              xAxes: [{
                  time: {
                      unit: 'date'
                  },
                  gridLines: {
                      display: false
                  },
                  ticks: {
                      maxTicksLimit: 7
                  }
              }],
              yAxes: [{
                  ticks: {
                      min: 0,
                      max: 40000,
                      maxTicksLimit: 5
                  },
                  gridLines: {
                      color: "rgba(0, 0, 0, .125)",
                  }
              }],
          },
          legend: {
              display: false
          }
      }
  });
});
