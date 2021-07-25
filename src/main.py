from looker import Looker

def main():
    print("Enter number of search")
    amount = int(input())
    searches = []
    for i in range(amount):
        search_data = {}
        print(f"Search #{i}")
        print("Enter city name (poznan, wroclaw, katowice)")
        search_data['city'] = input()
        print("Property Type ( 1 - dom, 2 - mieszkanie, 3 - dzialki)")
        search_data['property_type']  = int(input())
        print("Deal type ( 1 - na sprzedaz, 2 - na wynajem)")
        search_data['deal_type']  = int(input())
        print("Amount of property (10, 20, 30, -1 [for all]) ")
        search_data['search_amount'] = int(input())
        searches.append(search_data)
        print("Post After (eg. 2021-07)")
        postAfter = input()
        print("Post berfore (eg. 2021-08")
        postBefore = input()

    print("Press any to start scrapping 😃")
    for search in searches:
        current_looker = Looker()
        current_looker.search()
        print("Name file (eg. poznan-today)")
        file_name = input()
        current_looker.save_csv(file_name)
    
if __name__ == "__main__":
    main()