import speech_recognition as sr
import pyaudio
from pydub import AudioSegment
from pydub.utils import make_chunks
import datetime

dir = "data/wav/"
filenames = ["rd1150"]

sprec = sr.Recognizer()

for filename in filenames:
  print(f"[{datetime.datetime.now()}] {dir}{filename} ========\n")
  with sr.AudioFile(dir+filename+".wav") as source:
    audio = sprec.record(source)
  script = sprec.recognize_google(audio, language='ja-JP')
  
  with open("data/txt/"+filename+".txt",'w') as f:
    f.write(script)
  print(script)
