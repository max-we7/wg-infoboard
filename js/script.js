$(document).ready(function() {

  $("#refresh_onesecond").click(function() {
     $("#nahverkehr").load("php/fahrten_heag.php");
	 $("#regionalverkehr").load("php/regionalverkehr.php");
	 $("#clock").load("php/clock.php");
	 $("#einkaufen").load("php/einkaufsliste.php");
	 $("#putzen").load("php/putzplan.php");

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

var text = " +++ Sport: Nachricht1 +++ Politik: Nachricht 2 +++ ";
var begin = 0;
var end = text.length;

function lauftext()
{
 document.getElementsByName("newsticker")[0].value = "" +
 text.substring(begin,end) + " " + text.substring(0,begin);
 begin ++;
 if(begin >= end)
 {
  begin = 0;
 }
 window.setTimeout("lauftext()", 3000);
}