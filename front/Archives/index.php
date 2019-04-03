
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8"/>
	<title>UMatch</title>
	<link rel="stylesheet" type="text/css" href="CSS/login.css"></link>
</head>
<body>
    
<div class="login-page">
    <div class="form">
        <form class="register-form"  action="SQL/register.php" method="post">
            <input type="text" name="name" placeholder="Name" required/>
            <input type="text" name="firstName" placeholder="First name" required/>
            <input type="email" name="mail" placeholder="Email address" required/>
            <input type="password" name="psw" placeholder="Password" required/>
            <button type="submit">Create</button>
            <p class="message">Already registered? <a href="#">Sign In</a></p>
        </form>
        <form class="login-form" action="SQL/loginSQL.php" method="post">
            <input type="email" name="mail" placeholder="Mail" required/>
            <input type="password" name="psw" placeholder="Password" required/>
            <button>Login</button>
            <p class="message">Not registered? <a href="#">Create an account</a></p>
        </form>
    </div>
    <div id="errorLogin">
    </div>
</div>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>

<script>

    $('.message a').click(function(){
       $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
    });
    
    function wrongLogin() {
      console.log("Wrong Mail or Password.");
      var errorLogin = document.getElementById("errorLogin");
      errorLogin.innerHTML = "Wrong Mail or Password.";
      errorLogin.style.color = 'white';
      errorLogin.style.textAlign = "center";
    }
    
    
</script>

<?php
    session_start();
    
	if(($_SESSION["WR"]) == "wrong"){
	        echo '<script type="text/javascript">',
             'wrongLogin();',
             '</script>';
	}
	unset($_SESSION['WR']);
	unset($_SESSION['ID']);
?>
</body>
</html>
