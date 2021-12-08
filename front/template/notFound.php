<?php

$baseDirectory = getcwd()."/front";
include_once( "$baseDirectory/routes.php" );

?><!doctype html><html lang="en">
<head>

<meta charset="utf-8">

<title>Pagina no Encontrada</title>

	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

	<meta name="description" content="CyberAware">
	<meta name="author" content="Nicolas Gonzalez">
	<link href="static/css/bootstrap.min.css" rel="stylesheet">
	<link href="static/css/custom.css" rel="stylesheet">

<style>

      html,body {

			margin:0px;
			padding:0px;
			height:100%;
      }

	
      body {

		background: linear-gradient(rgba(0, 96, 96, 0.49), rgba(9, 25, 28, 0.52)), url(static/assets/centro.jpg) center / cover;
		text-align: center;
      }

      .container {

		vertical-align:top;

        max-width: 600px;
        padding: 45px;
        border: 1px solid #b3b3b3;
        border-radius: 4px;
        margin: 0 auto;
        box-shadow: 0 1px 10px #a7a7a7, inset 0 1px 0 #fff;
        background: #fcfcfc;
		
		margin-top: 100px;
		display: inline-block;
		
		text-align: left;
      }

</style>
</head>
<body>

<div class="container">

<h1>No Encontrado</h1> <p>Parece que la pagina solicitada	 no se encuentra disponible.</p>
<p>Esto puede deberse a que:</p>

<ul> <li>el enlace es incorrecto</li> <li>el enlace ha expirado</li> </ul>

<ul>
      <a href="" onclick="history.back(-1)" class="m-2 btn btn-primary">Volver a la pagina anterior</a>
      <a href="<?php nya("home"); ?>" class="m-2 btn btn-primary">Ir a la pagina de inicio</a>
</ul>

</div>


	<script src="static/js/lib/jquery-3.4.1.min.js"></script>
	<script src="static/js/lib/popper.min.js"></script>
	<script src="static/js/lib/bootstrap.min.js"></script>

</body>
</html>