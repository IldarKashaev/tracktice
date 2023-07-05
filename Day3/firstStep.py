import requests
import os 
from bs4 import BeautifulSoup
from uuid import uuid4
import urllib

path = 'images/'
links = []

try:
    os.mkdir(path) #Making a new folder if it does not exist
except: 
    print("Папка уже существует!")

def carParsing(num):
    session = requests.Session()
    global links
    
    for x in range(num+1): 
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
        
    print('Ссылки на изображения сформированы.')
def imgDownloading(links, count):
    for i in range(count):
        image_name = f'{uuid4()}' + '.jpg' #Creating a unique name
        urllib.request.urlretrieve(links[i], path + image_name) #Saving images
    print('Изображения скачаны.')

nums = int(input('Введите количество изображений для загрузки: ')) 
carParsing(nums // 18)
imgDownloading(links, nums)




