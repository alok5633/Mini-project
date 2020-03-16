<?php

session_start();
 if(!isset($_SESSION['username'])){
     header('location:login.php');
 }

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <link rel="stylesheet" href="bootstrap.css">
    <link rel="stylesheet" href="style.css">
</head>
<body class="B">
 <div class="container">
    <h2 class="text-center text-success">Welcome <?php echo $_SESSION['username'];?></h2>
    <button onclick="window.location.href='logout.php'" class ="btn btn-primary" style="margin-left:auto;margin-right:auto;display:block;margin-top:22%;margin-bottom:0%">LogOut</button>
    </div>   
</body>
</html>