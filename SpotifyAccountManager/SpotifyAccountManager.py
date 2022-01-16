import platform
import string
from SpotifyAccountManager.ProxyGen import ProxyGen
import threading
import time
import random
from random import choice, randint
import json
import os
from os import system, _exit, path

import requests

if platform.system() == "Windows":  # checking OS
    title = "windows"
else:
    title = "linux"

credentialsPath = "credentials.json"

#Copied from other script
#headers = {'User-agent': 'S4A/2.0.15 (com.spotify.s4a; build:201500080; iOS 13.4.0) Alamofire/4.9.0', 'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8', 'Accept': 'application/json, text/plain;q=0.2, */*;q=0.1', 'App-Platform': 'IOS', 'Spotify-App': 'S4A', 'Accept-Language': 'en-TZ;q=1.0', 'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5', 'Spotify-App-Version': '2.0.15'}
domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'hotmail.co.uk', 'hotmail.fr', 'outlook.com', 'icloud.com', 'mail.com', 'live.com', 'yahoo.it', 'yahoo.ca', 'yahoo.in', 'live.se', 'orange.fr', 'msn.com', 'mail.ru', 'mac.com']

def randomName(size=10, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for i in range(size))

def randomPassword(size=14, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for i in range(size))

class SpotifyAccountManager:
    def __init__(self, maxthreads = 4) -> None:
        #These to be populated in setup()
        self.maleNames = ["Bob"]
        self.femaleNames = ["Alice"]
        self.credentials = {}

        self.maxthreads = maxthreads

        self.proxy = ProxyGen()
        self.setup()

    def setup(self):
        if path.exists('names/male.txt'):
            with open('names/male.txt', 'r', encoding = 'UTF-8') as f:
                for line in f.read().splitlines():
                    if line != '':
                        self.maleNames.append(line)
        if path.exists('names/female.txt'):
            with open('names/female.txt', 'r', encoding = 'UTF-8') as f:
                for line in f.read().splitlines():
                    if line != '':
                        self.femaleNames.append(line)
        if path.exists(credentialsPath):
            f = open(credentialsPath)
            try:
                self.credentials = json.load(f)
                print(f'loaded creds... {str(self.credentials)}')
            except Exception as e:
                print(f'error loading credentials... {str(e)}')
                self.credentials = {'credentials': []}     

    def creator(self, maxi):
        created = 0
        errors = 0

        while created < maxi:
            print(f'Generating | {str(created)}/{str(maxi)} | Errors: {str(errors)} | Proxy: {str(self.proxy.FormatProxy())}')
            
            s = requests.session()

            gender = choice(['male', 'female'])
            displayname = choice(self.maleNames) if gender == 'male' else choice(self.femaleNames)
            email = randomName() + "@" + choice(domains)
            password = randomPassword()
            birth_year = str(randint(1970, 2000))
            birth_month = str(randint(1, 12))
            birth_day = str(randint(1, 28))
            #print(f'birthday: {birth_day}, birthyear: {birth_year}')
            data = {
                "displayname": displayname,
                "creation_point": "https://login.app.spotify.com?utm_source=spotify&utm_medium=desktop-win32&utm_campaign=organic",
                "birth_month": birth_month,
                "email": email,
                "password": password,
                "creation_flow": "desktop",
                "platform": "desktop",
                "birth_year": birth_year,
                "iagree": "1",
                "key": "4c7a36d5260abca4af282779720cf631",
                "birth_day": birth_day,
                "gender": gender,
                "password_repeat": password,
                "referrer": ""
            }

            try:
                r = s.post("https://spclient.wg.spotify.com/signup/public/v1/account/",
                        data=data, proxies=self.proxy.FormatProxy())

                if '{"status":1,"' in r.text:
                    self.credentials['credentials'].append({"username": email, "password": password, "proxy": self.proxy.FormatProxy()})
                    created += 1
                else:
                    errors += 1
            except Exception as e:
                #print("Error creating: " + str(e))
                pass
        print(f'\n=========\nDONE\n==========\nCreds:\n{str(self.credentials)}')
        open(credentialsPath, "w").write(json.dumps(self.credentials))
        return        

    def genNewAccounts(self, numAccounts = 1):
        openThreads = []
        
        while len(openThreads) < self.maxthreads:
            openThreads.append(threading.Thread(target=self.creator(maxi=numAccounts)))
            openThreads[-1].start()

        while len(openThreads) > 0:
            time.sleep(5)
            newOpenThreads = []
            for thread in openThreads:
                if thread.is_alive():
                  newOpenThreads.append(thread)
            if len(openThreads) == 0:
                return self.credentials

if __name__ == '__main__':
    accGen = SpotifyAccountManager()
    accGen.genNewAccount()


   
