import pandas as pd
import numpy as np

excel1 = pd.read_excel("/Users/taehopark/PycharmProjects/dalchaebi/Scrapping/HIDOC/stopwords (2623~3623).xlsx",engine='openpyxl')
excel2 = pd.read_excel("/Users/taehopark/PycharmProjects/dalchaebi/Scrapping/HIDOC/stopwords (1640~2139).xlsx",engine='openpyxl')
excel3 = pd.read_excel("/Users/taehopark/PycharmProjects/dalchaebi/Scrapping/HIDOC/stopwords (1640~2139).xlsx",engine='openpyxl')

#데이터프레임화
df1 = pd.DataFrame(excel1)
df2 = pd.DataFrame(excel2)
df3 = pd.DataFrame(excel3)

df_combined = pd.concat([df1,df2,df3],axis=0,ignore_index=True)
df_combined = df_combined.drop(columns=['Unnamed: 0'])
df_combined.to_excel("test.xlsx")

#딕셔너리를 만든다

dics = {}
title_list =[]
question_list =[]
answer_list =[]

for i in range(len(df_combined)):
    title_raw = df_combined['제목'][i].replace("'","").replace("[","").replace("]","").split(',')
    question_raw = df_combined['질문'][i].replace("'", "").replace("[", "").replace("]", "").split(',')
    answer_raw = df_combined['답변'][i].replace("'", "").replace("[", "").replace("]", "").split(',')
    for title in title_raw:
        title_list.append(title)
    for question in question_raw:
        question_list.append(question)
    for answer in answer_raw:
        answer_list.append(answer)

title_list=list(set(title_list))[1:]
question_list=list(set(question_list))[1:]
answer_list=list(set(answer_list))[1:]
# '' 없애기
list_combined = list(set(title_list+question_list+answer_list))
for word in list_combined:
    if word not in dics.keys():
        dics[word] = len(dics)

#원-핫 인코딩 벡터 차원 크기 결정
nb_classes = len(dics)

#원-핫 인코딩 사용하기 위해 리스트 형태로 변환, 이 때 value만 리스트로 변환
targets = list(dics.values())
one_hot_targets = np.eye(nb_classes)[targets]

#BOW
BOW_dics ={}
for word in list_combined:
    if word not in BOW_dics.keys():
        BOW_dics[word] = 0
for i in range(len(df_combined)):
    title_raw_BOW = df_combined['제목'][i].replace("'", "").replace("[", "").replace("]", "").split(',')
    for title in title_raw_BOW:
        if title in dics.keys():
            BOW_dics[title] = BOW_dics[title]+1
print(BOW_dics)



