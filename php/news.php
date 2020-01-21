<?php
	# Load from JSON
    $str = file_get_contents('../data/news.json');
    $json = json_decode($str, true);
    $var = ""
    foreach($json as $item) {
		$var = $var . $item;
	}
?>

<div id="news">
    <?php foreach($json as $item) {
		$var = $var . $item;
	}?>
</div>

<?php echo $var;?>