Novare Res Beer List
================

Pulls beer list from the Novare Res [draughts page](http://novareresbiercafe.com/draught.php), pulls info using [Brewery DB](http://brewerydb.com) API, and links to [Beer Advocate](http://beeradvocate.com).

# Usage

To run with all features:

    ./novare.py > source.json

Use the -n flag to skip the Brewery DB API calls (for debugging):

    ./novare.py -n > source.json
