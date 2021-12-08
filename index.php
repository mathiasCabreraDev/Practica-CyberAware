<?php

$baseDirectory = getcwd()."/front";
include_once( "$baseDirectory/routes.php" );

// Seleccionamos el modulo deseado
$module = @$_GET["m"];

// Si no se ha ingresado modulo se mostrara la pagina por defecto
if ( $module == "" ) {

  $defaultRoute = reset($routes);

  // En caso de que alguien meta mano y no existan paginas registradas
  // Se mostrara la del error 404
  if ( $defaultRoute !== FALSE ) {

    include( $baseDirectory."/template/".$defaultRoute->file );
  }
  else {

    include( $baseDirectory."/template/notFound.php" );
  }
}
else {

  // Se busca el modulo deseado dentro de las paginas registradas
  foreach ( $routes as $route ) {

    if ( $route->name == $module ) {

      // Si coincide con un registro se mostrara
      include( $baseDirectory."/template/".$route->file );
      die();
    }
  }

  // Y si no error 404
  include( $baseDirectory."/template/notFound.php" );
}

?>
