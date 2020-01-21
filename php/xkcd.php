<?php
	# Load from JSON
    $str = file_get_contents('http://xkcd.com/info.0.json');
    $json = json_decode($str, true);
    $link = $json["img"]
//    $array = explode("\n", file_get_contents('../data/xkcd.txt'));
?>

<div>
    <p>Today's XKCD</p>
</div>
<div>
    <img style="height:25%;max-width:40%;" src=<?php echo $link;?></img>
</div>