<?php
	# Load from JSON
//    $str = file_get_contents('../data/xkcd.json');
//    $json = json_decode($str, true);
    $array = explode("\n", file_get_contents('../data/xkcd.txt'));
?>


Today's XKCD
<img src=<?php echo $array[0];?>/>