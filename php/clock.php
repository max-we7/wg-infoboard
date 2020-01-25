<?php
	# Date and Clock
	date_default_timezone_set('Europe/Berlin');
	setlocale(LC_ALL, 'de_DE.utf8');
	$time = date('H:i');
	//$date = date('d. F Y');
	$date = strftime("%A, %e. %B %Y");
	//$days = array('Sonntag', 'Montag', 'Dienstag', 'Mittwoch','Donnerstag','Freitag', 'Samstag');
	//$day_of_week_int = date('w');
	//$day_of_week = $days[$day_of_week_int];
	//$date = $day_of_week . ", " . date('d.m.Y');
?>

<?php echo $time;?>
<br>
<div id="date"><?php echo $date;?></div>