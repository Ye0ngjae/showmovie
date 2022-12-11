import requests 
import urllib.request
from bs4 import BeautifulSoup
import time
import os
from lxml import etree

url = 'https://movie.naver.com/'

def get_num(link):
    num = link.split('=')[1]
    save_img(num)
    
    return num

def save_img(num):
    img_url = url+'movie/bi/mi/photoViewPopup.naver?movieCode='+str(num)
    print(img_url)
    res = requests.get(img_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    img = soup.find('img')
    img_src = img['src']
    urllib.request.urlretrieve(img_src, 'static/img/'+str(num)+'.jpg')

def get_title(num):
    movie_url = url+'movie/bi/mi/photoViewPopup.naver?movieCode='+str(num)
    res = requests.get(movie_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    name = soup.find('img')
    title = name['alt']

    return title
    
def get_movie_info(num):
    movie_url = url+'movie/bi/mi/basic.naver?code='+str(num)
    res = requests.get(movie_url)
    
    soup = BeautifulSoup(res.content, 'html.parser')
    dom = etree.HTML(str(soup))

    info = soup.find('div', class_='story_area')
    info = soup.find('p', class_='con_tx')

    return str(info).replace('<br/>', '\n').replace('<p class="con_tx">', '').replace('</p>', '')
   
def get_movie_stat(num):
    movie_url  = url+'movie/bi/mi/basic.naver?code='+str(num)
    res = requests.get(movie_url)
    
    soup = BeautifulSoup(res.content, 'html.parser')
    dom = etree.HTML(str(soup))
    
    info = soup.find('dl', class_='info_spec')
    info = info.findAll('span')
    
    return str(info[3].text).replace('\n', '').replace(' ', '')
