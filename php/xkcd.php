<?php
	# Load from JSON
    $str = file_get_contents('http://xkcd.com/info.0.json');
    $json = json_decode($str, true);
    $link = $json["img"]
?>

<div>
    <p>Today's XKCD</p>
</div>
<div>
    <img src="<?php echo $link;?>"/>
</div>