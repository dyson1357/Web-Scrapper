from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
import re


#  다나와 메인 페이지 오픈
#  chromedriver 설정, 4.0부터는 아래와 같이 써야 함
service = Service('C:/chrome/chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get("https://www.ebay.com/")
time.sleep(2)

#  검색어 입력
search_txt = input('ebay 검색 키워드: ')
driver.find_element(By.ID, "gh-ac").click()
element = driver.find_element(By.ID, "gh-ac")
element.send_keys(search_txt)

#  검색 버튼 눌러 검색 수행
driver.find_element(By.ID, "gh-btn").send_keys(Keys.ENTER)

'''
이 밑은 뜯어 고치는 중
'''

curPage = 1
print_page = 0
dec_page = 1
pList = []

#  전체 페이지 순회

#  BS4 사용 전 초기화
soup = BeautifulSoup(driver.page_source, 'html.parser')
#  상품 리스트 파싱
product_list = soup.select('div.main_prodlist.main_prodlist_list > ul > li')

#  현재 페이지에 노출된 상품들의 제품명, 가격, 이미지 링크를 인기 상품 순서로 출력
for i in product_list:
    if i.find('div', class_='prod_main_info'):
        #  상품명
        name = i.select_one('p.prod_name > a').text.strip()

        #  다양한 가격 id 및 위치들 처리, 해당 주소에 이미지 없으면 None 처리 하고 뒤에 다른 형식에 위치 했는지 파악해 찾아감
        price = getattr(i.select_one('p.price_sect > a'), 'text', None)
        if price == None:
            price = getattr(i.select_one('p.price_sect'), 'text', None)
        if price == None:
            price = i.select_one('div.top5_price').text.strip()
        img_link = i.select_one('div.thumb_image > a > img').get('data-original')
        if img_link == None:
            img_link = i.select_one('div.thumb_image > a > img').get('src')

        #  광고 데이터 거르는 작업 - 이미지 src가 다음과 같으면 광고 데이터임을 확인
        if img_link != '//img.danawa.com/new/noData/img/noImg_160.gif':
            pList.append([name, price, img_link])
            print(name, price, img_link)
    print()
curPage += 1
dec_page += 1

#  크롤링 완료 되면 완료 메시지 출력
if curPage > total_page:
    print('크롤링 완료')
    break
else:
    #  페이지 넘기는 작업 수행
    #  nth-child(N) -> 부모 안에 모든 요소 중 N번째 요소 https://lalacode.tistory.com/6 참고
    cur_css = 'div.paging_number_wrap > a:nth-child({})'.format(dec_page)

    #  10페이지 단위로 옆으로 넘기는 버튼 클릭 수행
    if (dec_page - 1) % 10 == 0:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'paging_edge_nav.paging_nav_next.click_log_page'))).send_keys(Keys.ENTER)
        del soup
        dec_page = 1
        print_page += 10
        time.sleep(3)


    #  긁어올 현재 페이지 number 출력
    print(curPage)


#  크롤링 결과를 '검색어.csv' 파일로 저장
def saveToFile(filename, list):
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(list)
    print(search_txt + '.csv 파일 저장 완료')


saveToFile(search_txt + '.csv', pList)

#  이거 없으면 타임아웃 에러 나던데,,
driver.quit()
