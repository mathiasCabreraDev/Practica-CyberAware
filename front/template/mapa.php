<html lang="es">

<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	<title>Mapa</title>
	<meta name="description" content="CyberAware">
	<meta name="author" content="Nicolas Gonzalez">
	<link href="static/css/bootstrap.min.css" rel="stylesheet">
	<link href="static/css/custom.css" rel="stylesheet">
	<link rel="stylesheet" href="https://bossanova.uk/jsuites/v2/jsuites.css" type="text/css" />		
	<link rel="stylesheet" href="https://bossanova.uk/jexcel/v3/jexcel.css" type="text/css" />
</head>

<body>
	<?php 
		$baseDirectory = getcwd();
		//exec("python $baseDirectory/Back/tweets/generar/GenerarHTML.py 707121254784872448");
		//include_once("$baseDirectory/Back/tweets/generar/mapa.html");
		//fsocket("localhost:8081", "{data:hola}")
		$id_retweet = $_GET['id'];
		$curl = curl_init();
		curl_setopt($curl, CURLOPT_URL, 'localhost:5000/mapa/'.$id_retweet);
		curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
		curl_exec($curl);
		include_once("$baseDirectory/back/tweets/generar/mapa.html");
	?>
