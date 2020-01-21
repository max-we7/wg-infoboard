<?php
	# Load from JSON
    $str = file_get_contents('http://xkcd.com/info.0.json');
    $json = json_decode($str, true);
    $link = $json["img"]
?>

<div id="xkcd_title">
    Today's XKCD
</div>
<div>
    <img src="<?php echo $link;?>"/>
</div>