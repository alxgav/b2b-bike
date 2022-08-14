from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from time import sleep
from time import time
from datetime import datetime

from browser import browser
from loguru import logger


import config
import os
import glob
import re
import math
import json



start_time = time()

'''add logging'''
logger.add(f'{config.path}/log/error.log', 
           format= '{time} {level} {message}', 
           level='DEBUG', 
           serialize=False, 
           rotation='1 month', 
           compression='zip')

logger.info(f'Start parsing {datetime.today()}')

'''preparing app'''

if not os.path.exists(os.path.abspath("download")):
    os.makedirs(os.path.abspath("download"))


'''Setup selenium for Chrome'''
browser = browser()
browser.implicitly_wait(10)
browser.get(f'{config.PAGE}ACX/')
browser.maximize_window()


def find_data(data: list) -> bool:
    for i in [i.replace('\n', '').replace('"', '').replace(',', '') for i in open (f'{config.path}/{config.IDS}', 'r').readlines()]:
        if i[0:len(i)] in data:
            return True


'''Login this page'''
def login(user, password) -> None:
    username = browser.find_element(by=By.XPATH, value='//*[@id="loginForm:user"]') 
    username.clear()
    username.send_keys(user)
    passw = browser.find_element(by=By.XPATH, value='//*[@id="loginForm:passwd"]')
    passw.clear()
    passw.send_keys(password)
    passw.send_keys(Keys.ENTER)
    # sleep(5)
    logger.info('Logged')

'''get cookie '''
def get_session() -> str:
    session_id = ''
    for cook in browser.get_cookies():
        for key, values in cook.items():
            if values == 'JSESSIONID':
                session_id = cook["value"]
    return  session_id         


'''get data from page. 
   - Download excel file,
  '''

def download(url: str) -> None:
    browser.get(url)
    files = glob.glob(f'{config.path}/download/*.*')
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            logger.error("Error: %s : %s" % (f, e.strerror))
    try:
       browser.find_element(By.XPATH, value='/html/body/bianchi-customer/acx-base/div/div/div/div[2]/div[2]/om-content/div/div[2]/page-loader/div/sdk-frame-section/sdk-frame-section[2]/sdk-frame-section/div/ordv-order-list-grid/div/div[1]/div[1]/div[1]').click()
       sleep(5)
       browser.find_element(By.XPATH, value='/html/body/bianchi-customer/acx-base/div/div/div/div[2]/div[2]/om-content/div/div[2]/page-loader/div/sdk-frame-section/sdk-frame-section[3]/sdk-frame-section/div/ordv-order-list-button-list2/div/div/sdk-button-panel/div[2]/sdk-button/button').click()
       sleep(10)
       logger.info('File downloaded')
    except:
        logger.error("Can't download file")

'''This function  can use only with get_product()'''
def get_link(element, id: str) -> str:
    try:
        browser.execute_script("arguments[0].click();", element.find_element(By.XPATH, value=f'//*[@id="{id}"]/sdk-collection-item-ld/div/div[1]/div/div/div[2]/div[2]/sdk-item-attribute/sdk-single-action-attribute/sdk-button/button'))
        sleep(3)
        browser.switch_to.window(browser.window_handles[1])
        link = browser.current_url
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
    except:
        link =''
        browser.execute_script("arguments[0].click();", element.find_element(By.XPATH, value='//*[@id="toast-container"]/div[1]'))
    finally:
        return link

'''This function work very long, but it function exyract url of product.
In requests method like data_bake() after response can get data in json format without url to product
'''
def get_product(url: str) -> dict:
    browser.get(url)
    sleep(5)
    browser.execute_script("arguments[0].click();", browser.find_element(by=By.XPATH, value='/html/body/bianchi-customer/acx-base/div/div/div/div[2]/div[2]/om-content/div/div[2]/page-loader/div/sdk-frame-section/sdk-frame-section[1]/sdk-frame-section[1]/div/ordv-order-list-button-list1/div/div/div[1]/sdk-button/button'))
    sleep(5)
    browser.execute_script("arguments[0].click();", browser.find_element(by=By.XPATH, value='/html/body/sdk-modal-panel/mz-modal/div/div[1]/div/mz-modal-content/reorders-choice/div/div/div[1]/img'))
    sleep(5)
    data = []


    totals = math.ceil(int(re.sub('\D', '', browser.find_element(By.XPATH, value='/html/body/bianchi-customer/acx-base/div/div/div/div[2]/div[2]/om-content/div/div[2]/page-loader/div/sdk-frame-section/sdk-frame-section[1]/sdk-frame-section[2]/div/ordv-order-product-search-grid/div/div[1]/div[2]/div').text ))/40)
    for page in range(1, totals+1):
        for element in browser.find_elements(By.CLASS_NAME, value='item-col-ld'):
            id = element.get_attribute('id').strip()

            if id not in data:
                if find_data(id):
                    try:
                        PRODUCT = element.find_element(by=By.XPATH, value=f'//*[@id="{id}"]/sdk-collection-item-ld/div/div[1]/div/div/div[2]/div[5]/sdk-item-attribute/sdk-data-attribute/div/div/div/div[3]/p').text 
                    except:
                        PRODUCT = ''
                    try:
                        PRICE = element.find_element(by=By.XPATH, value=f'//*[@id="{id}"]/sdk-collection-item-ld/div/div[1]/div/div/div[2]/div[6]/sdk-item-attribute/sdk-data-attribute/div/div/div/div[3]/p').text 
                    except:
                        PRICE = ''
                    data.append({'CODE': id,
                                 'PRODUCT':PRODUCT,
                                 'PRICE':PRICE,
                                 'LINK': get_link(element, id),
                                 })
            
        next_page()
    logger.info(len(data))
    logger.info(data)



