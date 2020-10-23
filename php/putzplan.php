<?php
	# Load putzplan from JSON
    $str = file_get_contents('../data/putzplan.json');
    $json = json_decode($str, true);
    $row_color = "";

    # bad
    $bad_vergangen = $json['bad']['tage_vergangen'];
    $bad_intervall = $json['bad']['intervall_tage'];
    $bad_verbleibend = $bad_intervall - $bad_vergangen;
    if ($bad_verbleibend > 1)
        $bad_faellig = "in " . $bad_verbleibend . " Tagen";
    elseif ($bad_verbleibend == 1)
        $bad_faellig = "morgen";
    elseif ($bad_verbleibend == 0)
        $bad_faellig = "<span>heute</span>";
    elseif ($bad_verbleibend == -1)
        $bad_faellig = "<span>gestern</span>";
    else
        $bad_faellig = "<span>seit " . abs($bad_verbleibend) . " Tagen</span>";

    # kueche
    $kueche_vergangen = $json['kueche']['tage_vergangen'];
    $kueche_intervall = $json['kueche']['intervall_tage'];
    $kueche_verbleibend = $kueche_intervall - $kueche_vergangen;
    if ($kueche_verbleibend > 1)
        $kueche_faellig = "in " . $kueche_verbleibend . " Tagen";
    elseif ($kueche_verbleibend == 1)
        $kueche_faellig = "morgen";
    elseif ($kueche_verbleibend == 0)
        $kueche_faellig = "<span>heute</span>";
    elseif ($kueche_verbleibend == -1)
        $kueche_faellig = "<span'>gestern</span>";
    else
        $kueche_faellig = "<span>seit " . abs($kueche_verbleibend) . " Tagen</span>";

    # saugen
    $saugen_vergangen = $json['saugen']['tage_vergangen'];
    $saugen_intervall = $json['saugen']['intervall_tage'];
    $saugen_verbleibend = $saugen_intervall - $saugen_vergangen;
    if ($saugen_verbleibend > 1)
        $saugen_faellig = "in " . $saugen_verbleibend . " Tagen";
    elseif ($saugen_verbleibend == 1)
        $saugen_faellig = "morgen";
    elseif ($saugen_verbleibend == 0)
        $saugen_faellig = "<span>heute</span>";
    elseif ($saugen_verbleibend == -1)
        $saugen_faellig = "<span>gestern</span>";
    else
        $saugen_faellig = "<span>seit " . abs($saugen_verbleibend) . " Tagen</span>";

    # handtuecher
    $handtuecher_vergangen = $json['handtuecher']['tage_vergangen'];
    $handtuecher_intervall = $json['handtuecher']['intervall_tage'];
    $handtuecher_verbleibend = $handtuecher_intervall - $handtuecher_vergangen;
    if ($handtuecher_verbleibend > 1)
        $handtuecher_faellig = "in " . $handtuecher_verbleibend . " Tagen";
    elseif ($handtuecher_verbleibend == 1)
        $handtuecher_faellig = "morgen";
    elseif ($handtuecher_verbleibend == 0)
        $handtuecher_faellig = "<span>heute</span>";
    elseif ($handtuecher_verbleibend == -1)
        $handtuecher_faellig = "<span>gestern</span>";
    else
        $handtuecher_faellig = "<span>seit " . abs($handtuecher_verbleibend) . " Tagen</span>";

    # duschvorhang
    $duschvorhang_vergangen = $json['duschvorhang']['tage_vergangen'];
    $duschvorhang_intervall = $json['duschvorhang']['intervall_tage'];
    $duschvorhang_verbleibend = $duschvorhang_intervall - $duschvorhang_vergangen;
    if ($duschvorhang_verbleibend > 1)
        $duschvorhang_faellig = "in " . $duschvorhang_verbleibend . " Tagen";
    elseif ($duschvorhang_verbleibend == 1)
        $duschvorhang_faellig = "morgen";
    elseif ($duschvorhang_verbleibend == 0)
        $duschvorhang_faellig = "<span>heute</span>";
    elseif ($duschvorhang_verbleibend == -1)
        $duschvorhang_faellig = "<span>gestern</span>";
    else
        $duschvorhang_faellig = "<span>seit " . abs($duschvorhang_verbleibend) . " Tagen</span>";
