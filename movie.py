import requests 
from bs4 import BeautifulSoup
import time

url = 'https://movie.naver.com/'

r = requests.get(url).text
