from bs4 import BeautifulSoup
import requests 
import pandas as pd 
from selenium import webdriver 
from tqdm.notebook import tqdm # for progress bars
from selenium.common import exceptions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os 
BASE_URL = "https://trustpilot.com"

def get_soup(url):
    '''Function to fetch data from given url and parse it using lxml parser'''
    return BeautifulSoup(requests.get(url).content,'lxml')

data = {}
def get_categories_and_subs():
    soup = get_soup(BASE_URL + '/categories')
    for category in soup.findAll('div',{'class':'paper_paper__29o4A paper_square__XVMAC card_card__2F_07 card_noPadding__1tkWv styles_card__1CdW1'}):
        name = category.find('h2',{'class':'typography_typography__23IQz typography_body__2OHdw typography_weight-medium__34H_5 typography_fontstyle-normal__1_HQI styles_headingDisplayName__1pvgX'}).text.strip()
        data[name] =  {}
        sub_categories = category.find('ul',{"class":'card_cardContent__3Idve styles_linkList__2dU7d'})
        for sub in sub_categories.findAll('li'):
            sub_cat_name = sub.find('a').text.strip()
            sub_cat_uri = sub.find('a')['href']
            data[name][sub_cat_name] = sub_cat_uri
    return data 

def get_company_urls(driver):
    comp_list = driver.find_elements(by=By.NAME,value='business-unit-card')
    # print(comp_list)
    urls = [a.get_attribute('href') for a in comp_list]
    urls = list(set(urls))
    print(urls)
    return urls 

def go_next_page(driver):
    try:
        next_page_but = driver.find_element_by_xpath('//a[@class="button_button_3sN8k"]')
        return True,next_page_but 
    except exceptions.NoSuchElementException:
        return False,None 

def initialize_selenium():
    options = Options()
    # Headless browser ,operates as a typical browser but without a UI 
    # Good for automated testing and improved speed
    options.add_argument('--headless')
    # maximizes browser window to view all elements    
    options.add_argument('start-maximized')
    # disbale information bars
    options.add_argument('disable-infobars')
    #disable extensions
    options.add_argument('--disable-extensions')
    # prefs = {"profle.managed_defaulr_content_settings.images":2}
    # options.add_experimental_option("prefs",prefs)

    driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver',options=options)
    timeout= 5
    return driver,timeout

def get_data():
    data = get_categories_and_subs()
    driver,timeout = initialize_selenium()
    company_urls = {}
    string_end = "?numberofreviews=0&timeperiod=0&status=all"
    for category in tqdm(data):
        for sub in tqdm(data[category],leave=False):
            company_urls[sub] = []
            url = BASE_URL + data[category][sub]+string_end
            print(url)
            driver.get(url)
            try:
                is_element_present = expected_conditions.presence_of_element_located((By.CLASS_NAME,'link_internal__YpiJI'))
                WebDriverWait(driver,timeout).until(is_element_present)
            except:
                pass
            next_page = True 
            i = 1
            while next_page:
                extracted_company_urls = get_company_urls(driver)
                company_urls[sub]+=extracted_company_urls
                next_page,_ = go_next_page(driver)

                if next_page:
                    i+=1
                    next_url = url + f'&page={i}'
                    driver.get(next_url)
                    try: 
                        is_element_present = expected_conditions.presence_of_element_located((By.CLASS_NAME,'link_internal__YpiJI'))
                        WebDriverWait(driver,timeout).until(is_element_present)
                    except:
                        pass 
    final_data = []
    for category in data:
        for sub in data[category]:
            for url in company_urls[sub]:
                final_data.append((category,sub,url))
    df = pd.DataFrame(final_data,columns=['category','sub_category','urls'])
    if not os.path.exists('data'):
        os.makedirs('data')
    df.to_csv('data/company_urls.csv',index=False)


if __name__ == '__main__':
    get_data()