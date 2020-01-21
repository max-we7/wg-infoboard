<?php
	# Load from JSON
    $str = file_get_contents('../data/news.json');
    $json = json_decode($str, true);

?>

<p>IT WORKS</p>
