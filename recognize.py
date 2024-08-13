import speech_recognition as sr
import pyaudio
from pydub import AudioSegment
from pydub.utils import make_chunks
import datetime
import time

dir = "data/wav/"

def recognize(number, engine_name, max_retries=5):
  sprec = sr.Recognizer()
  retries = 0
  while retries < max_retries:
    try:
      print(f"[{datetime.datetime.now()}] {dir}rd{number}.wav ")
      with sr.AudioFile(dir+"rd"+number+".wav") as source:
        audio = sprec.record(source)
      if engine_name == "google":
        script = sprec.recognize_google(audio, language='ja-JP')
      elif engine_name == "azure":
        script = sprec.recognize_azure(audio, language='ja-JP')
      elif engine_name == "tensorflow":
        script = sprec.recognize_tensorflow(audio, language='ja-JP')
      else:
        print("Unsupported Speech Recognition engin/API")

      with open("data/txt/"+"rd"+number+".txt",'w') as f:
        f.write(script)
      print(script)
      break
    except sr.RequestError as e:
      print(f"Recognition failed: {e}. Retrying {retries + 1}/{max_retries}...")
      retries += 1
      time.sleep(1)
  
  if retries == max_retries:
    print(f"Failed to recognize after {max_retries} attempts.")

