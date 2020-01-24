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
        $schwarz_faellig = "<span class='due'>morgen</span>";
    elseif ($schwarz == 0)
        $schwarz_faellig = "<span class='overdue'>heute</span>";

    if ($gelb > 1)
        $gelb_faellig = "in " . $gelb . " Tagen";
    elseif ($gelb == 1)
        $gelb_faellig = "<span class='due'>morgen</span>";
    elseif ($gelb == 0)
        $gelb_faellig = "<span class='overdue'>heute</span>";

    if ($blau > 1)
        $blau_faellig = "in " . $blau . " Tagen";
    elseif ($blau == 1)
        $blau_faellig = "<span class='due'>morgen</span>";
    elseif ($blau == 0)
        $blau_faellig = "<span class='overdue'>heute</span>";

    if ($gruen > 1)
        $gruen_faellig = "in " . $gruen . " Tagen";
    elseif ($gruen == 1)
        $gruen_faellig = "<span class='due'>morgen</span>";
    elseif ($gruen == 0)
        $gruen_faellig = "<span class='overdue'>heute</span>";
?>

<table class="fahrttabelle">
    <tr>
        <td>Restmüll:<br><?php echo $schwarz_faellig;?></td>
        <td>Papiermüll:<br><?php echo $blau_faellig;?></td>
    </tr>
    <tr>
        <td>Biomüll:<br><?php echo $gruen_faellig;?></td>
        <td>Gelber Sack:<br><?php echo $gelb_faellig;?></td>
    </tr>
</table>