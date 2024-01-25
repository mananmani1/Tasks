from bs4 import BeautifulSoup
import requests
import pandas as pd

def scrape_and_get_data():
    # Fetch HTML content
    html_text = requests.get('https://www.worldometers.info/world-population/population-by-country/').text
    
    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html_text, 'lxml')
    
    # Extract data from HTML
    countries = soup.find_all('tr')[1::]
    # data = {'Country': [], 'median_age': [], 'urban_population': [], 'fertility_rate': []}
    data = {'country_li': [], 'population_li': [], 'yearly_growth_li': [], 'land_area_li': []}

    for i in countries:
        #iterating over the tags
        country = i.find('a').text
        population = i.find_all('td')[2].text
        yearly_growth = i.find_all('td')[3].text
        land_area = i.find_all('td')[6].text

        #appending 
        data['country_li'].append(country)
        data['population_li'].append(population)
        data['yearly_growth_li'].append(yearly_growth)
        data['land_area_li'].append(land_area)

    
    # Creating a DataFrame from the dictionary
    df = pd.DataFrame(data)

    
    return df


