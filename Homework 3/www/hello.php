<?php
	// localhost/hello.php?first=Rob&last=Olson

	$fn = $_POST['first'];
	$ln = $_POST['last'];

	echo "<b>Hello</b> $fn $ln!";

?>