<?php
var d = new Date();
var h = d.getHours();
var m = d.getMinutes();
var time_trigger = h + ":" + m;
if (time_trigger == "18:02")
  {
    document.getElementById("bg").style.background = "black";
    document.getElementById("bg").style.color = "white";
    document.getElementById("news").style.color = "white";
    $('#clean_table').removeClass('table table-striped');
    $('#clean_table').addClass('table-dark table-striped');

  }
  ?>
