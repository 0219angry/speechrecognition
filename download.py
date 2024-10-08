import requests
from bs4 import BeautifulSoup

def download(number):
  url = 'https://aozoraroudoku.jp/voice/'

  url_data = requests.get(url+'mp3/rd'+number+'.mp3').content

  with open('data/mp3/rd'+number+'.mp3',mode='wb') as f:
    f.write(url_data)
    
  html_data = requests.get(url+'rdp/rd'+number+'.html')
  html_data.encoding = html_data.apparent_encoding
  soup = BeautifulSoup(html_data.text, 'html.parser')

  title = soup.title.string
  print("Download file from \""+title+"\"")
  
