
import requests
import platform
import string
import threading
import time
import random
from random import choice, randint
import json
import os
from os import system, _exit, path

class ProxyGen():
    #unused
    def altupdate(self):
        try:
            arr = []
            link_list = [
            'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt'] 
            for link in link_list:
                for proxy in requests.get(link).content.decode().split("\n"):
                    arr.append(proxy)
            self.splited = arr
            return arr
        except Exception as e:
            print(e)

    def update(self):
        while True:
            data = ''
            urls = [
                "https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=10000&ssl=yes"]
            for url in urls:
                data += requests.get(url).text
                # scraping and splitting proxies
                self.splited += data.split("\r\n")
            time.sleep(600)

    def get_proxy(self):
        random1 = random.choice(self.splited)  # choose a random proxie
        return random1

    def FormatProxy(self):
        proxyOutput = {'https': 'socks4://'+self.get_proxy()}
        return proxyOutput

    def __init__(self):
        self.splited = []
        threading.Thread(target=self.update).start()
        time.sleep(3)