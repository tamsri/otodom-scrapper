from src.looker import Looker
from dateutil import parser
from datetime import datetime

before =  parser.parse('2021-06')
after = parser.parse('2021-07')
now = datetime.now()

if before < now and after > now:
    print("yes")
else:
    print("noo")


# look = Looker('poznan', 'sprzedaz', 'mieszkanie',
#                  parser.parse('2021-07'), parser.parse('2021-08') ,100)
# look.search()
# look.save_csv('poz.csv')