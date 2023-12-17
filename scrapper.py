import os
import pandas as pd
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
from parsel import Selector
import json
import logging


def create_logger():

    LOG_DIR = "scrapping_logs"
    CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    LOG_FILE_NAME = f"log_{CURRENT_TIME_STAMP}.log"

    os.makedirs(LOG_DIR, exist_ok=True)
    LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)

    # Logging Settings
    logging.basicConfig(
        filename=LOG_FILE_PATH,
        filemode="w",
        format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO)
    return logging.getLogger('api_logs')

class LinkedinScrapper():

    def __init__(self, linkedin_home_url, linkedin_id, linkedin_password):

        self.linkedin_home_url = linkedin_home_url
        self.linkedin_id = linkedin_id
        self.linkedin_password = linkedin_password
        self.current_time = str(datetime.now())[:10]
        self.driver = webdriver.Chrome()

    def linkedin_sign_in(self):

        self.driver.get(self.linkedin_home_url)
        logging.info(f'Going to page: {self.linkedin_home_url}')
        time.sleep(10)

        user_name = self.driver.find_element(By.ID,"username")
        user_name.send_keys(self.linkedin_id)
        time.sleep(random.uniform(2.5, 4.9))

        password = self.driver.find_element(By.ID,"password")
        password.send_keys(self.linkedin_password)
        time.sleep(random.uniform(2.5, 4.9))

        sign_button = self.driver.find_element(By.XPATH,'//*[@type="submit"]')
        sign_button.click()
        time.sleep(80)

    def linkedin_url_scrapper(self, number_of_scrolls, url_file_path='url.csv'):

        linkedin_url_list = []

        logging.info(f'Number of scrolls: {number_of_scrolls}')
        
        for i in range(number_of_scrolls):
            l=self.driver.find_elements(By.XPATH,"//*[@class= 'display-flex list-style-none flex-wrap']/li/div/section/div/div/div/a[@href]")
            logging.info(f"Scroll Number: {i+1}, Last element of l in this iteration: {l[-1]}")
            self.driver.execute_script('scrollBy(0,100)')
            time.sleep(random.uniform(2.5, 4.9))

        for j in l:
            url = j.get_attribute('href')
            linkedin_url_list.append(url)
            df = pd.DataFrame(data = [[url]]) 
            file_exists = os.path.exists(url_file_path)
            df.to_csv(url_file_path, mode='w' if not file_exists else 'a', index=False, header=not file_exists)
            time.sleep(random.uniform(2.5, 4.9))
        
        logging.info(f"Number of url collected: {len(linkedin_url_list)}")

        return linkedin_url_list
    
    def linkedin_profile_scrapper(self, linkedin_url_list, candidate_file_path='candidate.json'):

        for url in linkedin_url_list:

            self.driver.get(url)
            time.sleep(random.uniform(2.5, 4.9))

            sel = Selector(text=self.driver.page_source)
            name = sel.xpath('//*[starts-with(@class,"text-heading-xlarge inline t-24 v-align-middle break-words")]/text()').extract_first()

            if name:
                name = name.strip()

            job_title = sel.xpath('//*[starts-with(@class,"text-body-medium break-words")]/text()').extract_first()

            if job_title:
                job_title = job_title.strip()

            try:
                company = self.driver.find_element(By.XPATH,'//ul[@class="pv-text-details__right-panel"]').text

            except:
                company = 'NA'

            if company:
                company = company.strip()

            try:
                college = self.driver.find_element(By.XPATH,'//ul[@class="pv-text-details__right-panel"]/li[2]').text
            
            except:
                college = 'NA'
            if college:
                college = college.strip()

            location = sel.xpath('//*[starts-with(@class,"text-body-small inline t-black--light break-words")]/text()').extract_first()

            if location:
                location = location.strip()
            
            try:
                about = self.driver.find_element(By.XPATH,'//*[@id="profile-content"]/div/div[2]/div/div/main/section[2]/div[3]/div/div/div/span[1]').text
            except:
                about = "NA"
            if about:
                about=about.strip()

            candidate_data = {'name':name, 'job_title':job_title, 'company':company, 'college':college, 'location':location, 'about':about, 'url':url}

            with open(candidate_file_path, 'r') as f:
                existing_data = json.load(f)
            logging.info(f"New Data: {candidate_data}")
            existing_data['candidate'].append(candidate_data)

            with open(candidate_file_path, 'w') as json_file:
                json.dump(existing_data, json_file, indent=4)

            time.sleep(random.uniform(2.5, 4.9))

            df = pd.DataFrame(data = [[name, job_title, company, college, location, url, about]],
                    columns = ["Candidate_Name", "Job_title", "Company", "Colleg", "Location", "Linkedin_URL", "About"])          
            file_exists = os.path.exists("TCS_f.csv")
            df.to_csv("TCS_f.csv", mode='w' if not file_exists else 'a', index=False, header=not file_exists)

    def pipeline(self, number_of_scrolls=10):

        logging.info('Signing in LinkedIn')
        self.linkedin_sign_in()
        logging.info('Sign Up Successfull')
        linkedin_url_list = self.linkedin_url_scrapper(number_of_scrolls=number_of_scrolls)
        self.linkedin_profile_scrapper(linkedin_url_list)
        logging.info('All profiles extracted successfully')

logging = create_logger()
obj = LinkedinScrapper(linkedin_home_url="https://www.linkedin.com/company/tata-consultancy-services/people/", 
                       linkedin_id='*************', 
                       linkedin_password='******')
obj.pipeline(number_of_scrolls=10)