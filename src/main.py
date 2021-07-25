from looker import Looker
from dateutil import parser

def main():
    print("Enter number of search")
    amount = int(input())
    searches = []
    for i in range(amount):
        search_data = {}
        print(f"Search #{i}")
        print("Enter city name ( eg. poznan, wroclaw, katowice)")
        search_data['city'] = input()
        print("Property Type ( eg. dom, mieszkanie, dzialki)")
        search_data['property_type']  = input()
        print("Deal type ( eg. sprzedaz, wynajem)")
        search_data['deal_type']  = input()
        print("Amount of property (eg. 10, 20, 30, -1 [for all]) ")
        search_data['search_amount'] = int(input())
        print("Post After (eg. 2021-07)")
        search_data['after'] = parser.parse(input())
        print("Post berfore (eg. 2021-08)")
        search_data['before'] = parser.parse(input())
        print("Name file (eg. poznan-july.csv)")
        search_data['file_name'] = input()
        searches.append(search_data)
    
    print("Press any to start scrapping 😃")
    for search in searches:
        city = search['city']
        dealType = search['deal_type']
        propertyType = search['property_type']
        postAfter = search['after']
        postBefore = search['before']
        maxSearch = search['search_amount']
        
        current_looker = Looker(city, dealType, propertyType,
                                postAfter, postBefore, maxSearch)
        
        current_looker.search()

        file_name = search['file_name']
        current_looker.save_csv(file_name)
    
if __name__ == "__main__":
    main()