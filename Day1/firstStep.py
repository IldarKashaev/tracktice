import requests
import sys
from PIL import Image
from io import BytesIO
import os 

try:
    os.mkdir("images") #Создаем папку и проверяем ее на существование
except: 
    print("Папка уже существует!")

num = int(input('Введите количество страниц для парсинга: '))
if num < 1:
    sys.exit('Число меньше 1')
session = requests.Session()
for x in range(num): 
    payload = {'start': str(x*18)}
    r = session.get('https://migalki.net/images.php', params=payload) #Подключаемся к сайту
    d, f, k = [], [], []
    t = r.text.splitlines() #Переводим GET-запрос в массив из строк
    for i in range(len(t)):
        m = t[i].strip().startswith("<img") #Избавляемся от лишних пробелов и делаем поиск по строкам с "<img"
        if m:
            d.append(t[i].strip()) #Сохраняем их в массив
    
    for i in range(len(d)):
        l = d[i].split() #Разделяем строку на массив
        f.append(l[1]) #Оставляем нужную нам часть
    
    for i in range(len(f)):
        m = list(f[i]) #Превращаем опять в массив из символов
        k.append(''.join(m[5:-1])) #Срезаем лишнее (src=" и ")
        c = requests.get(k[i].replace('300', '1000')) #Получаем изображение
        img = Image.open(BytesIO(c.content)) #Открываем изображение
        filename = 'images/' + str(i + 18*x) + '.jpg'
        img = img.save(filename) #Сохраняем изображение

