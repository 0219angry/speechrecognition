<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
<script type="text/x-mathjax-config">
 MathJax.Hub.Config({
 tex2jax: {
 inlineMath: [['$', '$'] ],
 displayMath: [ ['$$','$$'], ["\\[","\\]"] ]
 }
 });
</script>

# 音声認識APIの精度テスト
青空朗読に掲載されている朗読をGoogle Speech Recognitionで音声認識し、青空文庫にある原文と比較することで認識精度をテストする([ソースコード](https://github.com/0219angry/speechrecognition))。

## 音声認識における誤りのパターン
### 削除誤り$D$ (Delection Error)
  本来必要な文字が欠落しているとき、削除誤りとして数える。欠落した文字数が誤り数となる。例えば、「こんにちは」が「こにちは」と認識されたとき、$D=1$である。

### 置換誤り$S$ (Subsutitution Error)
  本来の文字が別の文字で置き換えられているとき置換誤りとして数える。置換元と置換先の文字数でより多いほうが誤り数となる。例えば「おはようございます」が「おつかれさまです」と認識されたとき、$S=7$である。

### 挿入誤り$I$ (Insertion Error)
  本来の文字以外の文字が認識された文に挿入されていたとき、挿入誤りとして数える。例えば、「こんにちは」が「こんにちにちは」と認識されたとき、$I=2$である。

## 認識精度
ここで正解の文章の文字数を$N$としたとき、認識精度$\alpha$は以下の式で与えられる。

$$\alpha = \frac{N-D-S-I}{N}$$

本スクリプトではこの認識精度を計算する。

## 開発環境
- Ubuntu-22.04 on WSL2
- Python 3.10.12



## 使用方法
必要なライブラリをインストールする。
```
$ pip install -r requirement.txt
```
なお、pyaudioはffmpegに依存している。
``` Ubuntu
$ sudo apt-get install ffmpeg
```
上手くインストールできない場合は上の操作をする必要がある。
スクリプトの実行は次のように行う。
```
$ python3 main.py
Enter 青空朗読 contents number (#### in aozoraroudoku.jp/voice/rdp/rd####.html)
056
Enter 青空文庫 contents url
https://www.aozora.gr.jp/cards/000067/files/509_21645.html
Do you want short mode? Short mode only calculate accuracy. [Y/n]
n
Download file from "喫茶店にて | 青空朗読"
CONVERT rd056.mp3 ===> rd056.wav
[2024-08-13 15:09:38.866703] data/wav/rd056.wav 
How many letters are in the title and author? count space one letter
萩原朔太郎作 喫茶店にて先日 大阪の知人が訪ねてきたので銀座
12
main text =>先日 大阪の知人が訪ねてきたので銀座の相
OK? [Y/n]
y

全文字数: 822
削除誤り: 0
置換誤り: 53
挿入誤り: 0
accuracy: 93.55231143552312 %
finish
```
青空朗読の朗読番号、青空文庫の該当作品のURLを指定する。
モードの選択では、Short modeを選択したとき、すでに実行済みの音声認識結果を参照し、認識精度の計算のみを行う。

また、朗読音声には作者氏名と作品名の読み上げがあるので表示された最初の文章を確認し、その部分を取り除く必要がある。

## 出力ファイル
dataディレクトリ内に以下のファイルが作成される。

|ディレクトリ名|拡張子|内容|
|----|----|----|
|mp3|.mp3|青空朗読からダウンロードした音声ファイル|
|wav|.wav|処理のために変換されたwavファイル(内容はmp3ファイルと同一)|
|answer|.txt|青空文庫から取得した原文|
|txt|.txt|音声認識で出力された認識文|
|acc|.csv|認識精度計算時の処理ファイル|

accディレクトリにあるcsvファイルにすべての文章の解析結果が保存されているので、変換ミスなどを誤りから除去する場合は出力されたcsvファイルを集計することで対応できる。

本スクリプトで計算される認識精度は変換ミスや歴史的仮名遣いなどの違いもすべて誤りとして計測していることに注意する必要がある。

## 結果
「萩原朔太郎作 喫茶店にて」の認識精度は93.6%であった。

|||
|----|----|
|全文字数|822|
|削除誤り|0|
|置換誤り|53|
|挿入誤り|0|

比較用のcsvファイルはresultにある。
