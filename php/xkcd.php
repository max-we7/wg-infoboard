<?php
	# Load from JSON
    $str = file_get_contents('http://xkcd.com/info.0.json');
    $json = json_decode($str, true);
    $link = $json["img"]
?>



    <img src="http://192.168.178.52:5555/wg-infoboard/data/trump.jpg" width="50%"/>
