from keras.models import Model
from keras.layers import Dense,Input, LSTM
from keras.preprocessing.sequence import pad_sequences
import pandas as pd
import numpy as np
from keras.utils import to_categorical
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

example = pd.read_excel('example.xlsx',engine="openpyxl")

#1) Title & Answer
example = example.dropna(axis=0,subset=['title'])
example=example.reset_index()
del example['question']
example = example.loc[:,'title':'answer']
example = example[0:5999]
print(1)

#print(len(example)) #20081개에서 19865개로 줄었음

#sos와 eos를 우리 타겟인 answer에 입력해야 함
#string화 함
for i in range(len(example)):
    example.loc[i,'title'] = str(example.loc[i,'title'])
    example.loc[i,'answer'] = str(example.loc[i,'answer'])

example.answer = example.answer.apply(lambda x: '\t '+x+' \n')
print(2)
#글자 집합 구축 -> 글자를 토대로 벡터화하려고 함

title_vocab = set()
for line in example.title: #한줄씩 보기
    for char in line: #한 글자씩 보기
        title_vocab.add(char)

answer_vocab = set()
for line in example.answer:
    for char in line:
        answer_vocab.add(char)

#글자 집합의 크기

title_vocab_size = len(title_vocab)+1
answer_vocab_size = len(answer_vocab)+1

title_vocab = sorted(list(title_vocab))
answer_vocab = sorted(list(answer_vocab))

#print(title_vocab_size) #733
#print(answer_vocab_size) #1016

title_to_idx = dict([(word, i+1) for i,word in enumerate(title_vocab)])
answer_to_idx = dict([(word, i+1) for i, word in enumerate(answer_vocab)])
print(3)
#훈련 데이터를 정수 인코딩한다
encoder_input = []
for line in example.title:
    temp_X =[]
    for w in line: #각 줄에서 1개씩 글자를 읽음
        temp_X.append(title_to_idx[w])
    encoder_input.append(temp_X)
#print(encoder_input[:5]) #제대로 잘 됨

decoder_input =[]
for line in example.answer:
    temp_X =[]
    for w in line:
        temp_X.append(answer_to_idx[w])
    decoder_input.append(temp_X)

decoder_target =[]
for line in example.answer:
    t =0
    temp_X=[]
    for w in line:
        if t>0:
            temp_X.append(answer_to_idx[w])
        t=t+1
    decoder_target.append(temp_X)
#print(decoder_target[:5]) #제대로 잘 됨
print(4)
max_title_len = max([len(line) for line in example.title])
max_answer_len = max([len(line) for line in example.answer])
print(max_title_len) # 58
print(max_answer_len) #4664

#Padding 작업: Title의 길이는 전부 58, Answer의 길이는 전부 4664
encoder_input = pad_sequences(encoder_input, maxlen=max_title_len, padding='post')
decoder_input = pad_sequences(decoder_input, maxlen=max_answer_len, padding='post')
decoder_target = pad_sequences(decoder_target, maxlen=max_answer_len, padding='post')
print(5)
#원-핫 인코딩요 *전처리 완료
encoder_input = to_categorical(encoder_input)
decoder_input = to_categorical(decoder_input)
decoder_target = to_categorical(decoder_target)
print(6)
#Seq2seq 모델을 설계: 교사 강요
#입력 시퀀스의 정의와 처리
encoder_inputs = Input(shape=(None, title_vocab_size))
encoder_lstm =LSTM(units = 256,return_state=True) #hidden state 활성화
encoder_outputs, state_h, state_c = encoder_lstm(encoder_inputs)
encoder_states = [state_h,state_c]
#state_h는 hidden state, state_c는 cell 상태
#encoder_states가 바로 컨텍스트 벡터임 (디코더로 전달하는)

decoder_inputs = Input(shape=(None, answer_vocab_size))
decoder_lstm = LSTM(units=256,return_state=True, return_sequences=True)
decoder_outputs, _, _,=decoder_lstm(decoder_inputs, initial_state=encoder_states) #디코더의 첫 상태를 인코더의 은닉 상태, 셀 상태로 한다
decoder_softmax_layer = Dense(answer_vocab_size, activation = 'softmax')
decoder_outputs = decoder_softmax_layer(decoder_outputs)

model=Model([encoder_inputs,decoder_inputs],decoder_outputs)
model.compile(optimizer="rmsprop", loss='categorical_crossentropy')

model.fit(x=[encoder_input, decoder_input],y=decoder_target, batch_size=64, epochs=20, validation_split=0.2)
print(7)
#모델을 조정하고 동작시키는 방법
model.save("seq2seq_train.model")

encoder_model = Model(inputs=encoder_inputs,outputs= encoder_states)

#이전 시점의 상태들을 저장하는 텐서
decoder_state_input_h = Input(shape=(256,))
decoder_state_input_c = Input(shape=(256,))
decoder_states_inputs = [decoder_state_input_h,decoder_state_input_c]
decoder_outputs, state_h, state_c= decoder_lstm(decoder_inputs, initial_state=decoder_states_inputs)
#문장의 다음 단어를 예측하기 위해 초기 상태를 이전 시점의 상태로 사용. 이는 뒤의 함수 decode sequence에 구현

decoder_states = [state_h,state_c]
#훈련 과정과 달리 LSTM의 리턴하는 은닉 셀 상태와 셀 상태인 state_c와 state_h를 버리지 않음
decoder_outputs = decoder_softmax_layer(decoder_outputs)
decoder_model = Model(inputs=[decoder_inputs]+ decoder_states_inputs, outputs=[decoder_outputs]+decoder_states)

index_to_title = dict((i,char) for char, i in title_to_idx.items())
index_to_answer = dict((i,char) for char, i in answer_to_idx.items())
print(8)
def decode_sequence(input_seq):
    # 입력으로부터 인코더의 상태를 얻음
    states_value = encoder_model.predict(input_seq)

    # <SOS>에 해당하는 원-핫 벡터 생성
    target_seq = np.zeros((1, 1, answer_vocab_size))
    target_seq[0, 0, answer_to_idx['\t']] = 1.

    stop_condition = False
    decoded_sentence = ""

    # stop_condition이 True가 될 때까지 루프 반복
    while not stop_condition:
        # 이점 시점의 상태 states_value를 현 시점의 초기 상태로 사용
        output_tokens, h, c = decoder_model.predict([target_seq] + states_value)

        # 예측 결과를 문자로 변환
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = index_to_answer[sampled_token_index]

        # 현재 시점의 예측 문자를 예측 문장에 추가
        decoded_sentence += sampled_char

        # <eos>에 도달하거나 최대 길이를 넘으면 중단.
        if (sampled_char == '\n' or
           len(decoded_sentence) > max_answer_len):
            stop_condition = True

        # 현재 시점의 예측 결과를 다음 시점의 입력으로 사용하기 위해 저장
        target_seq = np.zeros((1, 1, answer_vocab_size))
        target_seq[0, 0, sampled_token_index] = 1.

        # 현재 시점의 상태를 다음 시점의 상태로 사용하기 위해 저장
        states_value = [h, c]

    return decoded_sentence


for seq_index in [3,50,100,300,1001]:
    input_seq = encoder_input[seq_index: seq_index+1]
    decoded_sentence = decode_sequence(input_seq)
    print(35*"-")
    print('입력 문장: ', example.title[seq_index])
    print('정답 문장: ', example.answer[seq_index][1:len(example.answer[seq_index])-1]) # '\t'와 '\n'을 빼고 출력
    print('예측 문장:', decoded_sentence[:len(decoded_sentence) - 1])  # '\n'을 빼고 출력
model.save("seq2seq_test.model")