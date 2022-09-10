import os
import time
import pytz
import csv
from dotenv import load_dotenv
from datetime import datetime, timedelta 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Get email and password from env
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# Connect to MyUWE
driver = webdriver.Safari()
driver.get("https://my.uwe.ac.uk/uPortal/f/u17l1s1100/normal/render.uP")

# Wait until redirect to sign in
wait = WebDriverWait(driver, 10)
wait.until(EC.title_is('Sign in to your account'))

# Wait until box to input email in is found
elem = EC.presence_of_element_located((By.ID, 'i0116'))
wait.until(elem)

# Once found, enter the email
input1 = driver.find_element(By.ID, "i0116")
input1.send_keys(EMAIL, Keys.RETURN)

# Wait until box to input password in is found
elem = EC.presence_of_element_located((By.ID, 'i0118'))
wait.until(elem)

# Once found, enter the password and click submit
input2 = driver.find_element(By.ID, "i0118")
input2.send_keys(PASSWORD)

# Submit the login
time.sleep(5)
button = driver.find_element(By.ID, "idSIButton9")
button.submit()

# Don't save login
time.sleep(2)
button = driver.find_element(By.ID, "idBtn_Back")
button.submit()

time.sleep(5)
driver.get("https://my.uwe.ac.uk/uPortal/f/u17l1s1100/normal/render.uP?pCt=classtimetable.u17l1n1111&pP_style=TextSpreadsheet%7CTextSpreadsheet&pP_days=1-7&pP_periods=1-28&pP_weeks=12")

# Get start and end date
title = driver.find_element(By.XPATH, '//*[@id="scrollingTable"]/table[1]/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/b')
title = title.text.split(' ')
date = datetime.strptime(f'{title[4][:-1]} {title[3]} {title[2][1:].zfill(2)}', "%Y %b %d")
days = ["Monday", "Tuesday", "Wednesday","Thursday", "Friday", "Saturday", "Sunday"]


# Loop through table
table = driver.find_element(By.XPATH, '//*[@id="scrollingTable"]/table[2]/tbody')
trs = table.find_elements(By.TAG_NAME, "tr")

lessons = []

for i in range(len(trs)): 
    if i == 0:
        continue
    else: 
        tds = trs[i].find_elements(By.TAG_NAME, "td")

        # Get the correct date
        previous = trs[i-1].find_elements(By.TAG_NAME, "td")[0].text
        if (tds[0].text != previous) and (i != 1):
            diff = days.index(tds[0].text) - days.index(previous)
            date += timedelta(days=diff)
        
        # Covert date & time for ISO Format (For Google API)
        st = tds[1].text.split(':')
        et = tds[2].text.split(':')
        start_time = date.replace(hour=int(st[0]), minute=int(st[1]), tzinfo=pytz.timezone('Europe/London')).isoformat()
        end_time = date.replace(hour=int(et[0]), minute=int(et[1]), tzinfo=pytz.timezone('Europe/London')).isoformat()

        lessons.append([start_time, end_time, tds[4].text, tds[5].text, tds[6].text])

# Write lessons to the schedule csv
with open('schedule.csv', 'w') as file:
    f = csv.writer(file)
    f.writerows(lessons)

driver.close()
