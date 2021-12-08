<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CyberAware</title>
    <link href="static/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="static/css/grid.css">
    <style>
        .about{
            text-align: center;
            margin: 20 0 0 0;
        }
        .aboutvar{
            font-family: Arial;
            font-size : 15px;
            font-weight: 300;
        }
        hr{
            border-color: #f08080; 
            border-width: 3px;
            max-width: 150px
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-dark bg-dark">
		<a class="navbar-brand" href="<?php nya("tweet"); ?>">CyberAware</a>
		<a class="navbar-brand aboutvar" href="<?php nya("about"); ?>"> Quienes Somos </a>
    </nav>
    <h2 class="about">Quienes Somos</h2>
    <hr class="primary">
    <div class="grid-container">
        <div class="profesora">
            <img class="imagen" src="images/2.png" alt="Romina">
        </div>
        <div class="nicolas">
            <img class="imagen" src="images/1.png" alt="Nicolas">
        </div>
        <div class="descripcion_profe">
            Profesora de Ingeniería Civil Informática, Universidad Andrés Bello
        </div>
        <div class="descripcion_nico">
        Estudiante de Ingeniería Civil Informática, Universidad Andrés Bello
        </div>
        <div class="nombre_profe">
            <h4>Romina Torres</h4>
        </div>
        <div class="nombre_nicolas">
            <h4>Nicolás González</h4>
        </div>
        <footer>
            UNAB COSAS ETC
        </footer>

    </div>
</body>
</html>
