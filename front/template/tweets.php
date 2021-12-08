<?php

$baseDirectory = getcwd()."/front";
include_once( "$baseDirectory/routes.php" );

?><!doctype html>
<html lang="es">

<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	<title>CyberAware</title>
	<meta name="description" content="CyberAware">
	<meta name="author" content="Nicolas Gonzalez">
	<link href="static/css/bootstrap.min.css" rel="stylesheet">
	<link href="static/css/custom.css" rel="stylesheet">
	<link rel="stylesheet" href="static/css/buscador.css">
	<link rel="stylesheet" href="https://bossanova.uk/jsuites/v2/jsuites.css" type="text/css" />		
	<link rel="stylesheet" href="https://bossanova.uk/jexcel/v3/jexcel.css" type="text/css" />
	<style>
		.my-custom-scrollbar {
			position: relative;
			height: 400px;
			overflow: auto;
		}
		.table-wrapper-scroll-y {
			display: block;
			margin: 10px 20px 15px 20px;
		}
	
		.aboutvar{
            font-family: Arial;
            font-size : 15px;
            font-weight: 300;
        }
		
	</style>
</head>
<body>
    <nav class="navbar navbar-dark bg-dark">
		<a class="navbar-brand" href="<?php nya("tweet"); ?>">CyberAware</a>
		<a class="navbar-brand aboutvar" href="<?php nya("about"); ?>"> Quienes Somos </a>
    </nav>
    <?php
        $baseDirectory = getcwd();
        include_once( "$baseDirectory/back/tweets/tabla_tweets.php" );
    ?>
	<div class="generar-mapa">
		<?php 
			include_once( "$baseDirectory/back/grafico.php" );
		?>
	</div>
	<h3 class="text-center">Buscador de Tweets</h3>
	<form class="formulario" action="" method="post">
		<input class="form-control" type="text" name="valorTweet" placeholder="Ingrese Texto">
		<button type="submit" name="submit" valur="Submit" class="btn btn-primary mb-2">Buscar</button>
	</form>
	<?php
		if (isset($_POST['submit'])) {
			$valorTweet  = $_POST["valorTweet"];
			include_once ("$baseDirectory/back/tabla-buscador.php");
		}
	?>
	<div class= "mapa">
			<?php include_once( "$baseDirectory/back/tweets/mapa_inicial.html"); ?>
	</div>
	
</body>
