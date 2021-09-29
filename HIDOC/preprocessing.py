# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import re
from konlpy.tag import Mecab
from konlpy.tag import Kkma
import matplotlib.pyplot as plt


df_origin = pd.read_excel("hidoc_total.xlsx",engine="openpyxl")

#결측치 처리
#Hidoc 옛날 버전에는 Question을 작성하지 않은 것으로 보임.
#목적상 Question이 중요한데, Question이 비어있으면 안되므로 결측치는 나가리 시킨다.
print(len(df_origin))
df=df_origin.dropna(axis=0,subset=['질문']) #dropna 사용 시 na가 있는 행 전체를 날리고 싶으면 axis=0, 열 전체를 날리고 싶으면 axis=1
print(len(df))
df=df.reset_index()

# 형태소 분석을 위한 밑작업
list_title =[]
list_time =[]
list_question=[]
list_answer=[]

for i in range(len(df)):
    list_title.append(df.loc[i,'제목'])
    list_time.append(df.loc[i,'질문 시간'])
    list_question.append(df.loc[i,'질문'])
    list_answer.append(df.loc[i,'답변'])

#형태소 분석
mecab=Mecab()
morphed_text=mecab.pos(list_title[25])
print(morphed_text) #형태소 tag를 통해 발라낼 수 있음을 알게 됨

#불용어 처리
stopwords ='안녕하세요 안녕 강미 노승혜 김태완 김경구 김선동 류혜경 양윤석 김준연 질문자 김산 김덕만 진성준 배영준 김정한 엄태익 김소희 정진욱 이혁준 손영모 최정석 허수영 신재빈 정준호 이지호 배지영 방혜승 이민아 문홍주 권오준 김태한 안영우 조택우 박지원 이완수 최민호 송지홍 유형준 김형석 안지현 최재영 엄태익 유수영 김명석 심수정 김명석 민형근 서정호 강경숙 김양현 이희만 이시헌 김양현 한미애 김희열 김주희 정은아 김윤석 조태환 유승선 황성배 박종원 박선민 이제성 이영미 은종운 한상철 김원용 고완규 최봉수 지식인 조원표 신소애 김시현 이규섭 노태성 양희탁 박창해 김덕환 민형근 전준연 최용진 임헌관 박현주 최호성 김형석 곽진호 김승철 김정욱 박정원 김상석 이완구 이호 김경현 박선민 이승수 손태 정호영 박재만 김동원 이주환 박현철 고대용 김명준 박근준 이승하 강혜진 하이닥 홍재웅 김진용 박근준 윤선영 손민규 박은경 김보연 정재혁 김지운 김관수 최석영 박성우 이동환 이준호 윤희주 최해현 박종호 윤혜진 이호 안희진 김미경 이상욱 이아름 신봉규 정종일 김지연 황은진 정희선 박종호 강은희 김현정 강병훈 김연선 이정은 김게진 권용일 이영미 장현우 조원표 오창선 김종석 조병현 황태현 정창원 최진석 박은진 신광식 황태영 김윤석 손경호 손정민 조윤경 최우석 김정희 한경호 최예진 손일표 최승균 박제혁 네이버 최진석 홍성재 박정민 양수진 상담의 박은기 차상헌 장석원 신재철 정연환 임성륜 오호준 박기정 장재빈 김신아 박기정 박정원 이승화 정현주 곽민재 한지운 김민한 백동훈 이문우 한지운 이석재 변상권 박나희 한용보 유이화 황상욱 임채연 강희석 노원재 서종호 지은혜 이신 유윤식 한상훈 전계민 양미애 김정선 배범철 박찬덕 이학민 박효경 김미선 최진욱 유석선  배덕호 심상인 서운희 이재성 문경용 조병구 김해성 이영진 이준형 이지한 한상훈 김성준 iN 문근배 장윤주 신봉식 여경아 이윤길 박평식 김영집 김정태 홍인표 김태균 이현철 김현주 하다현 박소정 이경호 신미영 홍원기 유병국 이주연 전혜림 김정호 김상훈 양수진 차상헌 김우영 장수연 변상권 황인섭 이진수 이남호 윤덕경 홍현기 정현주 김태성 조창근 김신아 박동수 박평식 조병구 김경구 김진국 김시헌 안상석 홍주희 김주남 강미지 이형근 박춘식 이우영 송민규 송민근 조현섭 김용진 김덕실 조은석 박기호 박정원 문상현 박관현 조성환 조예성 송호철 강경구 이성윤 김동현 윤창호 김규연 박진미 박희정 강영록 유재돈 김선복 윤홍일 홍승호 최은지 김예진 지은혜 정여화 한지운 김영진 안강석 서정웅 김지은 이성진 강기원 신석우 박효경 안지훈 이재오 유재영 김영준 고지훈 김태형 윤장호 현일식 이학민 엄문용 황규엽 반동규 권유석 강영호 우지희 조혜리 김윤정 윤성원 이희수 박기범 이문우 송미현 이재오 손원진 이영준 박경식 권수범 심형훈 신승령 윤소정 박연경 박웅 양미애 정명주 정재현 박예리 김정선 엄일준 유이화 유지연 신나리 곽민재 강희석 김지우 노원재 남정원 황해연 김찬수 박재형 조윤정 이방훈 한재병 박정인 복상훈 김상진 이수연 김민수 장희석 이지훈 조병주 이경숙 전미연 정규화 임승철 김규현 이정우 서종필 유선경 서민석 배중일 김영집 김정선 김봉현 문정원 김도원 김린애 이원우 박병규 송슬기 김린애 정흥규 김소연 원진 박부경'
stopwords = stopwords.split(' ')
for i in range(len(list_answer)):
    for stopword in stopwords:
        if re.search(stopword,list_answer[i])!=None:
            list_answer[i]=re.sub(stopword,'',list_answer[i])

