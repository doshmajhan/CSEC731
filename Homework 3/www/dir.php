<?php
//GOOD: http://localhost/dir.php?name=Rob&lang=en.txt
//GOOD: http://localhost/dir.php?name=Rob&lang=fr.txt
//BAD: http://localhost/dir.php?name=Rob&lang=../../../../../etc/passwd

	$lang = $_GET['lang'];
	$name = $_GET['name'];
	$file = fopen($lang, "r");
	$greeting = fread($file,filesize($lang));
	fclose($file);

	echo $greeting . " " . $name . "!";
?>