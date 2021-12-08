<?php

  class Route {

    public $name = "";
    public $file = "";

    function __construct($name, $file) {

        $this->name = $name;
        $this->file = $file;
    }

    public function __toString() {

      return "?m=".$this->name;
    }
  }

  function nya($key) {

    global $routes;
    echo $routes[$key];

    // Basicamente en lugar de escribir:
    // echo $routes["elefante"];

    // Estariamos escribiendo:
    // nya("elefante");
  }

  // OJO:
  // la pagina por defecto (a la que se accede cuando no se ingresa parametro GET al '?m=' )
  // siempre sera la primera del arreglo, en este caso 'home'

  $routes = array(

    "tweet" => new Route(
      "tweets",
      "tweets.php"
    ),
    "mapa" => new Route(
      "mapa",
      "mapa.php"
    ),
    "about" => new Route(
      "about",
      "about.php"
    ),
    "comunidades" => new Route(
      "comunidades",
      "comunidades.php"
    ),
    "editar" => new Route(
      "editar",
      "editar.php"
    )
  );

?>
