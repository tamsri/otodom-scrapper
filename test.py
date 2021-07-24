from src.looker import DealType, Looker, PropertyType


look = Looker('wroclaw', DealType.BUY, PropertyType.MIESZKANIE, 7000)
look.search()
look.save_csv()