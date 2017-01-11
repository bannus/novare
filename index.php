<?php
function printList($beers)
{
    $i = 0;
    foreach ($beers as $beer) 
    {
        echo "<div class=\"accordion-group\">";
        echo "<div class=\"accordion-heading\">", PHP_EOL;
        echo "<div class=\"accordion-toggle\">", PHP_EOL;
        echo "<a href=\"http://beeradvocate.com/search?q={$beer['novareName']}\">";
        echo $beer['novareName'];
        echo "</a>";
        if (isset($beer['style']))
        {
            echo " - {$beer['style']['name']}";
        }
        if (isset($beer['abv']))
        {
            echo " - {$beer['abv']}%";
        }
        if (isset($beer['description']))
        {
            echo " - ";
            echo "<a data-toggle=\"collapse\" data-parent=\"#accordion2\" href=\"#collapse$i\">";
            echo "Description";
            echo "</a>";
            echo "</div>", PHP_EOL;
            echo "</div>", PHP_EOL;
            echo "<div id=\"collapse$i\" class=\"accordion-body collapse\">";
            echo "<div class=\"accordion-inner\">";
            echo "{$beer['description']}";
            echo "</div>", PHP_EOL;
            echo "</div>", PHP_EOL;
        }
        else
        {
            echo "</div>", PHP_EOL;
            echo "</div>", PHP_EOL;
        }
        echo "</div>", PHP_EOL;
        $i++;
    }
}

function printTable($beers)
{
    echo "<table class=\"table\">", PHP_EOL;
    echo "<thead>", PHP_EOL;
    echo "<tr>", PHP_EOL;
    echo "<th></th>", PHP_EOL;
    echo "<th>Beer</th>", PHP_EOL;
    echo "<th>Style</th>", PHP_EOL;
    echo "<th>ABV</th>", PHP_EOL;
    echo "<th>IBU</th>", PHP_EOL;
    echo "</tr>", PHP_EOL;
    echo "</thead>", PHP_EOL;

    $i = 0;
    foreach ($beers as $beer) 
    {
        echo "<tr>", PHP_EOL;
        echo "<td></td>", PHP_EOL;
        echo "<td><a href=\"http://google.com/#safe=off&q=site:ratebeer.com {$beer['novareName']}\">";
        echo $beer['novareName'];
        echo "</a></td>";

        if (isset($beer['style']))
        {
            echo "<td>{$beer['style']['shortName']}</td>";
        }
        else
        {
            echo "<td></td>", PHP_EOL;
        }
        if (isset($beer['abv']))
        {
            echo "<td>{$beer['abv']}%</td>";
        }
        else
        {
            echo "<td></td>", PHP_EOL;
        }
        if (isset($beer['ibu']))
        {
            echo "<td>{$beer['ibu']}</td>";
        }
        else
        {
            echo "<td></td>", PHP_EOL;
        }
        //if (isset($beer['description']))
        //{
            //echo " - ";
            //echo "<a data-toggle=\"collapse\" data-parent=\"#accordion2\" href=\"#collapse$i\">";
            //echo "Description";
            //echo "</a>";
            //echo "</div>", PHP_EOL;
            //echo "</div>", PHP_EOL;
            //echo "<div id=\"collapse$i\" class=\"accordion-body collapse\">";
            //echo "<div class=\"accordion-inner\">";
            //echo "{$beer['description']}";
            //echo "</div>", PHP_EOL;
            //echo "</div>", PHP_EOL;
        //}
        //else
        //{
            //echo "</div>", PHP_EOL;
            //echo "</div>", PHP_EOL;
        //}
        $i++;
    }
    echo "</table>", PHP_EOL;
}
php?>

<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
<title>Novare Res</title>

<link href="bootstrap/css/bootstrap.css" type="text/css" media="screen" rel="stylesheet" />
<link href="bootstrap/css/bootstrap-responsive.css" type="text/css" media="screen" rel="stylesheet" />
<link href="style/style.css" type="text/css" media="screen" rel="stylesheet" />
</head>
<body>
<div class="wrapper">
    <div class="content">

        <div class="padding">
            <h1>Novare Res</h1>
            <?php
                $file = "source.json";
                $json = json_decode(file_get_contents($file), true);
                foreach($json['lists'] as $name=>$list)
                {
                    print "<h3>$name</h3>";
                    printTable($list);
                }
            php?>
            Last updated <?= $json['timestamp'] ?> EST
        </div>
    </div>
</div> 
</div><!-- / -->
<script type="text/javascript" src="bootstrap/js/jquery.js"></script>
<script type="text/javascript" src="bootstrap/js/bootstrap.min.js"></script>
</body>
</html>
