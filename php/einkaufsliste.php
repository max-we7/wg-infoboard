<?php
	# Load einkaufsliste from JSON
    $str = file_get_contents('../data/einkaufsliste.json');
    $json = json_decode($str, true);
?>

	<table class="einkaufsliste">
		<tr>
			<th><?php echo "Einkaufsliste: ";?><br>(/einkaufen)</th>
		</tr>
		<?php foreach($json['liste'] as $item) {?>
			<tr>
				<td><?php echo $item;?></td>
			</tr>
		<?php }	?>
	</table>