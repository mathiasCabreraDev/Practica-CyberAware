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
    <h2 class="about">Comunidades</h2>
    <hr class="primary">
        <?php 
            $host = 'localhost';
            $user = 'cyber';
            $pass = 'Unab.2021';
            $schema = 'CyberAware_copia';
            
            
            $db = new mysqli($host, $user, $pass, $schema);
            $db->set_charset("utf8");        
            
            $comunidades = "SELECT id, nombre_comunidades, texto_comunidades FROM comunidades";
            $resultados = mysqli_query($db, $comunidades);
            ?>
            <div class='table-wrapper-scroll-y my-custom-scrollbar'>
            <h3 class='text-center'>Comunidades</h3>
            <table class='table table-bordered table-striped mb-0'> <thead>
                    <tr>
                        <th>Comunidad</th>
                        <th>texto comunidad</th>
                        <th>id</th>
                        <th>Nombrar</th>
                    </tr> </thead> <tbody>
            <?php while ($consulta = mysqli_fetch_array($resultados)){ ?>
                    <tr>
                        <td><?php echo $consulta["nombre_comunidades"]; ?></td>
                        <td><?php echo $consulta["texto_comunidades"]; ?></td>
                        <td><?php echo $consulta["id"]; ?></td>
                        <?php $baseDirectory = getcwd(); ?>
                        <td><a href="/k-cmpPOO/front/template/editar.php?id=<?php echo $consulta["id"];?>">Nombrar</a></td>   
                    </tr>
            <?php            
            } ?>
            </tbody></table></div>
        
</body>
</html>