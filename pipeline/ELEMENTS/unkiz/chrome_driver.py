def unkiz_crolling():
  pass

# import modules
import glob
import time
import selenium
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

### basic settings
options = Options()
# web chrome version
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
options.add_argument('user-agent='+user_agent)
# full screen
options.add_argument('--start-fullscreen')
# set directory
options.add_experimental_option('prefs', {
  "download.default_directory": "C:/Users/enkee/OneDrive/바탕 화면/SNURO-EDM/pipeline/unkiz"
})
# hide logs
options.add_experimental_option("excludeSwitches", ["enable-logging"])

### start crolling
# set driver
s = Service('./pipeline/unkiz/chromedriver')
URL = 'http://unkiz.com/user/login'
# start driver
driver = webdriver.Chrome(service = s,options=options)
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

# transform

# 알 수 없는 다운로드 오류 발생