#Feature Engineering
#명사만 발라낸다 (일반명사: NNG, 고유명사: NNP, 외국어: SL, 시간부사: MAP)
morphed_title_list=[]
morphed_question_list=[]
morphed_answer_list=[]

for i in range(len(list_title)):
    tagged_text=''
    tagged_text_q=''
    tagged_text_a=''
    morphed_title = mecab.pos(list_title[i])
    morphed_question=mecab.pos(str(list_question[i]))
    morphed_answer=mecab.pos(list_answer[i])
    for tag in morphed_title:
        if (tag[1] in ['NNG','MAG', 'NNP','SL'] and len(tag[0]) > 1) or tag[0]=='질':
            feature_text=tag[0]
            tagged_text=tagged_text+feature_text+' '
    morphed_title_list.append(tagged_text) #모든 tagged text가 다 append되는 것에 대한 문제 해결 필요
    for tag_q in morphed_question:
        if (tag_q[1] in ['NNG','MAG', 'NNP','SL'] and len(tag[0]) > 1) or tag_q[0]=='질':
            feature_text_q =tag_q[0]
            tagged_text_q = tagged_text_q+feature_text_q+' '
    morphed_question_list.append(tagged_text_q)
    for tag_a in morphed_answer:
        if (tag_a[1] in ['NNG','MAG', 'NNP','SL'] and len(tag_a[0]) > 1) or tag_a[0]=='질':
            feature_text_a=tag_a[0]
            tagged_text_a=tagged_text_a+feature_text_a+' '
    morphed_answer_list.append(tagged_text_a)

example = pd.DataFrame(data=list(zip(morphed_title_list,morphed_question_list,morphed_answer_list)),columns=['title','question','answer'])
example.to_excel('example.xlsx')

#One-hot vector
title_split_list=[]
question_split_list=[]
answer_split_list=[]
for title_morphed in morphed_title_list:
    title_morphed=title_morphed.split(' ')
    for word in title_morphed:
        title_split_list.append(word)
title_split_list=list(set(title_split_list))
title_split_list=title_split_list[1:]
#Question
for question_morphed in morphed_question_list:
    question_morphed=question_morphed.split(' ')
    for q in question_morphed:
        question_split_list.append(q)
question_split_list=list(set(question_split_list))
question_split_list=question_split_list[1:]
#Answer
for answer_morphed in morphed_answer_list:
    answer_morphed=answer_morphed.split(' ')
    for a in answer_morphed:
        answer_split_list.append(a)
answer_split_list=list(set(answer_split_list))
answer_split_list=answer_split_list[1:]

#bucket = np.zeros(len(title_split_list),dtype=np.float)
#for title in title_split_list:
#    bucket_temp=bucket.copy()
#    np.out(bucket_temp,title_split_list.index(title),1)
#    print(bucket_temp)

from gensim.models import word2vec
morphed_total_list=morphed_title_list+morphed_question_list+morphed_answer_list
total_split_list=title_split_list+question_split_list+answer_split_list

def tokenize(doc):
    new_list = str(doc).split()
    return new_list
data = [tokenize(d) for d in morphed_total_list]
print(data)
# 문장을 이용하여 단어와 벡터를 생성한다.
#size=M size, window=중심단어+주변단어 갯수, 단어가 최소 한 번 이상 반복되는 것들만 고려하겠다.
size=len(total_split_list)
model = word2vec.Word2Vec(data,size=len(data),window=2,min_count=1)
#model.build_vocab(morphed_title_list) # trainset을 넣는
model.train(morphed_total_list, epochs=model.iter, total_examples=model.corpus_count)

print("model check: {0}".format(model))
model.save("hidoc.model")

#단어 벡터를 구함
word_vectors= model.wv
#모든 단어 벡터를 한방에 출력해보기 위해 vocab의 key정렬
vocabs = word_vectors.vocab.keys()
print(vocabs)
word_vectors_list=[word_vectors[v] for v in vocabs]

result_sim=model.wv.most_similar(positive=tokenize('생리 예정일'),negative='',topn=10)
#[('시간', 0.9999356269836426), ('야즈', 0.9999312162399292), ('장기', 0.99992835521698), ('응급', 0.9999250769615173), ('주기', 0.9999090433120728)]
result_sim2=model.most_similar(positive=tokenize('여자 아내'),negative=tokenize('남자'),topn=10)
#result_sim3=model.most_similar(u'질문')
print(result_sim)
print(result_sim2)

model.load()
