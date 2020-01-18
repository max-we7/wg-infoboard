<?php
	# Load putzplan from JSON
    $str = file_get_contents('../data/putzplan.json');
    $json = json_decode($str, true);

    $bad_vergangen = $json['bad']['tage_vergangen'];
    $bad_intervall = $json['bad']['intervall_tage'];
    $bad_verbleibend = $bad_intervall - $bad_vergangen;
    if ($bad_verbleibend > 1)
        $bad_faellig = "in " . $bad_verbleibend . " Tagen";
    elseif ($bad_verbleibend == 1)
        $bad_faellig = "morgen";
    elseif ($bad_verbleibend == 0)
        $bad_faellig = "heute";
    elseif ($bad_verbleibend == -1)
        $bad_faellig = "gestern";
    else
        $bad_faellig = "seit " . abs($bad_verbleibend) . " Tagen"
?>

	<table class="putzplan">
	    <tr>
	        <th>Aufgabe</th>
	        <th>Wer?</th>
	        <th>Fällig</th>
		<tr>
		    <th>Müll rausbringen</th>
		    <td><?php echo $json['muell']['dran']; ?></td>
		    <td>bei Bedarf</td>
		</tr>
		<tr>
		    <th>Glas wegbringen</th>
		    <td><?php echo $json['glas']['dran']; ?></td>
		    <td>bei Bedarf</td>
		</tr>
		<tr>
		    <th>Bäder putzen</th>
		    <td><?php echo $json['bad']['dran']; ?></td>
		    <td><?php echo $bad_faellig; ?></td>
		</tr>
		<tr>
		    <th>Küche putzen</th>
		    <td><?php echo $json['kueche']['dran']; ?></td>
		    <td></td>
		</tr>
		<tr>
		    <th>Staubsaugen</th>
		    <td><?php echo $json['saugen']['dran']; ?></td>
		    <td></td>
		</tr>
		<tr>
		    <th>Handtücher waschen</th>
		    <td><?php echo $json['handtuecher']['dran']; ?></td>
		    <td></td>
		</tr>
		<tr>
		    <th>Duschvorhänge waschen</th>
		    <td><?php echo $json['duschvorhang']['dran']; ?></td>
		    <td></td>
		</tr>
	</table>