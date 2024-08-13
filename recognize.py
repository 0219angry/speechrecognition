import speech_recognition as sr
import pyaudio
from pydub import AudioSegment
from pydub.utils import make_chunks
import datetime
import time

dir = "data/wav/"

def recognize(number, max_retries=5):
  sprec = sr.Recognizer()
  retries = 0
  while retries < max_retries:
    try:
      print(f"[{datetime.datetime.now()}] {dir}rd{number}.wav ")
      with sr.AudioFile(dir+"rd"+number+".wav") as source:
        audio = sprec.record(source)
      script = sprec.recognize_google(audio, language='ja-JP')
      while True:
        print("How many letters are in the title and author? count space one letter")
        print(script[0:30])
        main_text_start = int(input())
        print(f"main text =>{script[main_text_start:main_text_start+20]}")
        print("OK? [Y/n]")
        ok = input()
        if ok == "Y" or ok == "y":
          break
      

      with open("data/txt/"+"rd"+number+".txt",'w') as f:
        f.write(script[main_text_start:])
      break
    except sr.RequestError as e:
      print(f"Recognition failed: {e}. Retrying {retries + 1}/{max_retries}...")
      retries += 1
      time.sleep(1)
  
  if retries == max_retries:
    print(f"Failed to recognize after {max_retries} attempts.")

