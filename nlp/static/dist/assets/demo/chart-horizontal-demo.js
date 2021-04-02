// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Pie Chart Example
var ctx = document.getElementById("myHorizontalChart");
var value = document.getElementById('overall').value;
const dict = JSON.parse(value);
console.log(dict.neg);

var myPieChart = new Chart(ctx, {
  type: 'horizontal',
  data: {
    labels: Object.keys(dict),
    datasets: [{
      data: Object.values(dict),
      backgroundColor: ['#00FF00', '#FF0001'],
    }],
  },
});