def get_acsessories():
    pass

'''if use data_bike() this function not need'''
def next_page() -> None:
    try:
        browser.execute_script("arguments[0].click();", browser.find_element(By.XPATH, value='//*[@id="nextPage"]'))
        sleep(5)
    except:
        logger.error('next page not working')

'''get data from bike shop'''
def data_bike(url_page: str) -> dict:
    browser.get(url_page)
    sleep(5)
    browser.execute_script("arguments[0].click();", browser.find_element(by=By.XPATH, value='/html/body/bianchi-customer/acx-base/div/div/div/div[2]/div[2]/om-content/div/div[2]/page-loader/div/sdk-frame-section/sdk-frame-section[1]/sdk-frame-section[1]/div/ordv-order-list-button-list1/div/div/div[1]/sdk-button/button'))
    sleep(5)
    browser.execute_script("arguments[0].click();", browser.find_element(by=By.XPATH, value='/html/body/sdk-modal-panel/mz-modal/div/div[1]/div/mz-modal-content/reorders-choice/div/div/div[1]/img'))
    sleep(5)
    data_bike = []
    for request in browser.requests:
        if request.response:
            if request.response.headers['Content-Type'] == 'application/json':
                if 'add-products/products' in request.url:
                    data = json.loads(request.response.body)
                    for item in data['data']['result']:
                        id = item['productCode']
                        if find_data(id):
                            data_bike.append({'CODE': id,
                                    'PRODUCT':item["productDescription"],
                                    'PRICE':item["price"]
                                    })
                    
                    return data_bike
    return None


def get_data_details(data: list): 
    for code in data:
        code = code['CODE']
        search_input = browser.find_element(By.XPATH, value='/html/body/bianchi-customer/acx-base/div/div/div/div[2]/div[2]/om-content/div/div[2]/page-loader/div/sdk-frame-section/sdk-frame-section[1]/sdk-frame-section[2]/div/ordv-order-product-search-grid/div/div[1]/div[4]/div[1]/mz-input-container/div/input')
        search_input.clear()
        search_input.send_keys(code)
        browser.execute_script("arguments[0].click();", browser.find_element(By.XPATH, value='/html/body/bianchi-customer/acx-base/div/div/div/div[2]/div[2]/om-content/div/div[2]/page-loader/div/sdk-frame-section/sdk-frame-section[1]/sdk-frame-section[2]/div/ordv-order-product-search-grid/div/div[1]/div[4]/div[3]/sdk-button/button/i'))
        sleep(5)
        browser.find_element(By.XPATH, value=f'//*[@id="{code}"]/sdk-collection-item-ld/div/div[1]/div/div/div[1]/i').click()
        browser.execute_script("arguments[0].click();", browser.find_element(By.XPATH, value='/html/body/bianchi-customer/acx-base/div/div/div/div[2]/div[2]/om-content/div/div[2]/page-loader/div/sdk-frame-section/sdk-frame-section[1]/sdk-frame-section[2]/div/ordv-order-product-search-grid/div/div[1]/div[3]/sdk-button[4]/button'))
        sleep(5)
        for request in browser.requests:
            if request.response:
                if request.response.headers['Content-Type'] == 'application/json':
                    if f'/add-products/{code}/grid' in request.url:
                        data = json.loads(request.response.body)
                        
        break



@logger.catch
def main():
    login(config.USER_NAME, config.USER_PASSWORD)
    session_id = get_session()
    url_page = f'{config.PAGE}ACX/fweba2/page/order-list?httpSessionId={session_id}&host=10.98.0.52&context_path=ACX'
    logger.info(session_id)
    # download(url_page)
    data = data_bike(url_page)
    get_data_details(data)
    logger.info(f'length of data {len(data)}')
    browser.close()
    browser.quit()
    


if __name__ == '__main__':
    main()
    logger.info("--- %s seconds ---" % (time() - start_time))
    logger.info(f'End parsing {datetime.today()}')
    

