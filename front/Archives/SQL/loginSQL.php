<?php
    session_start();
    require "connect.php";
    
    $mail = $_POST["mail"];
    $psw = $_POST["psw"];
    
    $sql = "SELECT * FROM Compte WHERE Mail='$mail' AND Psw='$psw'";
    $result = $conn->query($sql);
    
    if ($result->num_rows > 0) {
        // output data of each row
        while($row = $result->fetch_assoc()) {
            $_SESSION["ID"] = $row["IDCompte"];
            header('Location: ../main_page.php');
        }
    } else {
        $_SESSION["WR"] = "wrong";
        header('Location: ../index.php');
    }
    $conn->close();
?>