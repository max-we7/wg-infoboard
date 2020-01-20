<html>
<head>
  <title>Timetable</title>
  <meta charset="utf-8" />
  <meta name="author" content="Maximilian Werner"/>
  <link href="https://fonts.googleapis.com/css?family=PT+Serif|Josefin+Sans" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
  <script src="http://code.jquery.com/jquery-latest.js"></script>
  <script src="js/script.js"></script>
  
  <!-- Hidden refresh links -->
  <a href="#" id="refresh_onesecond" hidden="">refresh</a>
  <a href="#" id="refresh_tenminutes" hidden="">refresh</a>

</head>
<body onLoad="lauftext()">
	<div id="flexbox">
		<div class="inner_flexbox">
			<div id="nahverkehr"></div>
			<div id="regionalverkehr"></div>
		</div> <!-- inner_flexbox -->
		<div class="inner_flexbox">
			<div id="clock"></div>
			<div id="weather">
			<div id="wcom-82d5e81c8529ca7eab7a4b2c15ecefd4" class="wcom-default w300x250" style="border: 0px none; background-color: rgb(0, 0, 0); border-radius: 5px; color: rgb(255, 255, 255);"><link rel="stylesheet" href="//cs3.wettercomassets.com/woys/5/css/w.css" media="all"><div class="wcom-city"><a style="color: rgb(255, 255, 255);" href="https://www.wetter.com/deutschland/griesheim/DE0003699.html" target="_blank" rel="nofollow" aria-label="Wetter Berlin" title="Wetter Griesheim">Wetter Griesheim</a></div><div id="wcom-82d5e81c8529ca7eab7a4b2c15ecefd4-weather"></div><script type="text/javascript" src="//cs3.wettercomassets.com/woys/5/js/w.js"></script><script type="text/javascript">_wcomWidget({id: 'wcom-82d5e81c8529ca7eab7a4b2c15ecefd4',location: 'DE0003699',format: '300x250',type: 'spaces'});</script></div>
			</div> <!-- weather -->
		</div> <!-- inner_flexbox -->
		<div class="inner_flexbox">
			<div id="einkaufen"></div>
		</div>
		<div class="inner_flexbox">
		    <div id="putzen"></div>
		</div>
	</div> <!-- flexbox -->

	<p>Aktuelle Nachrichten vom 20.02.08</p>
    <input type="text" name="newsticker">

	<footer>
		<p>&copy; <?php echo date("Y");?> Designed and Engineered by Max Werner</p>
	</footer>

</body>
</html>