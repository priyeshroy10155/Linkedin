import requests as rq
import os
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import random
from parsel import Selector
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
current_time = str(datetime.datetime.now())[:10]


driver=webdriver.Chrome()
def WebScraper(url):
    driver.get(url)
    time.sleep(random.uniform(2.5, 4.9))
    sel = Selector(text=driver.page_source)
    
    name = sel.xpath('//*[starts-with(@class,"text-heading-xlarge inline t-24 v-align-middle break-words")]/text()').extract_first()
    if name:
        name=name.strip()

    job_title=sel.xpath('//*[starts-with(@class,"text-body-medium break-words")]/text()').extract_first()
    if job_title:
        job_title=job_title.strip()

    try:
        company=driver.find_element(By.XPATH,'//ul[@class="pv-text-details__right-panel"]').text
    except:
        company='NA'
    if company:
        company=company.strip()

    try:
        colleg=driver.find_element(By.XPATH,'//ul[@class="pv-text-details__right-panel"]/li[2]').text
    except:
        colleg='NA'
    if colleg:
        colleg=colleg.strip()

    location = sel.xpath('//*[starts-with(@class,"text-body-small inline t-black--light break-words")]/text()').extract_first()
    if location:
        location=location.strip()
    
    try:
        about = driver.find_element(By.XPATH,'//*[@id="profile-content"]/div/div[2]/div/div/main/section[2]/div[3]/div/div/div/span[1]').text
    except:
        about="NA"
    if about:
        about=about.strip()
    

    df = pd.DataFrame(data = [[name, job_title, company, colleg, location, url, about]],
                    columns = ["Candidate_Name", "Job_title", "Company", "Colleg", "Location", "Linkedin_URL", "About"])          
    file_exists = os.path.exists("TCS_f_1.csv")
    df.to_csv("TCS_f_1.csv", mode='w' if not file_exists else 'a', index=False, header=not file_exists)

def Navigation(URL):
    driver.get(URL)
    time.sleep(10)
    #time.sleep(random.uniform(2.5, 4.9))
    #driver.maximize_window()

    #user_name = driver.find_element(By.ID,"session_key")
    user_name = driver.find_element(By.ID,"username")
    user_name.send_keys('***********')
    time.sleep(random.uniform(2.5, 4.9))

    password = driver.find_element(By.ID,"password")
    password.send_keys('*************')

    time.sleep(random.uniform(2.5, 4.9))

    sign_button = driver.find_element(By.XPATH,'//*[@type="submit"]')
    sign_button.click()
    time.sleep(80)
    L=[]
    L1=L
    x=0
    while True:
        x+=1
        l=driver.find_elements(By.XPATH,"//*[@class= 'display-flex list-style-none flex-wrap']/li/div/section/div/div/div/a[@href]")
        driver.execute_script('scrollBy(0,100)')
        time.sleep(random.uniform(2.5, 4.9))
        if x>100:
            break
    for i in l:
        L.append(i.get_attribute("href"))
        url_1= (i.get_attribute("href"))
        df1 = pd.DataFrame(data = [[url_1]])          
        file_exists = os.path.exists("TCS_URL_2.csv")
        df1.to_csv("TCS_URL_2.csv", mode='w' if not file_exists else 'a', index=False, header=not file_exists)

        #WebScraper(i.get_attribute("href"))
        time.sleep(random.uniform(2.5, 4.9))
    for j in L:
        WebScraper(j)
        time.sleep(random.uniform(2.5, 4.9))
Navigation("https://www.linkedin.com/company/tata-consultancy-services/people/")