import glob
import pydub
import pathlib
import os

mp3_files = glob.glob('data/mp3/*.mp3')
wav_files = glob.glob('data/wav/*.wav')
  
for mp3_file in mp3_files:
  filename = os.path.basename(mp3_file)
  if "data/wav/"+filename[:-4]+".wav" not in wav_files:
    print(f"CONVERT {filename[:-4]}.mp3 ===> {filename[:-4]}.wav")
    sound = pydub.AudioSegment.from_mp3(mp3_file)
    sound.export("data/wav/"+filename[:-4]+".wav", format="wav")
    
    