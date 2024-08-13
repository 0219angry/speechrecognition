import requests
from bs4 import BeautifulSoup

# 無視する文字の一覧
ignore_letters =  ["。","、","\n","\t","\r"," ","　","○","「","」","（","）","-","―","！","!","？","?"]



def calc_accuracy(number, ans, rec, engine_name):
  N = len(ans) # 正解文の長さ
  delection_error = 0 # 削除誤り
  substitution_error = 0 # 置換誤り
  insertion_error = 0 # 挿入誤り
  
  c_ans = 0 # 正解文内の現在地
  c_rec = 0 # 認識文内の現在地
  error_encount = False # true: 現在エラーの処理中
  error_encount_ans = None # 直近の誤り発生地点(正解文)
  error_encount_rec = None # 直近の誤り発生地点(認識文)
  
  great_c_ans_result = 0 # 現在最良の一致した地点(正解文)
  great_c_rec_result = 0 # 現在最良の一致した地点(認識文)
  
  f = open("data/acc/"+"rd"+number+"_"+engine_name+".csv",'w')
  f.write("error_type, answer, recognized, error_count, answer_start, answer_end, recog_start, recog_end\n")
  
  # 最小の誤り数でとれるものを採用する(そうしないと同じ文字があった時不適切な文字同士を同じものとみなす可能性がある)
  while c_ans < N:
    if error_encount == True:
      error_letter_count = 100000
      while c_ans < len(ans):
        while c_rec < len(rec):
          if ans[c_ans] == rec[c_rec] and error_letter_count > max(c_rec-error_encount_rec, c_ans-error_encount_ans)-1:
            error_letter_count = max(c_rec-error_encount_rec, c_ans-error_encount_ans)-1
            great_c_ans_result = c_ans
            great_c_rec_result = c_rec
            break
          c_rec += 1
        c_rec = error_encount_rec
        c_ans += 1
      if great_c_rec_result == error_encount_rec: # 削除誤り
        delection_error += error_letter_count
        f.write("delection, ")
      elif great_c_ans_result == error_encount_ans: # 挿入誤り
        f.write("insertion, ")
        insertion_error += error_letter_count
      else: # 置換誤り
        f.write("substitution, ")
        substitution_error += error_letter_count
      
      # 誤り内容をcsvに書き込み
      f.write(f"{''.join(ans[error_encount_ans:great_c_ans_result])}, {''.join(rec[error_encount_rec:great_c_rec_result])}, ")
      f.write(f"{error_letter_count}, {error_encount_ans}, {great_c_ans_result-1}, {error_encount_rec}, {great_c_rec_result-1}\n")
      c_ans = great_c_ans_result
      c_rec = great_c_rec_result
      error_encount = False


    
    # 正解文の終端に来たのに認識文が残っているときは挿入誤り    
    if c_ans == len(ans):
      i = len(rec)-c_rec-1
      insertion_error += i
      break
    
    # 認識文の終端に来たのに正解文が残っているときは削除誤り
    if c_rec == len(rec):
      d = len(ans)-c_ans-1
      delection_error += d
      break
      
    # 誤りに遭遇した
    if ans[c_ans] != rec[c_rec] and error_encount == False:
      # 正解していた部分をcsvに書き込み
      f.write(f"correct, {''.join(ans[great_c_ans_result:c_ans])}, {''.join(rec[great_c_rec_result:c_rec])}, ")
      f.write(f"0, {great_c_ans_result}, {c_ans-1}, {great_c_rec_result}, {c_rec-1}\n")
      error_encount = True
      error_encount_ans = c_ans
      error_encount_rec = c_rec
      continue
    
    if ans[c_ans] == rec[c_rec]:
      c_ans += 1
      c_rec += 1
      
  f.write(f"correct, {''.join(ans[great_c_ans_result:c_ans])}, {''.join(rec[great_c_rec_result:c_rec])}, ")
  f.write(f"0, {great_c_ans_result}, {c_ans-1}, {great_c_rec_result}, {c_rec-1}\n")
  
  f.close()
  print(f"全文字数: {N}")
  print(f"削除誤り: {delection_error}")
  print(f"置換誤り: {substitution_error}")    
  print(f"挿入誤り: {insertion_error}")
  print(f"accuracy: {(N-delection_error-substitution_error-insertion_error)/N} %")
  return (N-delection_error-substitution_error-insertion_error)/N
  


def accuracy(number, url,engine_name):
  
  response = requests.get(url)
  
  response.encoding = response.apparent_encoding
  
  soup = BeautifulSoup(response.text, 'html.parser')
  
  main_text = soup.find('div', class_='main_text')
  
  answer_text = main_text.get_text()
  
  with open("data/answer/rd"+number+"_"+engine_name+".txt","w") as f:
    f.write(answer_text)
  
  with open("data/txt/"+"rd"+number+"_"+engine_name+".txt",'r') as f:
    recognized_text = f.read()
    
  formatted_answer = []
  
  for l in answer_text:
    if l not in ignore_letters:
      print(l,end="")
      formatted_answer.append(l)
      

  print()
  
  formatted_recog_text = []
  
  for l in recognized_text:
    if l not in ignore_letters:
      print(l,end="")
      formatted_recog_text.append(l)
  print()
  
  calc_accuracy(number, formatted_answer, formatted_recog_text, engine_name)