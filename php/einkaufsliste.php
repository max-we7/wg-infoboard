<?php
	# Load einkaufsliste from JSON
    $str = file_get_contents('../data/einkaufsliste.json');
    $json = json_decode($str, true);

?>

 <table id='buy_table' class="<?php $currentTime = idate("H"); if ($currentTime < 18) {echo 'table table-striped';} elseif ($currentTime > 18) {echo 'table table-dark table-striped';} ?>">
  <thead>
    <tr>
      <th>Einkaufsliste (/einkaufen)</th>
    </tr>
  </thead>
  <tbody>
    <?php foreach($json['liste'] as $item) {?>
      <tr><td><?php echo $item;?>
      </td></tr><?php }	?>

  </tbody>
</table>
