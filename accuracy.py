import requests
from bs4 import BeautifulSoup

def accuracy():
  print("Enter 青空朗読 contents number (#### in aozoraroudoku.jp/voice/rdp/rd####.html)")
  number = input()
  print("Enter 青空文庫 contents url")
  url = input()
  
  response = requests.get(url)
  
  response.encoding = response.apparent_encoding
  
  soup = BeautifulSoup(response.text, 'html.parser')
  
  main_text = soup.find('div', class_='main_text')
  
  answer_text = main_text.get_text()
  
  with open("data/txt/"+"rd"+number+".txt",'r') as f:
    recognized_text = f.read()
    
  print(answer_text)
  print(recognized_text)
    
accuracy()