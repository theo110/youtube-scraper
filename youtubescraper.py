from os import link
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time
import pandas as pd
import json
import requests

videos = []
titles = []
links = []


def getVideoData(keyword):
    option = Options()
    option.headless = False
    service = Service('geckodriver.exe')
    driver = webdriver.Firefox(service=service,options=option)
    baseUrl = 'https://www.youtube.com/'

    driver.get(f'{baseUrl}/search?q={keyword}')
    time.sleep(3)
    titles0 = driver.find_elements(By.CSS_SELECTOR,'#video-title > yt-formatted-string')
    for title in titles0:
        titles.append(title.get_attribute('innerText'))
    links0 = driver.find_elements(By.CSS_SELECTOR,'#video-title')
    for link in links0:
        if link.get_attribute('href') is not None:
            links.append(link.get_attribute('href'))
    views0 = driver.find_elements(By.CSS_SELECTOR,'#metadata-line > span:nth-child(1)')
    for i in range(len(views0)):
        video = {
            "Title": titles[i],
            "Link": links[i],
            "Views": views0[i].get_attribute('innerText'),
        }
        videos.append(video)


def main():
    keyword = input("Please enter a keyword to search up: ")
    getVideoData(keyword)

    jsonData = json.dumps(videos)

    #post data to your url could use a lambda function to store in AWS dynamodb.
    lambda_url = "http://youtube.com"
    reply = requests.post(lambda_url,data=jsonData)

    #converts data to csv
    df = pd.DataFrame(videos)
    df.to_csv("data.csv", encoding='utf-8', index=False)

if __name__ == "__main__":
    main()