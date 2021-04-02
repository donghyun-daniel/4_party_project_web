
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

var new_num = 0;
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
// }

