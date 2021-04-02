// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';
Chart.defaults.global.plugins.datalabels.display = true;
Chart.defaults.global.defaultFontSize = 10;
var chartColors = {
  red: 'rgb(255, 99, 132, 0.5)',
  orange: 'rgb(255, 159, 64, 0.5)',
  yellow: 'rgb(255, 205, 86)',
  green: 'rgb(75, 192, 192)',
  blue: 'rgb(54, 162, 235)',
  purple: 'rgb(153, 102, 255)',
  grey: 'rgb(201, 203, 207)'
};
var col_index = 0;
var ctx = document.getElementById("myBarChart");
var category = document.getElementById('categories').value;
var category = JSON.parse(category);
let positiveData = document.getElementById('positive_data').value;
let negativeData = document.getElementById('negative_data').value;
positiveData = JSON.parse(positiveData);
negativeData = JSON.parse(negativeData);
console.log(ChartDataLabels.id)
const horizontalBarChartData = {
  labels: category,
  datasets:[{
    label: 'positive',
    backgroundColor: window.chartColors.blue,
    borderColor: window.chartColors.blue,
    borderWidth: 1,
    data: positiveData,
    datalabels: {
      align: 'end',
      anchor: 'end',
      backgroundColor:window.chartColors.blue,
      borderWidth: 2,
    }
  },{
    label: 'negative',
    backgroundColor: window.chartColors.red,
    borderColor: window.chartColors.red,
    borderWidth: 1,
    data: negativeData,
    datalabels: {
      align: 'end',
      anchor: 'end',
      backgroundColor:window.chartColors.red,
      borderWidth: 2,
    }
  
  }]
}

var myBarChart = new Chart(ctx, {
  type: 'bar',
  data: horizontalBarChartData,
  options: {
    plugins:{
      datalabels: {
        color:'white',
        font :{
          size : 10
        },
        listeners: {
          click: function(context) {
            // Receives `click` events only for labels of the first dataset.
            // The clicked label index is available in `context.dataIndex`.
            Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';
Chart.defaults.global.plugins.datalabels.display = false;
var chartColors = {
    red: 'rgb(255, 99, 132, 0.5)',
    orange: 'rgb(255, 159, 64, 0.5)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
  };

var new_num = context.dataIndex;
console.log("여긴가")
console.log(new_num);
// var option = document.getElementById("selectCategory").value;
// document.getElementById("selectCategory").onchange = function(e) {
//     option = this.value;

    var category = document.getElementById('categories').value;
    var cleanData = document.getElementById('clean_data').value;
    const timeDict = JSON.parse(cleanData);
    category = JSON.parse(category);
    console.log(category[1])
    const years = Object.keys(timeDict[category[new_num]]);
    let total = 0;
    let pos_total =0;
    let neg_total = 0 ;
    let posRateArr = [];
    let negRateArr = [];
    
    for(let i =0; i < years.length; i++){
    let posNegArr = timeDict[category[new_num]][years[i]]
    total += (posNegArr[0] + posNegArr[1])
    pos_total += posNegArr[0]
    neg_total += posNegArr[1]

    posRateArr.push(Math.round(100*(pos_total/total)))
    negRateArr.push(Math.round(100*(neg_total/total)))
    }
    const lineChartData = {
    labels: years,
    datasets:[{
        label: 'positive',
        backgroundColor: window.chartColors.blue,
        borderColor: window.chartColors.blue,
        fill: false,
        data: posRateArr,
        yAxisID: 'y-axis-1'
    }, {
        label: 'negative',
        backgroundColor: window.chartColors.red,
        borderColor: window.chartColors.red,
        fill: false,
        data: negRateArr,
        yAxisID: 'y-axis-2'
    }]
    };

    var ctx = document.getElementById("myPieChart")
    var myPieChart = new Chart(ctx, {
    type: 'line',
    data: lineChartData,
    options:{
        responsive:true,
        hoverMode: 'index',
        stacked: false,
        scales:{
        yAxes: [{
            ticks:{
            suggestedMin: 0,
            suggestedMax: 100,
            },
            position:'left',
            id:'y-axis-1',
        },{
            ticks:{
            suggestedMin: 0,
            suggestedMax: 100,
            },
            position:'right',
            id:'y-axis-2',
            gridLines:{
            drawOnChartArea: false
            }
        }]
        }
    }
    });
            var form = document.getElementById("category_change_form");
            var input = document.getElementById("category_change_input");
            var submit = document.getElementById("category_change_submit");
            var col_index = context.dataIndex;
            console.log(col_index);
            input.setAttribute("value",col_index);
            console.log(input.value);
            submit.submit();
          }
        }
      }
    }
    ,
    events:['click'],
    elements:{
      rectangle:{
        borderwidth: 2,
      }
    },
    responsive: true,
    legend: {
      position:'right',
    },
    // title:{
    //   display:true,
    //   text: '각 카테고리별 긍정 부정 점수'
    // },
    scales: {
      xAxes: [{
        time: {
          unit: 'month'
        },
        ticks: {
          min: 0,
          max: 1
        },
        gridLines: {
          display: true
        }

      }],
      yAxes: [{
        ticks: {
          min: 0,
          max: 100
        },
        gridLines: {
          display: true
        }
      }],
    },
  }
});



