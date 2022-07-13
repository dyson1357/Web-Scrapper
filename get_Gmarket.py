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

#  chromedriver 설정, 4.0부터는 아래와 같이 써야 함
service = Service('C:/chrome/chromedriver.exe')
driver = webdriver.Chrome(service=service)

#  검색어 입력 및 결과 화면 출력
search_txt = input('Gmarket 검색 키워드: ')
driver.get("https://browse.gmarket.co.kr/search?keyword=" + search_txt)
time.sleep(2)

driver.find_element(By.XPATH,
                    '//*[@id="region__content-status-information"]/div/div/div[2]/div[1]/div[1]/button').click()
driver.find_element(By.XPATH,
                    '//*[@id="region__content-status-information"]/div/div/div[2]/div[1]/div[2]/ul/li[2]').click()


total_item = driver.find_element(By.CLASS_NAME, 'text__item-count').text
print("*" + search_txt + "*" + " 전체 상품 수: " + total_item)

