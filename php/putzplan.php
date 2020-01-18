<?php
	# Load putzplan from JSON
    $str = file_get_contents('../data/putzplan.json');
    $json = json_decode($str, true);
?>

	<table class="putzplan">
	    <tr>
	        <th>Aufgabe</th>
	        <th>Wer?</th>
	        <th>Fällig</th>
		<tr>
		    <th>Müll rausbringen</th>
		    <td><?php echo $json['muell']['dran'] ?></td>
		    <td></td>
		</tr>
		<tr>
		    <th>Glas wegbringen</th>
		    <td></td>
		    <td></td>
		</tr>
		<tr>
		    <th>Bäder putzen</th>
		    <td></td>
		    <td></td>
		</tr>
		<tr>
		    <th>Küche putzen</th>
		    <td></td>
		    <td></td>
		</tr>
		<tr>
		    <th>Staubsaugen</th>
		    <td></td>
		    <td></td>
		</tr>
		<tr>
		    <th>Handtücher waschen</th>
		    <td></td>
		    <td></td>
		</tr>
		<tr>
		    <th>Duschvorhänge waschen</th>
		    <td></td>
		    <td></td>
		</tr>
	</table>