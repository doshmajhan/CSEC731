<?php
	$userid = $_GET['id'];
	
	$connection = mysqli_connect("10.0.2.33", "webapp", "webapp_password", "myapp");

	if(!$connection)
	{
		die("DB Connection failed");
	}
	
	$sql_query = "SELECT * FROM users WHERE id='$userid'";

	$query_result = mysqli_query($connection, $sql_query);
	if(mysqli_num_rows($query_result)==0)
	{
		echo "Sorry, ID #$userid was not found!";
	}
	else
	{
		
		while ($row = mysqli_fetch_assoc($query_result))
		{
			
			echo $row['id'] . " " . $row['first'] . " ";
			echo $row['last'] . " " . $row['password'];
		}
		
		mysqli_close($connection);

		// echo "<br><br><br> $sql_query";
	}
	
?>