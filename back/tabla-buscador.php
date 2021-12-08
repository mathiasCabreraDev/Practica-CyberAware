<?php
    //echo $valorTweet;
    $params = array ('frase' => $valorTweet);
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, 'localhost:5000/busqueda');
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_POST, true);
    curl_setopt($curl, CURLOPT_POSTFIELDS, $params);
    $comunidad = curl_exec($curl);

    if ($comunidad == 0) {
?>
    <h6 class="text-center"> Tweet ingresado no pertenece a ninguna comunidad</h6>
<?php }else { ?>
    <h6 class="text-center"> <?php echo "Tweet ingresado pertenece a la comunidad: $comunidad" ?> </h6>
    <h4 class="text-center"> <?php echo "10 Tweets mas relevenates de la comunidad: $comunidad" ?> </h4>
<?php
    $host = "localhost";
    $user = "root";
    $pass = "Unab.2019";
    $schema = "CyberAware_copia";
    $db = new mysqli($host, $user, $pass, $schema);
    $db->set_charset("utf8");  

    $queryComunidad = "SELECT stemming_id FROM rel_stemming_comunidades WHERE comunidades_id = " . $comunidad . "ORDER BY grado DESC LIMIT 10";

    $resultados = mysqli_query($db, $queryComunidad);
    echo "
        <div class='table-wrapper-scroll-y my-custom-scrollbar'>
        <table class='table table-bordered table-striped mb-0'> <thead>
                <tr>
                    <th>Usuario</th>
                    <th>Tweet</th>
                    <th>Ubicaion</th>
                    <th>Fecha</th>
                </tr> </thead> <tbody>";
    while ($consulta = mysqli_fetch_array($resultados)){
        $informacion_tweet = "SELECT s.nombre_usuario, t.texto, s.ubicacion, s.fecha_creacion FROM stemming as s 
                              INNER JOIN tweets as t on t.tweet_id = s.tweet_id
                              WHERE s.id = " . $consulta['stemming_id'];
        $datos_tweet = mysqli_query($db, $informacion_tweet);
        while($dato_tweet = mysqli_fetch_array($datos_tweet)){
            echo "<tr>
                    <td>" . $dato_tweet["nombre_usuario"]."</td>
                    <td>" . $dato_tweet["texto"]."</td>
                    <td>" . $dato_tweet["ubicacion"]."</td>
                    <td>" . $dato_tweet["fecha_creacion"]."</td>
                </tr>";
        }
    }
    echo "</tbody></table></div>";
    }
?>


