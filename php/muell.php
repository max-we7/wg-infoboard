<?php
	# Load putzplan from JSON
    $str = file_get_contents('../data/zaw.json');
    $json = json_decode($str, true);
    $gelb = $json["gelb"];
    $schwarz = $json["schwarz"];
    $blau = $json["blau"];
    $gruen = $json["gruen"];

    if ($schwarz > 1)
        $schwarz_faellig = "in " . $schwarz . " Tagen";
    elseif ($schwarz == 1)
        $schwarz_faellig = "<span class='table-warning'>morgen</span>";
    elseif ($schwarz == 0)
        $schwarz_faellig = "<span class='table-danger'>heute</span>";

    if ($gelb > 1)
        $gelb_faellig = "in " . $gelb . " Tagen";
    elseif ($gelb == 1)
        $gelb_faellig = "<span class='table-warning'>morgen</span>";
    elseif ($gelb == 0)
        $gelb_faellig = "<span class='table-danger'>heute</span>";

    if ($blau > 1)
        $blau_faellig = "in " . $blau . " Tagen";
    elseif ($blau == 1)
        $blau_faellig = "<span class='table-warning'>morgen</span>";
    elseif ($blau == 0)
        $blau_faellig = "<span class='table-danger'>heute</span>";

    if ($gruen > 1)
        $gruen_faellig = "in " . $gruen . " Tagen";
    elseif ($gruen == 1)
        $gruen_faellig = "<span class='table-warning'>morgen</span>";
    elseif ($gruen == 0)
        $gruen_faellig = "<span class='table-danger'>heute</span>";
?>

<table class="table">
    <tr class="<?php if ($schwarz == 1) {echo 'table-warning';} elseif ($schwarz  == 0) {echo 'table-danger';} else {echo 'table-success';} ?>">
        <th scope="row">Restmüll:</th>
        <td><?php echo $schwarz_faellig;?></td>
    </tr>
    <tr class="<?php if ($blau == 1) {echo 'table-warning';} elseif ($blau  == 0) {echo 'table-danger';} else {echo 'table-success';} ?>">
        <th scope="row">Papiermüll:</th>
        <td><?php echo $blau_faellig;?></td>
    </tr>
    <tr class="<?php if ($gruen == 1) {echo 'table-warning';} elseif ($gruen  == 0) {echo 'table-danger';} else {echo 'table-success';} ?>">
        <th scope="row">Biomüll:</th>
        <td><?php echo $gruen_faellig;?></td>
    <tr>
    </tr>
    <tr class="<?php if ($gelb == 1) {echo 'table-warning';} elseif ($gelb  == 0) {echo 'table-danger';} else {echo 'table-success';} ?>">
        <th scope="row">Gelber Sack:</th>
        <td><?php echo $gelb_faellig;?></td>
    </tr>
</table>
