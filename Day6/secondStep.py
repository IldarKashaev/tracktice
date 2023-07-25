#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 14:23:55 2023

@author: ytrilda
"""
import requests
from bs4 import BeautifulSoup
from uuid import uuid4
import urllib


path = 'images/Avito/A/'
images, links = [], []
imgs = []

def carLinks(num):
    session = requests.Session()
    global links
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0'}
    
    for x in range(1, num): 
        payload = {'p': str(x)}
        r = session.get('https://www.avito.ru/all/gruzoviki_i_spetstehnika/avtobusy-ASgBAgICAURUjgI?cd=1', headers=headers, params=payload) #Connecting to the Website
        soup = BeautifulSoup(r.text, 'html.parser')
        
        for link in soup.find_all('a', attrs={'itemprop': 'url', 'rel': 'noopener'}):
            links.append(link.get('href')) #Extracting links

def imagesParser(links):
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0'}

    for x in range(len(links)): 
        r = session.get('https://avito.ru' + links[x], headers=headers) #Connecting to the Website
        soup = BeautifulSoup(r.text, 'html.parser')
        print(r)
        for image in soup.find_all('span', attrs={'class': 'image-frame-cover-lQG1h'}):
            imgLink = str(image)
            imgs.append(imgLink[66:-10])
            imgLink = imgLink[66:-10]
            imgDownloading(imgLink)
        
def imgDownloading(imgLink):
    image_name = f'{uuid4()}' + '.jpg' #Creating a unique name
    urllib.request.urlretrieve(imgLink, path + image_name) #Saving images

#carLinks(39)
imagesParser(links)
