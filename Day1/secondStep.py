#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 11:14:09 2023

@author: ytrilda
"""

import os 
import urllib.request
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By

try:
    os.mkdir("img") #Создаем папку и проверяем ее на существование
except: 
    print("Папка уже существует!")
    
num = int(input('Введите количество страниц для парсинга: '))
if num < 1:
    sys.exit('Число меньше 1')
for x in range(num): 
    driver = webdriver.Firefox() #Устанавливаем драйвер
    driver.implicitly_wait(0.5)
    driver.minimize_window()
    driver.get("https://migalki.net/images.php" + "?start=" + str(x*18)) #Подключаемся к сайту
    posts, names = [], []
    divs = driver.find_elements(By.CLASS_NAME, 'col-xs-4')     
    for div in divs:
        img = div.find_element(By.TAG_NAME, 'img') #Ищем изображения
        post = img.get_attribute('src')
        if (post not in posts and len(posts) < 18):
            posts.append(post) 
            names.append(post[-36:]) #Получаем названия файлов
    
    for i in range(len(posts)):
        urllib.request.urlretrieve(posts[i], 'img/' + str(names[i])) #Сохраняем изображения
    
    driver.quit() #Закрываем браузер