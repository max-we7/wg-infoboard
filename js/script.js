$(document).ready(function() {

  $("#refresh_onesecond").click(function() {
     $("#nahverkehr").load("php/fahrten_heag.php");
	 $("#regionalverkehr").load("php/regionalverkehr.php");
	 $("#clock").load("php/clock.php");
	 $("#einkaufen").load("php/einkaufsliste.php");
	 $("#putzen").load("php/putzplan.php");
	 $("#xkcd").load("php/news.php");
	 $("#zaw").load("php/muell.php");
	 $("#testtest").load("php/news.php");

    return false;
    });
	
  $("#refresh_tenminutes").click(function() {
     $("#weather").load("php/weather.html");

    return false;
    });
			
});

function refresh_onesecond() {
$("#refresh_onesecond").click();  
}

function refresh_tenminutes() {
$("#refresh_tenminutes").click();  
}

setInterval(refresh_onesecond, 1000); // jede Sekunde
setInterval(refresh_tenminutes, 600000); // alle 10 min