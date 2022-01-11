# version
# selenium : 4.1.0
# python 3.10.0

# import modules
import glob
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common import keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


### start crolling
URL = 'http://unkiz.com/user/login'
driver = webdriver.Firefox(executable_path='./pipeline/unkiz/geckodriver')
# get url (unkiz)
driver.get(url=URL)

### login
id = driver.find_element(By.CLASS_NAME, 'Input_input__2FfX3.Input_fluid__33hRL').send_keys('codingchild')
pw = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/input[2]').send_keys('@learning1')
click = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/button').click()

### xAPI button
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/div[1]/div/div/div[2]/div[1]'))).click()

### download button
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/div[2]/div/a'))).send_keys(Keys.RETURN)

### error prediction - 곧이어 다른 버튼 누르기
waitfor = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div/div')
waitfor.click()

# wait : 종료 조건 = .json 확장자 파일 생성
print("Waiting for download to complete")
path = 'C:/Users/enkee/OneDrive/바탕 화면/SNURO-EDM/pipeline/unkiz'
at_least_1 = lambda x: len(x("{0}/*.json*".format(path))) > 0
WebDriverWait(glob.glob, 300).until(at_least_1)

driver.implicitly_wait(300)
driver.implicitly_wait(300)
driver.implicitly_wait(300)
driver.implicitly_wait(300)

print("Download Done")

# download 기다리기 - error

driver.close()