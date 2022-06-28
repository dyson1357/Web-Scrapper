from selenium import webdriver
from urllib.request import urlopen
from selenium.webdriver.common.keys import Keys
import time
import urllib.request

driver = webdriver.Chrome('C:/chrome/chromedriver.exe')  # 여기에 크롬드라이브 다운로드 받은 경로를 입력한다.
driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")
elem = driver.find_element_by_name("q")
elem.send_keys("한수환 총장")
#엔터를 침
elem.send_keys(Keys.RETURN)

SCROLL_PAUSE_TIME = 1
#스크롤 높이 구함
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    #브라우저 끝까지 스크롤 내림
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #페이지 로드 기다려
    time.sleep(SCROLL_PAUSE_TIME)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            driver.find_element_by_css_selector(".mye4qd").click()
        except:
            break
    last_height = new_height

images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd") #여러개의 이미지 선택하기, 클래스 이름 기준
count = 1
for image in images:
    try:
        image.click()
        time.sleep(2)
        imgUrl = driver.find_element_by_xpath(
            '/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img').get_attribute(
            "src")
        urllib.request.urlretrieve(imgUrl, "./test/" + str(count) + ".txt")
        count = count + 1
    except:
        pass

driver.close()