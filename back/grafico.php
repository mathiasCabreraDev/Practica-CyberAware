<?php
    $baseDirectory = getcwd();
    include_once( "$baseDirectory/front/routes.php" );
    include_once( "$baseDirectory/back/data-grafico.php");
?>
<!doctype html>
<script src="https://code.highcharts.com/highcharts.js"></script>
<link rel="stylesheet" href="static/css/grafico.css">
<div class="container-grafico">
    <div class = "grafico" id="container"></div>
</div>

<script>
    document.addEventListener('DOMContentLoaded', function () {
        var myChart = Highcharts.chart('container', {
            chart: {
                backgroundColor: '#d3d3d3',
                type: 'bar'
            },
            title: {
                text: 'Tweets/Dia'
            },
            xAxis: {
                categories: <?php echo json_encode($fechas); ?>
            },
            yAxis: {
                title: {
                    text: 'N° Tweets'
                }
            },
            series: [{
                name: 'Cantidad Tweets',
                data: <?php echo json_encode($cantidad); ?>
            }]
        });
    });
</script>
