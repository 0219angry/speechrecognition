import requests
from bs4 import BeautifulSoup

# 無視する文字の一覧
ignore_letters =  ["。","、","\n","\t","\r"," ","　","○","「","」","（","）","-","―","！","!","？","?"]



def calc_accuracy(number, ans, rec):
  N = len(ans) # 正解文の長さ
  delection_error = 0 # 削除誤り
  substitution_error = 0 # 置換誤り
  insertion_error = 0 # 挿入誤り
  
  c_ans = 0 # 正解文内の現在地
  c_rec = 0 # 認識文内の現在地
  error_encount = False # true: 現在エラーの処理中
  error_encount_ans = None # 直近の誤り発生地点(正解文)
  error_encount_rec = None # 直近の誤り発生地点(認識文)
  
  f = open("data/acc/"+"rd"+number+".csv",'w')
  f.write("type, answer, recognized, anser_pos, recognized_pos\n")
  
  while c_ans < N:
    if error_encount == True:
      # 正解文を進める(削除誤り)
      while c_ans < len(ans) and ans[c_ans] != rec[c_rec]:
        # print(f"<D>[{ans[c_ans]}] <=> [{rec[c_rec]}] {c_ans}|{c_rec}")
        f.write(f"Delection, {ans[c_ans]}, {rec[c_rec]}, {c_ans}, {c_rec}\n")
        c_ans += 1
        
      d = c_ans - error_encount_ans
      c_ans = error_encount_ans
      
      # 認識文を進める(挿入誤り)
      while c_rec < len(rec) and ans[c_ans] != rec[c_rec]:
        # print(f"<I>[{ans[c_ans]}] <=> [{rec[c_rec]}] {c_ans}|{c_rec}")
        f.write(f"Insertion, {ans[c_ans]}, {rec[c_rec]}, {c_ans}, {c_rec}\n")
        c_rec += 1
        
      i = c_rec - error_encount_rec
      c_rec = error_encount_rec
      
      # どちらも進める(置換誤り)
      while c_rec < len(rec) and c_ans < len(ans) and ans[c_ans] != rec[c_rec]:
        # print(f"<S>[{ans[c_ans]}] <=> [{rec[c_rec]}] {c_ans}|{c_rec}")
        f.write(f"Substitution, {ans[c_ans]}, {rec[c_rec]}, {c_ans}, {c_rec}\n")
        c_rec += 1
        c_ans += 1
      s = c_rec - error_encount_rec
      c_rec = error_encount_rec
      c_ans = error_encount_ans
      
      # 値が小さいほうを採用する
      if i <= d and i <= s: # 挿入誤り 
        insertion_error += i
        c_rec = c_rec + i
        error_encount = False
        # print(f"insertion error detected: {i} letter(s).")
        
      elif d <= i and d <= s: # 削除誤り
        delection_error += d
        c_ans = c_ans + d
        error_encount = False
        # print(f"delection error detected: {d} letter(s).")
        
      else: # 置換誤り
        substitution_error += s
        c_ans = c_ans + s
        c_rec = c_rec + s
        error_encount = False
        # print(f"substitution error detected: {s} letter(s).")
    
    # 正解文の終端に来たのに認識文が残っているときは挿入誤り    
    if c_ans == len(ans):
      i = len(rec)-c_rec-1
      insertion_error += i
      # print(f"insertion error detected: {i} letter(s).")
      break
    
    # 認識文の終端に来たのに正解文が残っているときは削除誤り
    if c_rec == len(rec):
      d = len(ans)-c_ans-1
      delection_error += d
      # print(f"delection error detected: {d} letter(s).")
      break
      
        
    if ans[c_ans] != rec[c_rec] and error_encount == False:
      print(f"<E>[{ans[c_ans]}] <=> [{rec[c_rec]}] {c_ans}|{c_rec}")
      f.write(f"Error, {ans[c_ans]}, {rec[c_rec]}, {c_ans}, {c_rec}\n")
      error_encount = True
      error_encount_ans = c_ans
      error_encount_rec = c_rec
      continue
    
    if ans[c_ans] == rec[c_rec]:
      # print(f"<C>[{ans[c_ans]}] <=> [{rec[c_rec]}] {c_ans}|{c_rec}")
      f.write(f"Correct, {ans[c_ans]}, {rec[c_rec]}, {c_ans}, {c_rec}\n")
      c_ans += 1
      c_rec += 1
  
  
  f.close()
  print(f"全文字数: {N}")
  print(f"削除誤り: {delection_error}")
  print(f"置換誤り: {substitution_error}")    
  print(f"挿入誤り: {insertion_error}")
  print(f"accuracy: {(N-delection_error-substitution_error-insertion_error)/N} %")
  return (N-delection_error-substitution_error-insertion_error)/N
  


def accuracy(number, url):
  
  response = requests.get(url)
  
  response.encoding = response.apparent_encoding
  
  soup = BeautifulSoup(response.text, 'html.parser')
  
  main_text = soup.find('div', class_='main_text')
  
  answer_text = main_text.get_text()
  
  with open("data/answer/rd"+number+".txt","w") as f:
    f.write(answer_text)
  
  with open("data/txt/"+"rd"+number+".txt",'r') as f:
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
  
  calc_accuracy(number, formatted_answer, formatted_recog_text)