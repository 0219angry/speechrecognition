import speech_recognition as sr
import pyaudio
from pydub import AudioSegment
from pydub.utils import make_chunks
import datetime

dir = "data/wav/"

def recognize(number):
  sprec = sr.Recognizer()

  print(f"[{datetime.datetime.now()}] {dir}rd{number} ========\n")
  with sr.AudioFile(dir+"rd"+number+".wav") as source:
    audio = sprec.record(source)
  script = sprec.recognize_google(audio, language='ja-JP')

  with open("data/txt/"+"rd"+number+".txt",'w') as f:
    f.write(script)
  print(script)

