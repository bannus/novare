<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
    <title>Novare Res</title>
    
    <link href="bootstrap/css/bootstrap.css" type="text/css" media="screen" rel="stylesheet" />
    <link href="style/style.css" type="text/css" media="screen" rel="stylesheet" />
</head>
<body>
<div class="wrapper">
    <div class="content">
        <div class="padding">
            <h1>Novare Res</h1>
            <h2>Beers on Tap</h2>
            <ul>
                <?
                $request_url = "http://cloud.cs50.net/~kloot/novare/source.xml";
                $beers = simplexml_load_file($request_url) or die("couldn't find xml document");

                foreach ($beers->beer as $beer) {
                    echo "<li>";
                    echo "<a href=\"http://beeradvocate.com/search?q=$beer\">";
                    echo $beer;
                    $url = "http://api.brewerydb.com/v2/";
                    $data = "search?q=$beer&type=beer&key=3e87654b8c90922e6fe4aaefa3e45a89";
                    $ch = curl_init($url);
                    curl_setopt($ch, CURLOPT_POST ,1);
                    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
                    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1); /* obey redirects */
                    curl_setopt($ch, CURLOPT_HEADER, 0);  /* No HTTP headers */
                    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);  /* return the data */
                    $result = curl_exec($ch);

                    curl_close($ch);
                    echo "</a>";
                    echo "<br/>", PHP_EOL;
                }
                ?>
            </ul>
            Last updated <?= $beers->timestamp ?> EST
        </div>
    </div>
</div>    
</div><!-- / -->
</body>
</html>
