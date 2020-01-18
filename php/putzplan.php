<?php
	# Load putzplan from JSON
    $str = file_get_contents('../data/putzplan.json');
    $json = json_decode($str, true);

    # bad
    $bad_vergangen = $json['bad']['tage_vergangen'];
    $bad_intervall = $json['bad']['intervall_tage'];
    $bad_verbleibend = $bad_intervall - $bad_vergangen;
    if ($bad_verbleibend > 1)
        $bad_faellig = "in " . $bad_verbleibend . " Tagen";
    elseif ($bad_verbleibend == 1)
        $bad_faellig = "morgen";
    elseif ($bad_verbleibend == 0)
        $bad_faellig = "<span class='due'>heute</span>";
    elseif ($bad_verbleibend == -1)
        $bad_faellig = "<span class='overdue'>gestern</span>";
    else
        $bad_faellig = "<span class='overdue'>seit " . abs($bad_verbleibend) . " Tagen</span>";

    # kueche
    $kueche_vergangen = $json['kueche']['tage_vergangen'];
    $kueche_intervall = $json['kueche']['intervall_tage'];
    $kueche_verbleibend = $kueche_intervall - $kueche_vergangen;
    if ($kueche_verbleibend > 1)
        $kueche_faellig = "in " . $kueche_verbleibend . " Tagen";
    elseif ($kueche_verbleibend == 1)
        $kueche_faellig = "morgen";
    elseif ($kueche_verbleibend == 0)
        $kueche_faellig = "<span class='due'>heute</span>";
    elseif ($kueche_verbleibend == -1)
        $kueche_faellig = "<span class='overdue'>gestern</span>";
    else
        $kueche_faellig = "<span class='overdue'>seit " . abs($kueche_verbleibend) . " Tagen</span>";

    # saugen
    $saugen_vergangen = $json['saugen']['tage_vergangen'];
    $saugen_intervall = $json['saugen']['intervall_tage'];
    $saugen_verbleibend = $saugen_intervall - $saugen_vergangen;
    if ($saugen_verbleibend > 1)
        $saugen_faellig = "in " . $saugen_verbleibend . " Tagen";
    elseif ($saugen_verbleibend == 1)
        $saugen_faellig = "morgen";
    elseif ($saugen_verbleibend == 0)
        $saugen_faellig = "<span class='due'>heute</span>";
    elseif ($saugen_verbleibend == -1)
        $saugen_faellig = "<span class='overdue'>gestern</span>";
    else
        $saugen_faellig = "<span class='overdue'>seit " . abs($saugen_verbleibend) . " Tagen</span>";

    # handtuecher
    $handtuecher_vergangen = $json['handtuecher']['tage_vergangen'];
    $handtuecher_intervall = $json['handtuecher']['intervall_tage'];
    $handtuecher_verbleibend = $handtuecher_intervall - $handtuecher_vergangen;
    if ($handtuecher_verbleibend > 1)
        $handtuecher_faellig = "in " . $handtuecher_verbleibend . " Tagen";
    elseif ($handtuecher_verbleibend == 1)
        $handtuecher_faellig = "morgen";
    elseif ($handtuecher_verbleibend == 0)
        $handtuecher_faellig = "<span class='due'>heute</span>";
    elseif ($handtuecher_verbleibend == -1)
        $handtuecher_faellig = "<span class='overdue'>gestern</span>";
    else
        $handtuecher_faellig = "<span class='overdue'>seit " . abs($handtuecher_verbleibend) . " Tagen</span>";

    # duschvorhang
    $duschvorhang_vergangen = $json['duschvorhang']['tage_vergangen'];
    $duschvorhang_intervall = $json['duschvorhang']['intervall_tage'];
    $duschvorhang_verbleibend = $duschvorhang_intervall - $duschvorhang_vergangen;
    if ($duschvorhang_verbleibend > 1)
        $duschvorhang_faellig = "in " . $duschvorhang_verbleibend . " Tagen";
    elseif ($duschvorhang_verbleibend == 1)
        $duschvorhang_faellig = "morgen";
    elseif ($duschvorhang_verbleibend == 0)
        $duschvorhang_faellig = "<span class='due'>heute</span>";
    elseif ($duschvorhang_verbleibend == -1)
        $duschvorhang_faellig = "<span class='overdue'>gestern</span>";
    else
        $duschvorhang_faellig = "<span class='overdue'>seit " . abs($duschvorhang_verbleibend) . " Tagen</span>";
?>

	<table class="putzplan">
	    <tr>
	        <th>Aufgabe</th>
	        <th>Wer?</th>
	        <th>Fällig</th>
	        <th>Chatbot-Befehl</th>
		<tr>
		    <th>Müll rausbringen</th>
		    <td><?php echo $json['muell']['dran']; ?></td>
		    <td>bei Bedarf</td>
		    <td>/muell</td>
		</tr>
		<tr>
		    <th>Glas wegbringen</th>
		    <td><?php echo $json['glas']['dran']; ?></td>
		    <td>bei Bedarf</td>
		    <td>/glas</td>
		</tr>
		<tr>
		    <th>Bäder putzen</th>
		    <td><?php echo $json['bad']['dran']; ?></td>
		    <td><?php echo $bad_faellig; ?></td>
		    <td>/bad</td>
		</tr>
		<tr>
		    <th>Küche putzen</th>
		    <td><?php echo $json['kueche']['dran']; ?></td>
		    <td><?php echo $kueche_faellig; ?></td>
		    <td>/kueche</td>
		</tr>
		<tr>
		    <th>Staubsaugen</th>
		    <td><?php echo $json['saugen']['dran']; ?></td>
		    <td><?php echo $saugen_faellig; ?></td>
		    <td>/saugen</td>
		</tr>
		<tr>
		    <th>Handtücher waschen</th>
		    <td><?php echo $json['handtuecher']['dran']; ?></td>
		    <td><?php echo $handtuecher_faellig; ?></td>
		    <td>/handtuecher</td>
		</tr>
		<tr>
		    <th>Duschvorhänge waschen</th>
		    <td><?php echo $json['duschvorhang']['dran']; ?></td>
		    <td><?php echo $duschvorhang_faellig; ?></td>
		    <td>/duschvorhang</td>
		</tr>
	</table>