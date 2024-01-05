# -*- encoding: utf-8 -*-

import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import json

#Pegar conteúdo
url = "https://www.transfermarkt.com/lionel-messi/leistungsdatendetails/spieler/28003"
rank = {}

rankings = {
    'order': {'field': 'goals', 'label': 'goals'}
}

def buildingRank(type):
    field = rankings[type]['field']
    label = rankings[type]['label']
    element = driver.find_element_by_xpath(
        f"//main//div[@class='row']//div[@class='responsive-table']//table[@data-field='{field}']"
    ).click()
    html_content = element.get_attribute('outerHTML')

    #Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    #Estruturar para DataFrame - Pandas
    df_full = pd.read(str(table))[0].head(10)
    df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', label]]
    df.columns = ['season', 'competition', 'club', 'appearances', 'goals', 'assists']

    #Transformar os dados em uma estrutura de Dicionários
    return df.to_dict('records') 


option = Options()
option.headless = True
service = Service(executable_path='geckodriver', log_path="geckodriver.log")
driver = webdriver.Firefox(options=option, service=service)


for k in rankings:
    rank[k] = buildingRank(k)

driver.quit()

#Formatação e conversão para JSON
with open('ranking.json', 'w', encoding='utf-8') as jp:
    js = json.dumps(rank, indent=4)
    jp.write(js)