from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pymysql
import csv
import time
import re
import math

options = webdriver.ChromeOptions()
options.add_argument("headless")

#  검색어 입력 및 결과 화면 출력
search_txt = input('Gmarket 검색 키워드: ')

#  chromedriver 설정, 4.0부터는 아래와 같이 써야 함
service = Service('C:/chrome/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://browse.gmarket.co.kr/search?keyword=" + search_txt)
driver.implicitly_wait(10)
time.sleep(2)


#  판매 인기순 정렬
driver.find_element(By.XPATH,
                    '//*[@id="region__content-status-information"]/div/div/div[2]/div[1]/div[1]/button').click()
driver.find_element(By.XPATH,
                    '//*[@id="region__content-status-information"]/div/div/div[2]/div[1]/div[2]/ul/li[2]').click()

#  전체 상품 수
total_item = driver.find_element(By.CLASS_NAME, 'text__item-count').text
total_item = int(re.sub(r'\D', '', total_item))
print("*" + search_txt + "*" + " 전체 상품 수: " + str(total_item))

item_count = 1
page = 1
pList = []
link_list = []
total_page = math.ceil(total_item/100)
num = 1

#  전체 페이지 순회
while page <= total_page:
    #  BS4 사용 전 초기화
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #  상품 상세 페이지 링크 수집
    links = driver.find_elements(By.CLASS_NAME, 'link__item')
    for i in links:
        print(num)
        num += 1
        link_list.append(i.get_attribute('href'))
        print(link_list)

    if page == total_page:
        print('크롤링 완료')
        break

    if (item_count % 100) == 0:
        #  다음 페이지로 전환 동작
        if page == total_page:
            print('크롤링 완료')
            break
        else:
            next_btn = driver.find_element(By.CLASS_NAME, 'link__page-next')
            #  페이지 넘기는 작업 수행
            if next_btn is None:
                print("마지막 페이지까지 완료")
            else:
                driver.find_element(By.CLASS_NAME, "link__page-next").send_keys(Keys.ENTER)
                page += 1
                print(str(page) + "페이지")
                time.sleep(3)

    item_count += 1


    '''#  상품 정보 수집
    for item in link_list:
        driver.get(item)
        time.sleep(2)

        #  상품명
        name = driver.find_element(By.CLASS_NAME, 'itemtit').text
        name = re.sub(r"^\s+|\s+$", "", name)

        #  가격(현재 판매 중인 가격)
        price = driver.find_element(By.CLASS_NAME, 'price_real').text
        price = re.sub(r"^\s+|\s+$", "", price)

        #  브랜드 정보 수집
        driver.find_element(By.CSS_SELECTOR,
                            '#vip-tab_detail > div.vip-detailarea_productinfo.box__product-notice.js-toggle-content > '
                            'div.box__product-notice-more > button').send_keys(Keys.ENTER)
        brand = getattr(soup.select( '#vip-tab_detail > div.vip-detailarea_productinfo.box__product-notice.js-toggle-content.on > '
                                     'div.box__product-notice-list > table:nth-child(1) > tbody > tr:nth-child(7) > td'),'text', None)
        if brand is None:
            brand = "정보 없음"
        brand = re.sub(r"^\s+|\s+$", "", brand)

        pList.append([name, price, brand])
        print(item_count)
        pList.append([name, price, brand])
        print("상품명: " + name + " / 가격: " + price + " / 브랜드(판매자): " + brand)

        item_count += 1
        print()'''

#  크롤링 결과를 '검색어.csv' 파일로 저장
def saveToFile(filename, list):
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(list)
    print(search_txt + '.csv 파일 저장 완료')


saveToFile(search_txt + '.csv', pList)

driver.quit()

