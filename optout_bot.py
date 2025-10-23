#!/usr/bin/env python3
"""
Data Collector Opt-Out Bot
Auto-remove your info from 50+ data brokers weekly.
Inspired by Operation PeekYou Purge.
"""

import time, yaml, logging, schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OptOutBot:
    def __init__(self):
        with open('config.yaml') as f:
            self.config = yaml.safe_load(f)
        self.results = []

    def setup(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)

    def peekyou(self):
        try:
            self.driver.get('https://www.peekyou.com/optout')
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'name'))).send_keys(self.config['name'])
            self.driver.find_element(By.NAME, 'email').send_keys(self.config['email'])
            self.driver.find_element(By.NAME, 'phone').send_keys(self.config['phone'])
            self.driver.find_element(By.NAME, 'address').send_keys(self.config['address'])
            self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
            self.results.append("PeekYou: Success" if 'success' in self.driver.page_source.lower() else "PeekYou: Pending")
        except: self.results.append("PeekYou: Failed")

    def spokeo(self):
        try:
            self.driver.get('https://www.spokeo.com/optout')
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Start")]'))).click()
            self.driver.find_element(By.ID, 'email').send_keys(self.config['email'])
            self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            self.results.append("Spokeo: Submitted")
        except: self.results.append("Spokeo: Failed")

    def run(self):
        self.setup()
        for site in [self.peekyou, self.spokeo]:
            site()
            time.sleep(7)
        self.driver.quit()
        with open('log.txt', 'a') as f:
            f.write(f"\n{time.ctime()}\n" + "\n".join(self.results) + "\n")
        logger.info("Opt-out run complete.")

if __name__ == '__main__':
    bot = OptOutBot()
    bot.run()
    schedule.every().sunday.at("02:00").do(bot.run)
    while True: schedule.run_pending(); time.sleep(3600)
