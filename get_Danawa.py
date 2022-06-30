from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

#  다나와 메인 페이지 오픈
#  chromedriver 설정, 4.0부터는 아래와 같이 써야 함
service = Service('C:/chrome/chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get("https://www.danawa.com/")
time.sleep(2)

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

#  현재 페이지에 노출된 상품들의 제품명, 가격, 이미지 링크를 인기 상품 순서로 출력
for i in product_list:
    if i.find('div', class_='prod_main_info'):
        name = i.select_one('p.prod_name > a').text.strip()
        price = i.select_one('p.price_sect > a').text.strip()
        img_link = i.select_one('div.thumb_image > a > img').get('data-original')
        if img_link == None:
            img_link = i.select_one('div.thumb_image > a > img').get('src')
        print(name, price, img_link)
    print()

driver.close()


'''
해야 할 것
1. 다나와 검색 페이지 접속 0
2. 검색어 입력
3. 검색
4. 스크롤 제일 아래로 내리고, 다 내리면 다음 페이지
5. 페이지 끝까지 읽음
6. 각 제품별 이름, 가격, 사진 수집
7. 해당 내용을 파일로 저장
'''