?>

  <table id='clean_table' class="table table-striped">
    <thead class="<?php $currentTime = idate("H"); if ($currentTime < 18) {echo 'thead-light';} elseif ($currentTime > 18) {echo 'thead-dark';} ?>">
	    <tr>
	        <th scope="col">Aufgabe</th>
	        <th scope="col">Wer?</th>
	        <th scope="col">Fällig</th>
	        <th scope="col">Chatbot-Befehl</th>
      </tr>
      </thead>

      <tbody>
		<tr class="table-info">
		    <td scope="row" class="task" id="korrektur">Müll rausbringen</td>
		    <td><?php echo $json['muell']['dran']; ?></td>
		    <td>bei Bedarf</td>
		    <td>/muell</td>
		</tr>
		<tr class="table-info">
		    <td scope="row" class="task">Glas wegbringen</td>
		    <td><?php echo $json['glas']['dran']; ?></td>
		    <td>bei Bedarf</td>
		    <td>/glas</td>
		</tr>
		<tr class="<?php if ($bad_verbleibend == 1) {echo 'table-warning';} elseif ($bad_verbleibend == 0) {echo 'table-danger';} elseif ($bad_verbleibend < 0) {echo 'table-danger';} else {echo 'table-success';} ?>">
		    <td scope="row" class="task">Bäder putzen</td>
		    <td><?php echo $json['bad']['dran']; ?></td>
		    <td><?php echo $bad_faellig; ?></td>
		    <td>/bad</td>
		</tr>
		<tr class="<?php if ($kueche_verbleibend == 1) {echo 'table-warning';} elseif ($kueche_verbleibend == 0) {echo 'table-danger';} elseif ($kueche_verbleibend < 0) {echo 'table-danger';} else {echo 'table-success';} ?>">
		    <td scope="row" class="task">Küche putzen</td>
		    <td><?php echo $json['kueche']['dran']; ?></td>
		    <td><?php echo $kueche_faellig; ?></td>
		    <td>/kueche</td>
		</tr>
	  <tr class="<?php if ($saugen_verbleibend == 1) {echo 'table-warning';} elseif ($saugen_verbleibend == 0) {echo 'table-danger';} elseif ($saugen_verbleibend < 0) {echo 'table-danger';} else {echo 'table-success';} ?>">
		    <td scope="row" class="task">Staubsaugen</td>
		    <td><?php echo $json['saugen']['dran']; ?></td>
		    <td><?php echo $saugen_faellig; ?></td>
		    <td>/saugen</td>
		</tr>
		<tr class="<?php if ($handtuecher_verbleibend == 1) {echo 'table-warning';} elseif ($handtuecher_verbleibend == 0) {echo 'table-danger';} elseif ($handtuecher_verbleibend < 0) {echo 'table-danger';} else {echo 'table-success';} ?>">
		    <td scope="row" class="task">Handtücher waschen</td>
		    <td><?php echo $json['handtuecher']['dran']; ?></td>
		    <td><?php echo $handtuecher_faellig; ?></td>
		    <td>/handtuecher</td>
		</tr>
		<tr class="<?php if ($duschvorhang_verbleibend == 1) {echo 'table-warning';} elseif ($duschvorhang_verbleibend  == 0) {echo 'table-danger';} elseif ($duschvorhang_verbleibend < 0) {echo 'table-danger';} else {echo 'table-success';} ?>">
		    <td scope="row" class="task">Duschvorhänge waschen</td>
		    <td><?php echo $json['duschvorhang']['dran']; ?></td>
		    <td><?php echo $duschvorhang_faellig; ?></td>
		    <td>/duschvorhang</td>
		</tr>
  </tbody>
	</table>

<?php $cpu_temp = file_get_contents('../data/cpu_temp.txt'); ?>
<?php echo "CPU Temperatur: $cpu_temp;"?>


