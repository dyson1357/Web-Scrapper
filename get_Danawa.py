from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pymysql
import time
import csv
import re

#  다나와 메인 페이지 오픈
#  chromedriver 설정, 4.0부터는 아래와 같이 써야 함
service = Service('C:/chrome/chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get("https://www.danawa.com/")
time.sleep(2)

#  검색어 입력
search_txt = input('다나와 검색 키워드: ')
driver.find_element(By.ID, "AKCSearch").click()
element = driver.find_element(By.ID, "AKCSearch")
element.send_keys(search_txt)

#  검색 버튼 눌러 검색 수행
driver.find_element(By.CLASS_NAME, "search__submit").send_keys(Keys.ENTER)

#  총 페이지 수 도출
page_path = driver.find_element(By.XPATH, '//*[@id="paginationArea"]/div/span')
total_page_text = page_path.text
total_page = int(re.sub(r'\D', '', total_page_text))
print(total_page)

curPage = 1
print_page = 0
dec_page = 1
pList = []

#  DB 연동 및 커서 생성
conn = pymysql.connect(host='127.0.0.1', user='root', password='151106', db='Scraping', charset='utf8')
cur = conn.cursor()

#  DB 테이블 생성용, 테스트 완료 후 삭제할 코드
cur.execute("CREATE TABLE Danawa(name char(50), price char(10), img char(100))")

#  전체 페이지 순회
while curPage <= total_page:
    #  BS4 사용 전 초기화
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #  상품 리스트 파싱
    product_list = soup.select('div.main_prodlist.main_prodlist_list > ul > li')

    #  현재 페이지에 노출된 상품들의 제품명, 가격, 이미지 링크를 인기 상품 순서로 출력
    for i in product_list:
        if i.find('div', class_='prod_main_info'):
            #  상품명
            name = i.select_one('p.prod_name > a').text
            name = re.sub(r"^\s+|\s+$", "", name)

            #  다양한 가격 id 및 위치들 처리, 해당 주소에 이미지 없으면 None 처리 하고 뒤에 다른 형식에 위치 했는지 파악해 찾아감
            price = getattr(i.select_one('p.price_sect > a'), 'text', None)
            if price == None:
                price = getattr(i.select_one('p.price_sect'), 'text', None)
            if price == None:
                price = getattr(i.select_one('div.top5_price'), 'text', None)
            price = re.sub(r"^\s+|\s+$", "", price)
            img_link = i.select_one('div.thumb_image > a > img').get('data-original')
            if img_link == None:
                img_link = i.select_one('div.thumb_image > a > img').get('src')
            img_link = re.sub(r"^\s+|\s+$", "", img_link)

            #  광고 데이터 거르는 작업 - 이미지 src가 다음과 같으면 광고 데이터임을 확인
            if "," in price or img_link != '' \
                                           '':
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
        else:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, cur_css))).send_keys(
                Keys.ENTER)
            del soup
            time.sleep(3)

        #  긁어올 현재 페이지 number 출력
        print(curPage)


#  크롤링 결과를 '검색어.csv' 파일로 저장
def saveToDB(filename, list):
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(list)
    print(search_txt + '.csv 파일 저장 완료')


saveToDB(search_txt + '.csv', pList)

#  이거 없으면 타임 아웃 에러 나던데,,
driver.quit()

'''
광고 데이터가 쓸모 없게 가져와지는 문제
1. 가격에 쉼표 존재하지 않음
2. 이미지가 no img -> 실제 상품은 no img 불러오는 src 없음
'''

'''
검색어 1. 노트북
검색어 2. LG전자 휘센 DQ
검색어 3. 다나와
검색어 4. 리슬링: 4246
검색어 5. 장우산
'''

'''
1. 한계점
'''

'''
키보드 인터럽트 처리하기~
'''

'''
1. 네이버
2. 쿠팡
3. g마켓
4. 
'''