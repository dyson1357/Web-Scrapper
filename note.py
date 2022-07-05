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
page_path = driver.find_element(By.XPATH, '//*[@id="paginationArea"]/div/span')
total_page_text = page_path.text
total_page = int(re.sub(r'\D', '', total_page_text))
print(total_page)

curPage = 1
print_page = 0
dec_page = 1
pList = []

#  전체 페이지 순회
while curPage <= total_page:
    #  BS4 사용 전 초기화
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #  상품 리스트 파싱
    product_list = soup.select('div.main_prodlist.main_prodlist_list > ul > li')

    element = driver.find_element(By.ID, "AKCSearch")

    #  현재 페이지에 노출된 상품들의 제품명, 가격, 이미지 링크를 인기 상품 순서로 출력
    for i in product_list:
        if i.find('div', class_='prod_main_info'):
            name = i.select_one('p.prod_name > a').text.strip()
            price = getattr(i.select_one('p.price_sect > a'), 'text', None)
            if price == None:
                price = i.select_one('p.price_sect').text.strip()
            img_link = i.select_one('div.thumb_image > a > img').get('data-original')
            if img_link == None:
                img_link = i.select_one('div.thumb_image > a > img').get('src')
            #  상품 상세 페이지 접속
            driver.find_element(By.CLASS_NAME, "click_log_product_standard_title_").click()
            detail_img_link = driver.find_element(By.XPATH, '//*[@id="partContents_52_1"]/p/img').get('data-original')
            if detail_img_link == None:
                detail_img_link = driver.find_element(By.XPATH, '//*[@id="partContents_52_1"]/p/img').get('src')
            pList.append([name, price, img_link, detail_img_link])
            print(name, price, img_link, detail_img_link)
        print()



    curPage += 1
    dec_page += 1

    if curPage > total_page:
        print('크롤링 완료')
        break
    else:
        #  페이지 넘기는 작업 수행
        #  nth-child(N) -> 부모 안에 모든 요소 중 N번째 요소 https://lalacode.tistory.com/6 참고
        cur_css = 'div.paging_number_wrap > a:nth-child({})'.format(dec_page)

        if (dec_page - 1) % 10 == 0:
            print("if에 잡혀있음")
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'paging_edge_nav.paging_nav_next.click_log_page'))).click()
            del soup
            dec_page = 1
            print_page += 10
            time.sleep(3)

        else:
            print("else로 빠졌음")
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, cur_css))).click()
            del soup
            time.sleep(3)

        print(curPage)


def saveToFile(filename, list):
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(list)
    print(search_txt + '.csv 파일 저장 완료')


saveToFile(search_txt + '.csv', pList)

'''
검색어 1. 노트북
검색어 2. LG전자 휘센 DQ
검색어 3. 다나와
검색어 4. 리슬링
'''
