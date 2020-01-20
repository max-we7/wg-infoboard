<?php
	# Load from JSON
    $str = file_get_contents('../data/xkcd.json');
    $json = json_decode($str, true);
?>

<?php echo $str;?>
Today's XKCD
<img src="https://imgs.xkcd.com/comics/unsubscribe_message.png"/>