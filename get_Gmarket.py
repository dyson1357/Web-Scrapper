from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import timedelta
import csv
import time
import re


options = webdriver.ChromeOptions()
options.add_argument("headless")

#  검색어 입력 및 결과 화면 출력
search_txt = input('Gmarket 검색 키워드: ')
num_of_req = int(input('가져올 상품 데이터 수: '))

#  시작 시간
start = time.time()

#  chromedriver 설정, 4.0부터는 아래와 같이 써야 함
service = Service('C:/chrome/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://browse.gmarket.co.kr/search?keyword=" + search_txt)
driver.implicitly_wait(10)

#  판매 인기순 정렬
driver.find_element(By.XPATH,
                    '//*[@id="region__content-status-information"]/div/div/div[2]/div[1]/div[1]/button').click()
driver.find_element(By.XPATH,
                    '//*[@id="region__content-status-information"]/div/div/div[2]/div[1]/div[2]/ul/li[2]').click()

item_count = 1
page = 1
pList = []
link_list = []
num = 1

#  전체 페이지 순회
while item_count <= num_of_req * 2:
    links = []
    #  상품 상세 페이지 링크 수집
    links = driver.find_elements(By.CLASS_NAME, 'link__item')

    for i in links:
        #  상세 페이지 링크 수집을 위한 a 태그의 href 속성 추출
        num += 1
        link_list.append(i.get_attribute('href'))
        link_list = list(dict.fromkeys(link_list))

        item_count += 1

        if item_count == num_of_req * 2:
            break

        #  페이지 넘기는 작업 수행
        if (item_count % 200) == 0:
            next_btn = driver.find_element(By.CLASS_NAME, 'link__page-next')
            if next_btn is None:
                print("마지막 페이지까지 완료")
            else:
                page += 1
                driver.find_element(By.CLASS_NAME, "link__page-next").send_keys(Keys.ENTER)
                driver.implicitly_wait(10)
                break
    if item_count == num_of_req * 2:
        break

prod_count = 1
#  수집된 링크 개수 확인(총 수집 요청 상품 수와 일치하는지 확인하기 위해)
print(len(link_list))

for product in link_list:
    #  상품 상세 페이지 접속
    driver.get(product)
    driver.implicitly_wait(10)

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
    brand_search = getattr(driver.find_element(
        By.CSS_SELECTOR, '#vip-tab_detail > div.vip-detailarea_productinfo.box__product-notice.js-toggle-content.on > '
                         'div.box__product-notice-list > table:nth-child(1) > tbody > tr:nth-child(7) > th'), 'text', None)

    if brand_search == "브랜드":
        brand = getattr(driver.find_element(
            By.CSS_SELECTOR, '#vip-tab_detail > div.vip-detailarea_productinfo.box__product-notice.'
                             'js-toggle-content.on > div.box__product-notice-list > table:nth-child(1) > tbody > '
                             'tr:nth-child(7) > td'), 'text', None)
    else:
        brand = "정보 없음"

    if brand == "상세설명 참조":
        brand = "정보 없음"
    brand = re.sub(r"^\s+|\s+$", "", brand)

    #  수집된 정보들 리스트에 추가
    pList.append([name, price, brand])
    print(str(prod_count) + " | 상품명: " + name + " / 가격: " + price + " / 브랜드: " + brand)
    prod_count += 1


#  크롤링 결과를 '검색어.csv' 파일로 저장
def saveToFile(filename, list):
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(list)
    print(search_txt + '.csv 파일 저장 완료')


#  pList = set(map(tuple, pList))
saveToFile(search_txt + '.csv', pList)
driver.quit()

#  종료 시간
end = time.time()
print("총 소요 시간(hh:mm:ss): ", timedelta(seconds=end-start))
