<?php
    $host = 'localhost';
    $user = 'cyber';
    $pass = 'Unab.2021';
    $schema = 'CyberAware_copia';
    
    $id = $_GET['id'];
    $query = "UPDATE comunidades SET nombre_comunidades = (".$nombre.") WHERE id= ".$id.";";
    // Create connection
    
    $db = new mysqli($host, $user, $pass, $schema);
    $db->set_charset("utf8");        
        
    if(isset($_POST['update'])){
        $name = $_POST['name'];
        $query = "UPDATE comunidades SET nombre_comunidades = (".$name.") WHERE id= ".$id.";";
        $edit = mysqli_query($db, $query);
        if($edit){
            mysqli_close($db);
            header('Location: /k-cmpPOO/');
            exit;
        }else{
            echo mysqli_error();
        }
    }
    
?>
<h3>Nombrar comunidad</h3>
<h4><?php echo $id; ?></h4>
<form method="POST">
    <input type="text" name="name" placeholder="Ingresar nombre" Requiered>
    <input type="submit" name="update" value="Update">
</form>


               
