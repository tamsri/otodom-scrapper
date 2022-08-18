# OTODOM Scrapper
Otodom scrapper read otodom.pl and turn the property listing to a spreadsheet

## Example
```Python
from src.looker import Looker
from dateutil import parser

scrapper = Looker('poznan', 'sprzedaz', 'mieszkanie',
                  parser.parse('2021-07'), parser.parse('2021-08') ,100)
scrapper.search()
scrapper.save_csv('poznan-july.csv')
```
