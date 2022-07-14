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


driver.find_element(By.XPATH, '//*[@id="s0-51-12-5-4[0]"]/div[2]/div[1]/div/ul/li[4]').click()
driver.find_element(By.XPATH, '//*[@id="nid-fly-7"]/button/span').send_keys(Keys.ENTER)
driver.find_element(By.XPATH, '//*[@id="nid-fly-6"]/div[2]').send_keys(Keys.ENTER)
