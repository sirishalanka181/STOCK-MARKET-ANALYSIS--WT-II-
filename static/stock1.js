var getData= $.get('/static/stock1');
    getData.done(function(results)
    {
      var data ={

        labels:results.dates,
        series: [
          results.close,
          
        ]
      };

      var options={
        width: 800,
        height: 600,
        showArea:true,
        showLabel:true,
        backgroundColor : 'rgba(123, 0, 255, 0.1)'
      }
      var myChart = new Chartist.Line('.ct-chart',data,options)
      document.getElementById("max").innerHTML=results.max_price;
      document.getElementById("min").innerHTML=results.min_price;
      document.getElementById("pred").innerHTML=results.pred_price;
    });
