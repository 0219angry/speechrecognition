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

      with open("data/txt/"+"rd"+number+"_"+engine_name+".txt",'w') as f:
        f.write(script)
      print(script)
      break
    except sr.RequestError as e:
      print(f"Recognition failed: {e}. Retrying {retries + 1}/{max_retries}...")
      retries += 1
      time.sleep(1)
  
  if retries == max_retries:
    print(f"Failed to recognize after {max_retries} attempts.")

