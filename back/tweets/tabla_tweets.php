<?php
        $host = "localhost";
        $user = "cyber";
        $pass = "Unab.2021";
        
        // Selected database
        $schema = "CyberAware_copia";
        
        // Create connection
        
        $db = new mysqli($host, $user, $pass, $schema);
        $db->set_charset("utf8");        
        
        $ultimos_tweets = "SELECT id FROM stemming ORDER BY fecha_creacion DESC limit 20";
        $resultados = mysqli_query($db, $ultimos_tweets);
        echo "
        <div class='table-wrapper-scroll-y my-custom-scrollbar'>
        <h3 class='text-center'>&Uacuteltimos 20 tweets</h3>
        <table class='table table-bordered table-striped mb-0'> <thead>
                <tr>
                    <th>Comunidad</th>
                    <th>Usuario</th>
                    <th>Tweet</th>
                    <th>Ubicaion</th>
                    <th>Fecha</th>
                </tr> </thead> <tbody>";
        while ($consulta = mysqli_fetch_array($resultados)){
	    $informacion_tweet = "SELECT s.tweet_id, r.comunidades_id, s.nombre_usuario, t.texto, if(s.ubicacion='nan' , 'Ubicacion no especificada' , s.ubicacion) as ubicacion, s.fecha_creacion FROM tweets as t
            INNER JOIN stemming as s on t.tweet_id = s.tweet_id
            INNER JOIN rel_stemming_comunidades AS r ON s.id = r.stemming_id
            where r.grado = (SELECT MAX(grado) FROM rel_stemming_comunidades WHERE stemming_id =" . $consulta['id'] . ")and r.stemming_id = " . $consulta['id'] ." limit 1";
	
	    $datos_tweet = mysqli_query($db, $informacion_tweet);
            while($dato_tweet = mysqli_fetch_array($datos_tweet)){
                echo "<tr>
                        <td>" . $dato_tweet["comunidades_id"]. "</td>
                        <td>" . $dato_tweet["nombre_usuario"]."</td>
                        <td>" . $dato_tweet["texto"]."</td>
                        <td>" . $dato_tweet["ubicacion"]."</td>
                        <td>" . $dato_tweet["fecha_creacion"]."</td>
                </tr>";
            }
        }
        echo "</tbody></table></div>";
?>
