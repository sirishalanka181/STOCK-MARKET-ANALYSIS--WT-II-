
function OpenRequest()
  {
    console.log("fetched");
    var getData= $.get('/data');
    getData.done(function(results)
    {
      document.getElementById("nifty").innerHTML=results.nifty;
      document.getElementById("sensex").innerHTML=results.sensex;
      document.getElementById("usd").innerHTML=results.usd;
    });
  }

OpenRequest();
setInterval(OpenRequest, 2000);