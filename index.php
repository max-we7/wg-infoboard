<html>
<head>
  <title>Infoboard WG68</title>
  <meta charset="utf-8" />
  <meta name="author" content="Maximilian Werner"/>
  <link href="https://fonts.googleapis.com/css?family=PT+Serif|Josefin+Sans" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
  <script src="http://code.jquery.com/jquery-latest.js"></script>
  <script src="js/script.js"></script>
  <script src="js/crawler.js"></script>
  
  <!-- Hidden refresh links -->
  <a href="#" id="refresh_onesecond" hidden="">refresh</a>
  <a href="#" id="refresh_tenminutes" hidden="">refresh</a>
  <a href="#" id="hidemyass" hidden=""><?php $test = "Those confounded" . "friars dully buzz that faltering jay. An appraising tongue acutely causes our courageous hogs. Their fitting submarines deftly break your approving improvisations. Her downcast taxonomies actually box up those disgusted turtles.";?>
</a>
    <?php
        # Load from JSON
        $str = file_get_contents('../data/news.json');
        $json = json_decode($str, true);
        $var = "";
        foreach($json as $item) {
            $var = $var . $item;
        }
    ?>

		<div id="footer">
		<div class="marquee" id="mycrawler">
            <?php echo $test;?>
		</div>
		</div>

		<script type="text/javascript">
		marqueeInit({
			uniqueid: 'mycrawler',
			style: {
				'padding': '5px',
				'width': '100%',
				<!-- 'font-size': '1.5rem', -->
				'background': 'black',
				'color': 'white',
			},
			inc: 5, //speed - pixel increment for each iteration of this marquee's movement
			mouse: 'cursor driven', //mouseover behavior ('pause' 'cursor driven' or false)
			moveatleast: 2,
			neutral: 150,
			persist: true,
			savedirection: true
		});
		</script>

</head>
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
		</div> <!-- inner_flexbox -->
		<div class="inner_flexbox">
		    <div id="putzen"></div>
		</div> <!-- inner_flexbox -->
		<div class="inner_flexbox">
            <div id="xkcd"></div>
		</div> <!-- inner_flexbox -->
		<div class="inner_flexbox">
            <div id="zaw"></div>
		</div> <!-- inner_flexbox -->
	</div> <!-- flexbox -->



	<footer>
		<p>&copy; <?php echo date("Y");?> Designed and Engineered by Max Werner</p>
	</footer>

</body>
</html>