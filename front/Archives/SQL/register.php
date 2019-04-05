<?php
    require "connect.php";
    
    $name = $_POST["name"];
    $firstName = $_POST["firstName"];
    $mail = $_POST["mail"];
    $psw = $_POST["psw"];
    
    //echo $name . " " . $firstName . " " . $mail . " " . $psw;
    
    $sql = "INSERT INTO Compte (Nom, Prenom, Mail, Psw)
        VALUES
            ('$name', '$firstName', '$mail', '$psw');
        ";
    
    if ($conn->query($sql) === TRUE) {
        echo "New record created successfully";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
    $conn->close();
?>