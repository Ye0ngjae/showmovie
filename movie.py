import requests 
import urllib.request
from bs4 import BeautifulSoup
import time
import os
from lxml import etree 

url = 'https://movie.naver.com/'

def get_num(link): # 영화 번호
    num = link.split('=')[1]
    save_img(num)
    
    return str(num)

def save_img(num): # 영화 포스터
    img_url = url+'movie/bi/mi/photoViewPopup.naver?movieCode='+num

    res = requests.get(img_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    img = soup.find('img')
    img_src = img['src']
    urllib.request.urlretrieve(img_src, 'static/img/movie/'+str(num)+'.jpg') # 이미지 저장

def get_title(num): # 영화 제목
    movie_url = url+'movie/bi/mi/photoViewPopup.naver?movieCode='+num
    res = requests.get(movie_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    name = soup.find('img')
    title = name['alt']

    return title
    
def get_info(num): # 영화 정보
    movie_url = url+'movie/bi/mi/basic.naver?code='+num
    res = requests.get(movie_url)
    
    soup = BeautifulSoup(res.content, 'html.parser')
    dom = etree.HTML(str(soup))

    info = soup.find('div', class_='story_area')
    info = soup.find('p', class_='con_tx')

    return str(info).replace('<br/>', '\n').replace('<p class="con_tx">', '').replace('</p>', '').replace('\xa0','').replace('\n', '').replace('&lt;','').replace('&gt;','').replace('\r','')
   
def get_date(num): # 개봉일
    movie_url  = url+'movie/bi/mi/basic.naver?code='+num
    res = requests.get(movie_url)
    
    soup = BeautifulSoup(res.content, 'html.parser')
    dom = etree.HTML(str(soup))
    
    info = soup.find('dl', class_='info_spec')
    info = info.findAll('span')
    
    return str(info[3].text).replace('\n', '').replace(' ', '').replace('\t', '').replace('\r', '')

#num = get_num(input('url: '))
#print(get_title(num))
#print(get_movie_stat(num))
#print(get_movie_info(num))