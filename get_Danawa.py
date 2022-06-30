from selenium import webdriver
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
driver.get("https://www.danawa.com/")
time.sleep(2)


#  검색어 입력
search_txt = input('검색 키워드: ')
driver.find_element(By.ID, "AKCSearch").click()
element = driver.find_element(By.ID, "AKCSearch")
element.send_keys(search_txt)

#  검색 버튼 눌러 검색 수행
driver.find_element(By.CLASS_NAME, "search__submit").click()


#  총 페이지 수 도출
page_path = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div[3]/div[2]/div[9]/div[2]/div[2]/div[5]/div/span")
total_page_text = page_path.text
total_page = int(re.sub(r'\D', '', total_page_text))
print(total_page)

curPage = 1

#  전체 페이지 순회
while curPage <= total_page:
    #  BS4 사용 전 초기화
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #  상품 리스트 파싱
    product_list = soup.select('div.main_prodlist.main_prodlist_list > ul > li')

    pList = []

    #  현재 페이지에 노출된 상품들의 제품명, 가격, 이미지 링크를 인기 상품 순서로 출력
    for i in product_list:
        if i.find('div', class_='prod_main_info'):
            name = i.select_one('p.prod_name > a').text.strip()
            price = i.select_one('p.price_sect > a').text.strip()
            img_link = i.select_one('div.thumb_image > a > img').get('data-original')
            if img_link == None:
                img_link = i.select_one('div.thumb_image > a > img').get('src')
            pList.append([name, price, img_link])
            print(name, price, img_link)
        print()
    curPage += 1

    #  페이지 순회 완료 되면 수행
    if curPage > total_page:
        print('Crawling succeed')
        break

    #  페이지 넘기는 작업 수행
    cur_css = 'div.paging_number_wrap > a:nth-child({})'.format(curPage)
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, cur_css))).click()
    del soup
    time.sleep(3)
    print(curPage)






'''
해야 할 것
1. 다나와 검색 페이지 접속 - 0
2. 검색어 입력 - 0
3. 검색 - 0
4. 총 페이지 수 파악
5. for문 처리 해서 각 페이지 돌면서
    5.1. 상품 목록 읽고 이름, 가격, 이미지 긁어옴
    5.2. 긁어온 데이터 저장
6. 종료
'''

'''
검색어 1. 노트북
검색어 2. LG전자 휘센 DQ
'''
