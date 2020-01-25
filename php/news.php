
<?php
	# Load from JSON
    $str = file_get_contents('../data/news.json');
    $json = json_decode($str, true);

?>

<div id="news">
    <?php foreach($json as $item) {?>
		+++ <?php echo $item;?>
	<?php }	?>
</div>