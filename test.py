from src.looker import DealType, Looker, PropertyType


look = Looker('poznan', DealType.BUY, PropertyType.MIESZKANIE, 1)
look.search()
look.save_csv('poz.csv')