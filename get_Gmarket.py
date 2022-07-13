from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pymysql
import time
import re

#  검색어 입력 및 결과 화면 출력
search_txt = input('Gmarket 검색 키워드: ')

#  chromedriver 설정, 4.0부터는 아래와 같이 써야 함
service = Service('C:/chrome/chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get("https://browse.gmarket.co.kr/search?keyword=" + search_txt)
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

#  전체 페이지 순회
while item_count <= total_item:
    #  BS4 사용 전 초기화
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #  상품 리스트 파싱
    product_list = soup.select('div.section__module-wrap > div')

    #  현재 페이지에 노출된 상품들의 제품명, 가격, 이미지 링크를 인기 상품 순서로 출력
    for i in product_list:
        if i.find('div', class_='box__information'):
            #  상품명
            name = i.select_one('span.text__item').text
            name = re.sub(r"^\s+|\s+$", "", name)

            #  가격(현재 판매 중인 가격)
            price = i.select_one('div.box__information-major > div.box__item-price > div.box__price-seller > strong').text
            price = re.sub(r"^\s+|\s+$", "", price)

            #  상품 브랜드, 브랜드가 적혀있지 않을 경우에는 판매자 정보
            brand = getattr(i.select_one('span.box__brand > span.text__brand'), 'text', None)
            if brand is None:
                brand = i.select_one('div.box__information_seller > a > span.text__seller').text
            brand = re.sub(r"^\s+|\s+$", "", brand)

            print(item_count)
            print(name, price, brand)
            item_count += 1
        print()

    if item_count > total_item:
        print('크롤링 완료')
        break
    else:
        next_btn = getattr(i.select_one('#section__inner-content-body-container > div:nth-child(3) > div > a.link__page-next'), 'text', None)
        #  페이지 넘기는 작업 수행
        if next_btn is not None:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="section__inner-content-body-container"]/div[3]/div/a[3]'))).send_keys(Keys.ENTER)
            del soup
            print(page)
            time.sleep(3)
        else:
            print("마지막 페이지까지 완료")
            time.sleep(3)
