<?php
//setting header to json
//database
$host = "localhost";
$user = "cyber";
$pass = "Unab.2021";

// Selected database
$schema = "CyberAware_copia";

// Create connection

$mysqli = new mysqli($host, $user, $pass, $schema);
$mysqli->set_charset("utf8"); 

if(!$mysqli){
  die("Connection failed: " . $mysqli->error);
}

//query to get data from the table
$query = "SELECT date_format(fecha_creacion,'%Y-%m-%d %H') as fecha_creacion, count(1) as cantidad FROM stemming GROUP BY 1 ORDER BY count(1) ASC";

//execute query
$result = $mysqli->query($query);

//loop through the returned data
$data = [];
$fechas = array();
$cantidad =array();
foreach ($result as $row) {
  $cantidad[] = (int)$row['cantidad'];
  $fechas[] = $row['fecha_creacion'];
  $data[] = $row;
}

//free memory associated with result
$result->close();

//close connection
$mysqli->close();
//now print the data
//print json_encode($fechas);
?>
