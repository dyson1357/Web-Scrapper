from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import timedelta
import csv
import time
import re

from selenium.webdriver.support.wait import WebDriverWait

options = webdriver.ChromeOptions()
options.add_argument("headless")

#  검색어 입력
search_txt = input('ebay 검색 키워드: ')
num_of_req = int(input('가져올 상품 데이터 수: '))

#  시작 시간
start = time.time()

#  chromedriver 설정, 4.0부터는 아래와 같이 써야 함
service = Service('C:/chrome/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

#  즉시 구매 옵션과 새 상품인 옵션을 만족하는 검색 결과창
driver.get(
    "https://www.ebay.com/sch/i.html?_nkw=" + search_txt + "&_sacat=0&LH_BIN=1&rt=nc&LH_ItemCondition=1000&_ipg=240")
driver.implicitly_wait(10)

item_count = 1
page = 1
pList = []
link_list = []
num = 1

#  전체 페이지 순회
while len(link_list) <= num_of_req + 1:
    links = []
    #  상품 상세 페이지 링크 수집
    links = driver.find_elements(By.CLASS_NAME, 's-item__link')

    for i in links:
        num += 1
        link_list.append(i.get_attribute('href'))
        link_list = list(dict.fromkeys(link_list))

        item_count += 1
        if len(link_list) == num_of_req + 1:
            break

        if (item_count % 240) == 0:
            next_btn = driver.find_element(By.CLASS_NAME, 'pagination__next.icon-link')
            #  페이지 넘기는 작업 수행
            if next_btn is None:
                print("마지막 페이지까지 완료")
            else:
                page += 1
                driver.find_element(By.CLASS_NAME, "pagination__next.icon-link").send_keys(Keys.ENTER)
                driver.implicitly_wait(10)
                break
    if len(link_list) == num_of_req + 1:
        break

del link_list[0]
prod_count = 1
print(len(link_list))

soup = BeautifulSoup(driver.page_source, 'html.parser')
for product in link_list:
    driver.get(product)
    #  time.sleep(5)
    driver.implicitly_wait(30)

    #  상품명
    try:
        name = driver.find_element(By.ID, 'vi-lkhdr-itmTitl').get_attribute('textContent')
        name = re.sub(r"^\s+|\s+$", "", name)
    except Exception as e:
        name = "로딩 불가"

    #  가격(현재 판매 중인 가격)
    try:
        price = driver.find_element(By.CLASS_NAME, 'notranslate').text
        price = re.sub(r"^\s+|\s+$", "", price)
    except Exception as e:
        name = "로딩 불가"

    catch_f = 1
    catch_s = 1

    try:
        specific = soup.select('#viTabs_0_is > div > div.ux-layout-section.ux-layout-section--features > div > div')
        for find_first in specific:
            find_first.select('div')
            for find_second in find_first:
                get_search = soup.select('#viTabs_0_is > div > div.ux-layout-section.ux-layout-section--features > div > div:nth-child('+ str(catch_f) +') > div:nth-child(' + str(catch_s) + ') > div').text
                if get_search == "Brand:":
                    brand = soup.select('#viTabs_0_is > div > div.ux-layout-section.ux-layout-section--features > div > div:nth-child('+ str(catch_f) +') > div:nth-child(' + str(catch_s+1) + ') > div').get_attribute('textContent')
                    catch_f += 1
                    catch_s += 1
    except Exception as e:
        brand = "정보 없음"

    driver.implicitly_wait(10)
    brand = re.sub(r"^\s+|\s+$", "", brand)

    pList.append([name, price, brand])
    print(str(prod_count) + " | 상품명: " + name + " / 가격: " + price + " / 브랜드: " + brand)
    prod_count += 1


#  크롤링 결과를 '검색어.csv' 파일로 저장
def saveToFile(filename, list):
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(list)
    print(search_txt + '.csv 파일 저장 완료')

saveToFile(search_txt + '.csv', pList)

driver.quit()

end = time.time()

print("총 소요 시간(hh:mm:ss): ", timedelta(seconds=end - start))
