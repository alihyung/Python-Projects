from bs4 import BeautifulSoup
import requests

url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'

page = requests.get(url)

# getting page in html:
soup = BeautifulSoup(page.text, 'html')

print(soup)


# finding tables that we want:
#soup.find('table', class_ = "wikitable sortable")
# <table class="wikitable sortable jquery-tablesorter">
#soup.find_all('table')[0]

# picking the first table:
table = soup.find_all('table')[0]

# finding all headers in table:
world_titles = table.find_all('th')

# getting text, cleaning, and placing in the list:
world_table_titles = [title.text.strip() for title in world_titles]

import pandas as pd

# creating data frame and assigning column names:
df = pd.DataFrame(columns = world_table_titles)

# finding all row values from the table:
column_data = table.find_all('tr')


for row in column_data[1:]:
    row_data = row.find_all('td') # find all individual values
    individual_row_data = [data.text.strip() for data in row_data]  # getting text, cleaning, and putting in a list
    #print(individual_row_data)
    length = len(df) # length of data frame
    df.loc[length] = individual_row_data # appending every list to the data frame's index
    
# saving as csv file with no index colummn
df.to_csv(r'C:\Users\alisa\Documents\Python\Companies.csv', index = False)
    
