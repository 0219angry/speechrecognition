import os

def init():
  try:
    os.makedirs("data/wav")
  except FileExistsError:
    pass
  try:
    os.makedirs("data/mp3")
  except FileExistsError:
    pass
  try:
    os.makedirs("data/txt")
  except FileExistsError:
    pass
  try:
    os.makedirs("data/acc")
  except FileExistsError:
    pass
  try:
    os.makedirs("data/answer")
  except FileExistsError:
    pass
    
init()