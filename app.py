from flask import Flask, render_template
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
import re
import time
import uuid
from datetime import datetime

app = Flask(__name__)

MONGO_URI = "YourMongoDBURI"
client = MongoClient(MONGO_URI)
db = client['twitter-trending']
collection = db['trends']

def get_trending_topics():
    proxy_address = "YourProxyAddress"
    proxy_username = "YourProxyUsername"
    proxy_password = "YourProxyPassword"
    twitter_username = "TwitterUsername"
    twitter_password = "TwitterPassword"
    twitter_mail = "TwitterMail"
    sw_options = {
        'proxy': {
            'http': f'http://{proxy_username}:{proxy_password}@{proxy_address}',
            'https': f'https://{proxy_username}:{proxy_password}@{proxy_address}',
        }
    }

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service,options=chrome_options,seleniumwire_options=sw_options)
    
    driver.get('https://ssl-judge2.api.proxyscrape.com/')
    time.sleep(1)
    response = driver.page_source
    ip_address = re.search("HTTP_X_FORWARDED_FOR = (\d+\.)+\d+", response).group().split("=")[-1]
    driver.get("https://x.com/login")
    usernameXpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input'
    time.sleep(5)
    username = driver.find_element(By.XPATH, usernameXpath)
    username.send_keys(twitter_username)
    username.send_keys(Keys.RETURN)
    time.sleep(10) # ProxyMesh is slow, hence waiting so that it doesn't get blocked as X (Formerly, Twitter) likes to verify emails from proxies instead of directly getting authenticated
    
    unusualLoginXpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input'
    if driver.find_element(By.XPATH, unusualLoginXpath).is_displayed():
        mailXpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input'
        mail = driver.find_element(By.XPATH, mailXpath)
        mail.send_keys(twitter_mail)
        mail.send_keys(Keys.RETURN)
        time.sleep(5)
    
    passwordXpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'
    password = driver.find_element(By.XPATH, passwordXpath)
    password.send_keys(twitter_password)
    password.send_keys(Keys.RETURN)    
    driver.get("https://x.com/explore/tabs/trending")
    time.sleep(5)
    
    topicXpath = "//*[@class='css-146c3p1 r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-b88u0q r-1bymd8e']"
    topics = driver.find_elements(By.XPATH, topicXpath)
    topicArray = [topic.text for topic in topics[:5]]
    unique_id = str(uuid.uuid4())
    timestamp = datetime.now()
    record = {
        "_id": unique_id,
        "topics": topicArray,
        "timestamp": timestamp,
        "ip_address": ip_address
    }
    collection.insert_one(record)
    driver.quit()
    return record

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_trends', methods=['GET'])
def get_trends():
    data = get_trending_topics()
    return data

if __name__ == '__main__':
    app.run(debug=True)
