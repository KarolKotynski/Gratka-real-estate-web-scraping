import time
import os
from find_page import PageSearch, ContentSearch

"""
purpose of this script is to list annoucements of real estate in Gdansk city
and save it in csv file
inputs are url page, number of page, name of div which contain
all annoucements and name of listed annoucements - articles
e.g.
url_page = "https://gratka.pl/nieruchomosci/mieszkania/gdansk/sprzedaz?page="
number_page = 1
container = 'content__listing'
list_search = 'article'
result is CSV file named "gratka<current_date>.csv"
"""


current_date = time.strftime('%m_%m_%Y')

location = os.path.dirname(__file__)
# create "results" folder in current path
path_file = f"{location}/results"
if not os.path.exists(path_file):
    os.makedirs(path_file)

# creating CSV file in current path with current date
csv_name = f"{location}/results/gratka{current_date}.csv"
f = open(csv_name, 'w+')

f.write("name;location;price;price/mkw;info;site\n")

# url  and its number of page
url_page = "https://gratka.pl/nieruchomosci/mieszkania/gdansk/sprzedaz?page="
number_page = 0

# name of looking div and name of listed articles 
container = 'content__listing'
list_search = 'article'

while True:
    # get content of current page
    print(number_page)
    page_soup = PageSearch(url_page, number_page).get_page()
    articles = ContentSearch(container, list_search).get_object_list()

    # loop for each article
    for article in articles:
        global_info = article.find('div', {'class':'teaserEstate__infoBox'})
        if global_info == None:
            continue

        name = global_info.div.h2.a.text.replace('²', '2').replace('с', 'c').strip()
        
        site = global_info.div.h2.a.get('href') 
        
        location = global_info.div.span.text.strip().replace(' ', '').strip()
        
        additional_info = global_info.div.ul.text.strip().split('\n')
        merged_additional_info = ''
        # loop to merge additional info
        for info in additional_info:
            merged_additional_info += info + ' '

        price = global_info.find('div', {'class':'teaserEstate__priceBox'}).p.text.strip().split('\n')
        
        # try to write to CSV file with exception if price[2] is None
        try:
            f.write(name + ';' 
                    + location + ';' 
                    + price[0] + ';' 
                    + price[2].strip() + ';' 
                    + merged_additional_info + ';' 
                    + site + '\n')
        except:
            f.write(name + ';' 
                    + location + ';' 
                    + price[0] + ';' 
                    + "NONE" + ';' 
                    + merged_additional_info + ';' 
                    + site + '\n')

    number_page += 1

f.close()
