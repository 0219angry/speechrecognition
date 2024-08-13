from init import init
from download import download
from convert import convert_one
from recognize import recognize
from accuracy import accuracy


def main():
  # 必要情報の要求
  print("Enter 青空朗読 contents number (#### in aozoraroudoku.jp/voice/rdp/rd####.html)")
  number = input()
  print("Enter 青空文庫 contents url")
  url = input()
  
  
  # 必要なディレクトリの作成
  init()
  
  if short_mode == "n" or short_mode == "N":
    # 音声ファイルのダウンロード
    download(number)

    # mp3->wav変換
    convert_one(number)

    # 音声認識(Google API)
    recognize(number)
  
  if short_mode == "n" or short_mode == "N" or short_mode == "y" or short_mode == "Y":
    # 認識精度の計算
    accuracy(number, url, engine_name)
  
  print("finish")


if __name__ == "__main__":
    main()

