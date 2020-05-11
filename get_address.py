# /usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from tqdm import tqdm as tqdm

chrome_options = options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(chrome_options=chrome_options)

'''
from
https://www.pingshu8.com/play_31539.html
to
https://www.pingshu8.com/play_31638.html
'''
weburls = []
downloadlink = []
for i in range(31539, 31639):
    weburls.append(f'https://www.pingshu8.com/play_{i}.html')
with open('temp_all_address_liuluoguo_guodegang', 'w') as fid:
    for i ,url in enumerate(tqdm(weburls)):
        try:
            # if i == 5: break
            driver.get(url)
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            wait = WebDriverWait(driver, 10)
            wait.until(EC.title_contains(" "))
            ele = soup.find_all(id='jp_audio_0')
            truexx = [k.get("src") for k in soup.find_all(id='jp_audio_0')][0]
            downloadlink.append(f'{url}|{truexx}')
            print(f'get webpage :{url},true address is :{truexx}')
        except:
            downloadlink.append(f'{url}| ')
            continue
    fid.writelines('\n'.join(downloadlink))
