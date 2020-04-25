<?php
	# Load timetable from JSON
    $str = file_get_contents('../data/timetable.json');
    $json = json_decode($str, true);

    $fahrt1_abfahrt = $json['trips'][0]['ab'];
	$fahrt2_abfahrt = $json['trips'][1]['ab'];
	$fahrt3_abfahrt = $json['trips'][2]['ab'];

	$fahrt1_tz = $json['trips'][0]['tz'];
	$fahrt2_tz = $json['trips'][1]['tz'];
	$fahrt3_tz = $json['trips'][2]['tz'];

	$fahrt1_ankunft = $json['trips'][0]['an'];
	$fahrt2_ankunft = $json['trips'][1]['an'];
	$fahrt3_ankunft = $json['trips'][2]['an'];

	$fahrt1_duration = $json['trips'][0]['duration'];
	$fahrt2_duration = $json['trips'][1]['duration'];
	$fahrt3_duration = $json['trips'][2]['duration'];

	$fahrt1_line = $json['trips'][0]['line'];
	$fahrt2_line = $json['trips'][1]['line'];
	$fahrt3_line = $json['trips'][2]['line'];
?>

<h5  id="table_header">Nahverkehr</h5>

<table id='heag_table' class="<?php $currentTime = idate("H"); if ($currentTime < 18) {echo 'table table-striped';} elseif ($currentTime > 18) {echo 'table table-dark table-striped';} ?>">
	<thead>
    <tr>
    <th scope="col">Verbindung</th>
		<th scope="col">HKP/Am Markt (zu Fuß: 10min)</th>
		<th scope="col">TZ Rhein Main (HBF)</th>
		<th scope="col">Darmstadt Schloss</th>
		<th scope="col">Dauer</th>

  </tr>
	</thead>
  <tbody>
	<tr>
    <td><?php if (count($fahrt1_line) > 1){ echo $fahrt1_line[0]; echo ", "; echo $fahrt1_line[1];} else {echo $fahrt1_line[0];}?></td>
		<td scope="row">ab: <?php echo $fahrt1_abfahrt;?></td>
		<td>an: <?php echo $fahrt1_tz;?></td>
		<td>an: <?php echo $fahrt1_ankunft;?></td>
		<td><?php echo $fahrt1_duration;?></td>
	</tr>
	<tr>
    <td><?php if (count($fahrt2_line) > 1){ echo $fahrt2_line[0]; echo ", "; echo $fahrt2_line[1];} else {echo $fahrt2_line[0];}?></td>
		<td scope="row">ab: <?php echo $fahrt2_abfahrt;?></td>
		<td>an: <?php echo $fahrt2_tz;?></td>
		<td>an: <?php echo $fahrt2_ankunft;?></td>
		<td><?php echo $fahrt2_duration;?></td>
	</tr>
	<tr>
    <td><?php if (count($fahrt3_line) > 1){ echo $fahrt3_line[0]; echo ", "; echo $fahrt3_line[1];} else {echo $fahrt3_line[0];}?></td>
		<td scope="row">ab: <?php echo $fahrt3_abfahrt;?></td>
		<td>an: <?php echo $fahrt3_tz;?></td>
		<td>an: <?php echo $fahrt3_ankunft;?></td>
		<td><?php echo $fahrt3_duration;?></td>

	</tr>
</tbody>
</table>
