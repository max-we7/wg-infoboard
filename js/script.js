$(document).ready(function() {

  $("#refresh_onesecond").click(function() {
     $("#nahverkehr").load("php/fahrten_heag.php");
	 $("#regionalverkehr").load("php/regionalverkehr.php");
	 $("#clock").load("php/clock.php");
	 $("#einkaufen").load("php/einkaufsliste.php");
	 $("#putzen").load("php/putzplan.php");
	 $("#xkcd").load("php/xkcd.php");
	 $("#zaw").load("php/muell.php");
	 $("#dreivier").load("php/gif.php");



    return false;
    });

    $("#news").load("php/news.php");
	
  $("#refresh_tenminutes").click(function() {

     $("#news").load("php/news.php");

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
setInterval(refresh_tenminutes, 3600000); // alle 60 min