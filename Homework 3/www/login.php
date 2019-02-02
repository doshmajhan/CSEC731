<?php

	if(empty($_SERVER['HTTP_REFERER']) || ($_SERVER['HTTP_REFERER'] != "http://localhost/login.html" && $_SERVER['HTTP_REFERER'] != "http://localhost/login.php"))
	{
		header("Location: http://localhost/login.html");
	}
	else if($_SERVER['HTTP_REFERER'] == "http://localhost/login.php")
	{
		session_destroy();
		header("Location: http://localhost/login.html");
	}
	else{
		if(session_status() == PHP_SESSION_NONE)
		{
			if(empty($_POST['id']) || empty($_POST['pw']))
			{
				header("Location: http://localhost/login.html");
			}

			$user = $_POST['id'];
			$pass = $_POST['pw'];
	
			$connection = mysqli_connect("10.0.2.33", "webapp", "webapp_password", "myapp");
	
			$sql_query = "SELECT id FROM users WHERE id='$user' and password='$pass'";

			$query_result = mysqli_query($connection, $sql_query);
			if(mysqli_num_rows($query_result)==0)
			{
				echo $sql_query;
				header("Location: http://localhost/login.html");
			}
			else
			{
				session_start();
				$_SESSION["userid"] = $user;
				echo "Your ID# is: " . $_SESSION["userid"] . "<br>";
				echo "You are logged in!<br>";
				echo "<form action='login.php' method='POST'>";
				echo "<input type='submit' value='Log Out'/>";
				echo "</form>";
			}
		}
		else{
			session_start();
			echo "Your ID# is: " . $_SESSION["userid"] . "<br>";
			echo "You are logged in!<br>";
			echo "<form action='login.php' method='POST'>";
			echo "<input type='submit' value='Log Out'/>";
			echo "</form>";
		}
	}

?>