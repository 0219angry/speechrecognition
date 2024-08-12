import requests
from bs4 import BeautifulSoup

# 無視する文字の一覧
ignore_letters =  ["。","、","\n","\t"," ","　","○","「","」","（","）","-","―","！","!","？","?"]

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
    
  with open("debug.txt",'w') as f:
    f.write(answer_text)
  for l in answer_text:
    if l not in ignore_letters:
      print(l,end="")
    # else:
    #   print(f"[{l}]", end="")
  print("\n")
  
  
  for l in recognized_text:
    if l not in ignore_letters:
      print(l,end="")
  print("\n")
  
    
accuracy()