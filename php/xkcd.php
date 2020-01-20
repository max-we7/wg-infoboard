<?php
	# Load from JSON
//    $str = file_get_contents('../data/xkcd.json');
//    $json = json_decode($str, true);
    $array = explode("\n", file_get_contents('../data/xkcd.txt'));
?>

<?php echo $array[0];?>
Today's XKCD
<img src="https://imgs.xkcd.com/comics/unsubscribe_message.png"/>