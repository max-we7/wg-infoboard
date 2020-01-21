<?php
	# Load from JSON
    $str = file_get_contents('../data/news.json');
    $json = json_decode($str, true);
    $var = ""
?>

<div id="news">
    <?php foreach($json as $item) {?>
		<?php $var = $var . $item;?>
	<?php }	?>
</div>

<?php echo $var;?>