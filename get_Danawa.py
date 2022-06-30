from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv
import re


#  다나와 메인 페이지 오픈
#  chromedriver 설정, 4.0부터는 아래와 같이 써야 함
def open_driver():
    service = Service('C:/chrome/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.danawa.com/")
    time.sleep(2)
    return driver


#  페이지 넘김
def next_page(driver):
    #  총 페이지 수 도출
    page_path = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div[3]/div[2]/div[9]/div[2]/div[2]/div[5]/div/span")
    total_page_text = page_path.text
    total_page = int(re.sub(r'\D', '', total_page_text))
    print(type(total_page))


#  검색 및 출력
def search_prod(driver):
    #  검색어 입력
    #  셀레니움 업데이트로 find_elements_by_* 구문 사용 대신 find_elements() 구문을 사용
    search_txt = input('검색 키워드: ')
    driver.find_element(By.ID, "AKCSearch").click()
    element = driver.find_element(By.ID, "AKCSearch")
    element.send_keys(search_txt)

    #  검색 버튼 눌러 검색 수행
    driver.find_element(By.CLASS_NAME, "search__submit").click()

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
    return pList


#  파일 저장
def save_file(filename, inventory):
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(inventory)
    print("저장 완료")


driver = open_driver()
pList = search_prod(driver)
save_file('prod.csv', pList)
next_page(driver)

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
