# SPOTIFY LISTEN BOT
# COMMANDEERED BY PHOON

from SpotifyAccountManager.SpotifyAccountManager import SpotifyAccountManager
from os import access
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as selEc
from selenium.webdriver.common.by import By as selBy
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import json, time, threading, random, sys
from modules.spotify import links, xpaths
import requests, json
import time, os, sqlite3, random, string, shutil

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType, SoftwareType

from tqdm import tqdm

def random_user_agent() -> str: 
    return UserAgent(software_names=[SoftwareName.CHROME.value], hardware_types={HardwareType.COMPUTER.value}, limit=100).get_random_user_agent()

#def random_user_agent() -> str: return UserAgent(software_names=[SoftwareName.ANDROID.value], hardware_types={HardwareType.MOBILE.value}, limit=100).get_random_user_agent()

def get_random_name() -> str: return json.loads(requests.get("https://api.namefake.com/").text)["name"]
def get_random_string(length: int) -> str: return "".join(random.choice(string.ascii_lowercase+string.digits) for i in range(length))
def get_random_text(length: int) -> str: return "".join(random.choice(string.ascii_lowercase) for i in range(length))

import time, sqlite3

from src.chrome import Chrome
from src.proxy.proxy import Proxy

class SpotifyViewBot:
    def __init__(self, headless) -> None:
        print("* Bot Init *")
        selUrl = input(" * Insert Spotify playlist url (empty for default): ")
        self.headless = headless
        # proxies = list(filter(None, open("data/proxies/proxies.txt", "r").read().split("\n")))
        #TODO: Implement threading here
        i = 0
        self.run(selUrl, self.headless, i)

    def login(self, browser, wait, i):
        #TODO: Dynamically get these from the generator...
        email = "O4IctunvPe@yahoo.com"
        password = "VDQydO0vQmEtbR"

        

        browser.get(links['loginPage'])
        user_form = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["user_form"])))
        user_form.send_keys(email)
        
        pass_form = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["pass_form"])))
        pass_form.send_keys(password)
        
        submit_btn = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["submit_btn"])))
        submit_btn.click()

        #This weird button sometimes appears... probably for a tangible reason I haven't determined
        try:
            weird_btn = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["weirdButton"])))
            weird_btn.click()
        except:
            pass


    def run(self, _url, _headless, i=None, proxy=None):
        #TODO: Dynamically get proxies ... perhaps include proxy used in account generation with the email/pass?
        Proxy(proxy, i)

        #TODO: reenable proxy support
        options = Options()
        #options.add_argument(f'user-agent={random_user_agent()}')
        print("OPTIONS: "+str(options))
        chrome = Chrome()
        
        browser = webdriver.Chrome(executable_path=chrome.CHROMEDRIVER, options=options) #chrome.options(i=i, proxy=proxy)
        chrome.execute(browser)
        wait = WebDriverWait(browser, 10)
        
        #Login first
        self.login(browser, wait, i)

        #Navigate to predefined playlist
        #TODO: Support rotating playlists
        browser.get(_url) if _url else browser.get(links["default"])
        time.sleep(5)
        
         #mfw gdpr banner
        try:  
            btn = wait.until(selEc.element_to_be_clickable((selBy.XPATH, '//*[contains(@class, "onetrust-close-btn-handler")]')))  
            btn.click()
        except Exception as e:
            print("no gdpr banner? weird...: " + str(e))

        try:
            #btn = wait.until(selEc.presence_of_element_located((selBy.XPATH, xpaths['closeButton'])))
            btn2 = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths['closeButton'])))  
            #btn3 = wait.until(selEc.presence_of_element_located((selBy.CSS_SELECTOR, '//*[contains(@class, "onetrust-close-btn-handler")]')))
            #btn.click()
            btn2.click()
            #btn3.click()
        except Exception as e:
            print("no close button...: " + e)

        shuffle_btn = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["shuffle_btn"])))
        repeat_btn = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["repeat_btn"])))

        if "control-button--active" not in shuffle_btn.get_attribute("class"):
            time.sleep(1)
            shuffle_btn.click()

        if "spoticon-repeat-16 control-button--active" in repeat_btn.get_attribute("class"):
            pass
        elif "spoticon-repeatonce-16 control-button--active" in repeat_btn.get_attribute("class"):
            time.sleep(1)
            repeat_btn.click()
            time.sleep(1)
            repeat_btn.click()
        else:
            time.sleep(1)
            repeat_btn.click()
        try:
            play_btn = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["playButton"])))
            #play_btn.click()
            play_btn.click()
           
        except:
            play_btn = wait.until(selEc.element_to_be_clickable((selBy.XPATH, "/html/body/div[3]/div/div[2]/div[3]/main/div[2]/div[2]/div/div/div[2]/section/div[3]/div/button[1]")))
            play_btn.click()
        while True:
            time.sleep(random.randint(55, 70))
            song_name = wait.until(selEc.presence_of_element_located((selBy.XPATH, xpaths["song_name"]))).text
            print(" * Played {0} for 3".format(song_name))
            skip_btn = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["skip_btn"])))
            skip_btn.click()

    """
    threads=[]
    while True:
        i+=1
        if len(threads) == 5:
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            threads=[]
        threads.append(threading.Thread(target=run, args=[selUrl, headless, i]).start())
        time.sleep(1)
    """
if __name__ == '__main__':
    head = "--headless" in sys.argv
    bot = SpotifyViewBot(headless=head)