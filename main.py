from bs4 import BeautifulSoup
from requests_html import HTMLSession
import pandas as pd
"""
The goal of this scraper is to get the following information about the dentists (100k active dentists all over the USA) : Name , Adress , Phone , Website , 
For the first stage, I will use just YellowPages for NewYork city only => 3k doctors
"""

session = HTMLSession()
def main():
    all_data = []
    for page_number in range(1,101):
        def parser(page_number):
            """This function takes the number of the page and parses it => soup"""
            print('page number: ',page_number )
            global soup
            try:
                url = f'https://www.yellowpages.com/search?search_terms=dentists&geo_location_terms=USA%2CNY&page={page_number}'
                resp = session.get(url)
                page = resp.text
                soup = BeautifulSoup(page , 'html.parser')
            except Exception as e :
                print('Error Occured :',e)
            finally:
                return soup
        def get_data():
            """Takes the soup and gets the needed data"""
            soup = parser(page_number)
            dentists = soup.find_all('div',{'class':'result'})
            data = []
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
                data.append(info)#   __not in here I think. it should be in the other __
            return data # list of dictionnaries
        all_data.extend(get_data())  # It was .append but to avoid getting a  lst of lists I made it .extend     
    return all_data # list of lists of dictionnaries 

result = main()
try :
    data_frame = pd.DataFrame(result)
    data_frame.to_csv('dataframe4.csv',mode='w')
except KeyboardInterrupt as e :
    print(e)
finally:
    data_frame = pd.DataFrame(result)
    data_frame.to_csv('dataframe4.csv',mode='w')
# print(data_frame)
# print(data)
# Why It Does not get highlighted ?
# <a class="track-visit-website" data-analytics='{"click_id":6,"act":2,"dku":"https://www.drmerrickdds.com","FL":"url","target":"website",
# "LOC":"https://www.drmerrickdds.com","adclick":true,"iid":"cfe2c449-0c0d-48b2-bfd0-0dde20f58b60"}' 
# href="https://www.drmerrickdds.com" rel="nofollow noopener" target="_blank">Website</a>