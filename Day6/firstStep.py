import requests
import os 
from bs4 import BeautifulSoup
from uuid import uuid4
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import data

path = 'images/'
links, carNumbers = [], []
types = [0, 0, 0, 0]


try:
    os.mkdir(path) #Making a new folders if it does not exist
except: 
    print("Папка уже существует!")

def carParsing(num):
    session = requests.Session()
    global links, carNumbers
    
    for x in range(num): 
        carNumbers, links = [], []
        payload = {'start': str(x*18)}
        r = session.get('https://migalki.net/images.php', params=payload) #Connecting to the Website
        soup = BeautifulSoup(r.text, 'html.parser')
        
        t1, t2 = [], []
        for link in soup.find_all('a'):
            t = link
            t1 = str(t).splitlines()
            for x in range(len(t1)):
                if t1[x].startswith('<a class="btn btn-success"'): #Search for lines containing a link to an image
                    t2.append(t1[x])
            t3 = '\n'.join(t2)
            soup = BeautifulSoup(t3, 'html.parser')
        
        for link in soup.find_all('a'):
            links.append(link.get('href')) #Extracting links
            carNumbers.append(link.get('onclick'))
            
        getNumbers(carNumbers)
        normalizeNumbers(carNumbers)
        carType(links, carNumbers)
    
def getNumbers(carNumbers): #Getting car numbers
    for i in range(len(carNumbers)): 
        for x in range(10):
            carNumbers[i] = carNumbers[i].replace("ImagePreviewWithPlate($(this).prop('href'), '/informer/" + str(x) + "/540/", '')
        carNumbers[i] = carNumbers[i].replace(".png'); return false;", '')
    for x in range(len(carNumbers), 0, -1): 
        if "ImagePreview($(this).prop('href')" in carNumbers[x-1]:
            carNumbers.pop(x-1)
            links.pop(x-1)
           
def normalizeNumbers(carNumbers): #Normalizing these numbers
    for x in range(len(carNumbers)):
        temp = list(carNumbers[x])
        for i in range(len(temp)):
            temp[i] = temp[i].replace('A', 'А')
            temp[i] = temp[i].replace('B', 'В')
            temp[i] = temp[i].replace('E', 'Е')
            temp[i] = temp[i].replace('K', 'К')
            temp[i] = temp[i].replace('M', 'М')
            temp[i] = temp[i].replace('H', 'Н')
            temp[i] = temp[i].replace('O', 'О')
            temp[i] = temp[i].replace('P', 'Р')
            temp[i] = temp[i].replace('C', 'С')
            temp[i] = temp[i].replace('T', 'Т')
            temp[i] = temp[i].replace('Y', 'У')
            temp[i] = temp[i].replace('X', 'Х')
        carNumbers[x] = ''.join(temp)
        
def carType(links, carNumbers):
    url_login = "https://vin.info/login"
    driver = webdriver.Firefox()
    driver.get(url_login)
    driver.minimize_window()
    element = driver.find_element(By.NAME, 'email') #Authentification on vin.info
    element.send_keys(data.vinInfoEmail)
    element = driver.find_element(By.NAME, 'password')
    element.send_keys(data.vinInfoPass)
    button = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/form/div[4]/button")
    button.click()
    button = driver.find_element(By.XPATH, "/html/body/div/div/header/nav/div[2]/div/div/div/div[1]/a/img")
    button.click()
    time.sleep(1)
    for x in range(len(links)):
        element = driver.find_element(By.NAME, "car_number")
        element.clear()
        element.send_keys(carNumbers[x])
        time.sleep(2)
        button = driver.find_element(By.XPATH, '//*[@id="form_auto"]/div/div/div[2]/div[5]/div/div[1]/button')
        button.click()
        time.sleep(1)
        pageSource = driver.page_source
        soup = BeautifulSoup(pageSource, 'html.parser')
        soup.prettify()
        try:
            carType = soup.find('span', attrs={'x-text': "item['value']"}, string=['A','B','C','D',None]).get_text()
            print(carNumbers[x], carType, sep=' - ')
            if carType == 'A':
                types[0] += 1
                imgDownloading(links, x, carType)
            elif carType == 'B':
                types[1] += 1
                imgDownloading(links, x, carType)
            elif carType == 'C':
                types[2] += 1
                imgDownloading(links, x, carType)
            elif carType == 'D':
                types[3] += 1
                imgDownloading(links, x, carType)
        except:
            carType = soup.find('span', attrs={'x-text': "item['value']"}, string=['A','B','C','D',None])
            print(carNumbers[x], carType, sep=' - ')
            continue

    print(types)
    print('Timeout 10 sec')
    driver.close()
    time.sleep(10)

             
def imgDownloading(links, num, cT):
    image_name = f'{uuid4()}' + '.jpg' #Creating a unique name
    urllib.request.urlretrieve(links[num], path + cT + '/' + image_name) #Saving images
    
    
    
        
nums = 500 
carParsing(nums)
