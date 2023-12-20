from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import requests
session = HTMLSession()
url =  'https://www.yellowpages.com/search?search_terms=dentists&geo_location_terms=USA%2CNY'
resp = requests.get(url)
page = resp.text
soup = BeautifulSoup(page , 'lxml')

def get_data(soup):
    dentists = soup.find_all('div',{'class':'result'})
    data = [] # 
    for dentist in dentists:
        name = dentist.find('a',class_='business-name').text
        phone = dentist.find(class_ = 'phones phone primary').text
        adress = dentist.find('div',{'class':'adr'}).contents[0].text +' '+ dentist.find('div',{'class':'adr'}).contents[1].text
        website_element = dentist.find('a',{'class' : 'track-visit-website'})
        website = website_element.get('href')  if website_element else 'No Website'
        info = {
            'Name' : name,
            'Phone' : phone , 
            'Adress' : adress , 
            'Website' : website
            }
        data.append(info)
    return data # list of dictionnaries

data = get_data(soup)
# Make a data frame
data_frame = pd.DataFrame(data)
# Convert it to csv
data_frame.to_csv('dataframe11.csv',mode='w')