import pandas as pd
from konlpy.tag import Mecab
from konlpy.tag import Kkma


# 데이터 전처리
excel = pd.read_excel(
    "/Users/taehopark/PycharmProjects/dalchaebi/Scrapping/HIDOC/hidoc(page2623~3623).xlsx",engine='openpyxl')
df = pd.DataFrame(excel)
tokenizer = Mecab()
kkma =Kkma()
title_list =[]
answer_list =[]
question_list=[]
# 종결 어미 replace로 없애기
for i in range(len(df)):
    df['제목'][i] = str(df['제목'][i]).replace(
        '.', '').replace('!', '').replace('?', '').replace(',', '')
    df['답변'][i] = df['답변'][i].replace(
        '.', '').replace('!', '').replace('?', '').replace(',', '')
    df['질문'][i] = str(df['질문'][i]).replace(
        '.', '').replace('!', '').replace('?', '').replace(',', '')
    # 토큰화
#    title_list.append(tokenizer.morphs(df['제목'][i])) #형태소를 단어와, 은/는/이/가와 함께 쪼개는 것
    title_list.append(kkma.nouns(df['제목'][i]))
    answer_list.append(kkma.nouns(df['답변'][i]))
    question_list.append(kkma.nouns(df['질문'][i]))

print(title_list)
print(answer_list)
print(question_list)

#m = Mecab()
#print(m.pos(df['답변'][0])) :pos로 되는지 확인
#print(type(m.pos(df['답변'][0]))) : List

# 띄어쓰기로 토큰화하기
