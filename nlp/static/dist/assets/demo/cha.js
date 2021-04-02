// Set new default font family and font color to mimic Bootstrap's default styling

Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Pie Chart Example
// var ctx = document.getElementById("myPieChart");
// var overall = JSON.parse("{{ overallJSON|escapejs }}");
//console.log(overall);
var value = document.getElementById('overall').value;
var category = document.getElementById('categories').value;
var cleanData = document.getElementById('clean_data').value;

console.log(cleanData);
const dict = JSON.parse(value);
const timeDict = JSON.parse(cleanData);
const years = Object.keys(timeDict);
//for문 초깃값,조건, 간격
let total = 0;
let pos_total =0;
let neg_total = 0 ;
let posRateArr = [];
let negRateArr = [];
for(let i =0; i < years.length; i++){
  let posNegArr = timeDict[years[i]]
  total += (posNegArr[0] + posNegArr[1])
  pos_total += posNegArr[0]
  neg_total += posNegArr[1]
  posRateArr.push(100*(pos_total/total))
  negRateArr.push(100*(neg_total/total))
}
const lineChartData = {
  labels: years,
  datasets:[{
    label: 'positive',
    backgroundColor: '#0000FF',
    borderColor: '#0000FF',
    fill: false,
    data: posRateArr,
    yAxisID: 'y-axis-1'
  }, {
    label: 'negative',
    backgroundColor: '#FF0000',
    borderColor: '#FF0000',
    fill: false,
    data: negRateArr,
    yAxisID: 'y-axis-2'
  }]
};
console.log(posRateArr, negRateArr);
console.log(timeDict['2017']);
console.log(dict.neg);


var ctx = document.getElementById("myPieChart")
var myPieChart = new Chart(ctx, {
  type: 'line',
  data: lineChartData,
  options:{
    responsive:true,
    hoverMode: 'index',
    stacked: false,
    title:{
      display: true,
      text: '긍정 부정 그래프 입니다'
    },
    scales:{
      yAxes: [{
        type: 'linear',
        display: true,
        position:'left',
        id:'y-axis-1',
      },{
        type:'linear',
        display: true,
        position:'right',
        id:'y-axis-2',
        gridLines:{
          drawOnChartArea: false
        }
      }]
    }
  }
  });
