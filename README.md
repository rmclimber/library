## HBScraper
Simple class to create a CSV of your Humble Bundle library. Parses the HTML
of the page and generates a two-column CSV (`Title, Publisher`).

Current dependencies: written and tested in base Python 3.11.7. As far as I know
the newest thing it actually needs is the [pattern matching](https://peps.python.org/pep-0636/) 
(match statements) introduced in Python 3.10. Works with the Humble Bundle
Library's HTML as of 20240124.

### Usage
#### Getting the HTML
To use, go to your Humble Bundle library 
[here](https://www.humblebundle.com/home/library). Using Chrome, right-click on 
the top item on the list and choose `Inspect`. Move back up the `div` hierarchy
till you find the class named `scrollbar-hider`. Right-click and choose
`Edit as HTML`. Select all, paste it into a text editor, and save it. 

#### Running the script
Assuming your Python version is 3.10+ and you saved the library HTML to 
`foo.html`, you should be able to run 
    python hb_parser.py foo.html
from a bash terminal. If you'd like to save the result to a specific file
named `bar.csv`, do:
    python hb_parser.py foo.html bar.csv
By default, the script will save to `output.csv` in the current working
directory. It also overwrites anything currently there. 