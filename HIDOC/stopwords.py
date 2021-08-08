# -*- coding: utf-8 -*-
from nltk.corpus import stopwords
import pandas as pd
from nltk.tokenize import word_tokenize
import nltk

excel = pd.read_excel(
    "/Users/taehopark/PycharmProjects/dalchaebi/Scrapping/HIDOC/token_list.xlsx",engine='openpyxl')
df = pd.DataFrame(excel)
stopwords ="하이 톨 오ㅔ 오느 배중일 이정 박정인 정인 김민수 민수 운동상담 영섭 약사 김현주 하다현 박소정 이경호 이드 홍원기 이원 이원우 대로면 김주희 뿐 전미연 미연 정규화 임승철 봉재 장희석 이지훈 부과 복상훈 소연 정도시 도시 김명 김영진 정찬 김상진 상진 태웅 박현철 이수연 미선 김규연 김영진 박재형 조윤정 이방훈 이방 안강석 뜩 조원표 김정선 김지우 지우 노원재 우석 스테로 내사 액 임도 하나 성우 남정원 윤희 윤희주 봉재 전내용 펜 손민규 윤선영 선영 김정현 권도 황해 황해연 디클 렉  김찬수 찬수 운동상담사 가여 엄일준 강희석 희석 원재 궁의 유이화 이화 장호 김영훈 논 연 유지연 유지 석영 곽 곽민재 국진이 신나리 나리 신승령 이푸 윤소정 소정 박예리 예리 하니 프 종이 박연경 연경 박병규 한재병 한재 박웅 웅 양미 양미애 정명주 명주 응급의학 황상 의학 보신적인 보신 가슴전문 정재현 재현 내분비 내분비내과 이완 엄문용 황규엽 엽 이문 이문우 군 우 상담약사 신승 신승령 송미현 이재오 손원진 이영준 박경식 경식 태환 김태환 권수범 수범 심형훈 창현 영미 이주환 반동규 반동 권유 권유석 강영호 영호 김희 지희 우지희 조혜리 혜 이희수 박기범 기범 김윤 김윤정 윤성원 성원 서정웅 김지은 영양상담사 영양상담 이성진 강기원 기원 김미선 신석우 모하 모하규 박효경 안지 안지훈 원기 부이 임승 요감 이재오 수가 유재영 재영 박재 효경 고지은 지은 김영준 김태 김태형 상담약사 손경호 경호 윤장호 장호 엄문 현일식 일식 이학민 이학 하지 질문날짜 박효경 효경 박성우 김관수 관수 홍승호 승호 소의 윤홍일 홍일 박진미 진미 최은지 즈음 신봉 신봉규 신승 정종일 김예진 예진 김지연 지연 원재 정희 정희선 지지 해지지 지은혜 은혜 김미경 신예지 예지 정여화 여화 불 김지운 지운 한지운 황태영 서정 한 율 서정호 랫 랫쪽 보파 도 정도안 가경 정일 일지 셈말이있엇구 것으 왜냐햇더 수고하세  만큼 쯔 쯔음 하세여 도 그로 요임 요임심 떻 떻ㄱ 뻐 외 탂 부 핫 팩 끊엇구 가가 것같애요소변 인지 모 꼇 습 약주 달간 데얼마 앖 안녕하세쇼 쇼 장과 겸 험이 진것 쑥 크린 안녕하세요해외 땜 제목 가기 님를 선생 제 옥 질문을하엿습니 여ㅜ 안가 교수님제가 교수님 졋고 엘 역 계 것때문 리브 훼 라민 이러스 반쯤 장하 당 릴려 가요아 왓 안녕하세여제 여제 ㅠ학교 보 잇 선생님안녕 ㄷㅔ ㅔ 근대 술 기로 돔 주실 에일 가보 올 있습상담내용 있습 야당 산로 메 콜 플란트 낭 서리 베리 닿인 탄 동안 달도 게나왔네 ㄱ 거일 이랑 내의 ㅣ 주세 긍대 릉 얘기릉 해 할려 어떡 베 랄 항 문성 이구 이대 용 편 달전 ㄷ감사 나지 누 종 므 르 산 한이 아시 ㅠ네이버 제대 하세영제 영제 한지 차로 와이 죄 주세 김등 개 면 말 소애산부인과원장 정원원장 박희정 강영록 영록 이등 의에 주희 노레 강경 상생리 유재 유재돈 돈 김선복 선복 뉴 렛 질문자분 분 양윤 상담자분 사라 휴 약기 개 안녕하세요시티 김정호 시티 양수진원장 훈 이혁 김상훈 머 황태영입 영입 강미지입니다야즈 이형근 이형 문상현 상현 한방 조예성 조성환 포 원 박관현 관현 홍민 한방 송호철 박평 하이닥산부인 강미지입니다휴약기 박동 장윤주 장 장윤 문경 서운희입니 미 때때 안녕하세요소파 미안 애 바 달 이영진 볍 요기볍것 문의에 유수영 강경구입 들 기의 ㅏㄷ ㄷ 룸 보아야 을지 해보 시기 신재 직 네이버지식인 인유두 상담전문의 보라 김선동 선동 이성윤 으 이민 입 토 반 박지 박지현 김동현 동 아보 다트 ㅋ ㅡ 졋  간의 일인 입니다답변이 정호 입니다적어주신 목부 입니다지금 입니다말씀하신 입니다올려주신 미영 김대영 대영 천은 천은경 바 박춘식 능 시기 붕비 욕 겠습 하심 녹 스  ㅇㅇㅇ 보시 이우 이우영 안녀하세 바 내시 간은 하심 박정 양희탁 희탁 황의 황의경 현훈증 심이 이남 노승혜 고완규 황 호표 표 송민규 은 는 입니다상기 박지원 송민 송민근 근 입니다하이닥 민호 조현섭입 조현섭 현섭 체 신의 신은 다에 이승수 장윤 답변감사 문경용 경용 플 방정 보세 대로 인 실 미레 안녕하세요서 과의 안녕하세요지연 정시 링 합 리덕 장수 원 학과 위의 님 싱 안녕하세요콘 김용진 용진 적 학적 한의 질문자분의 세한 이지 이지호 분의 산부인과전분의 김덕환 환 피부과 산부인과전문의 김덕실 질문글 가정의 곤 최 즈 주남 디 콘 다님 조은 조은석 석 광  느낑 날 성별 됬 노 순 지가 대 일쯤 닥으 게 쎄 인가 ㄹ 색깔ㄹ 건1 조 산기 방도 후로 환주위 하라 안녕하세요가임기 랫엇 안녕하세여 번째 쩨 않하 하고 발견되엇으 하구 요 맺었 야 정은 티 적도 어 을꺼 없엇고 찌 ㅇㅅ ㅅ ㅎ 오ㅠ 기성기 주하 송민근과장 송 ㅡ안녕하세 엇는 엇는데 ㅏ ㅏㅅ 임은 안해주 녕 언 작성하세 가도 맺었 규칮 규칮적인 궁긍 긍 꺼 테 같애여 것같애여 런 소만 국가 트라 가요답변 답변부탁 상담내용 명 사 별 나 총 이정화 뽀드 락 형 고등 쯤 세지 햇었습니 리 자 찮 찮고 건가요 가본적 이인 히 아 물이 시경 기 수도 니 꺼 요배 치 라면 하성 하성민 유 얼마 로 알 전쯤 달전쯤 번 양 재 세 증 상담글 도로 정도로 앞 가야 가야하나요질염 무이 ㅜ ㅜ지금 서도 그때 삼 넘 한날넘 엑스 안 고 중이고요 고요 개인정보보호 개인 달정도 달동안 초 데바이러스 데 지가 가지 구 여속이 달만 안녕 안녕하세 시행시 소애 승혜 한상철 답변 걱정마세 마세 남 주 상담주신 린 안녕하세요 안녕하세요소변 영진 보시기 답 창원 정창원 정 박기호 기호 태성 저 궁 조현 서 여 비 경우여 네이버지식 지식 입니다 혁 배덕호 강미지입니다쿠퍼액 이현철 현철 교 국 향 하 멍 울 부탁 치가 중 매 하이닥 닥 산부인과 신미 영 심 때문 이요 균이요 문의 주수 하다 양이 ㅇ 기결 ㅠ ㅇ통증 뭐 리스 곳 답변감 레 거 지 기가 개요 가요 렐라 렐 라 덱 리을 제가 요고 궁급 급 던 던사람 와요 졲 하세 귀하 질문 내용 등 한국 한국인의 경우 원장 우리 수 일 전 차 신 소 신소애 소애산부인과 신소애산부인과 원장 박 말씀 감사 문 박정원 정원 선생님 월 을 현 시점 마세요 세요 마 내 시일 걱정 듯 설명 주신 작성 등 이후 연락 대게 다 이 때문 터 도움 살 그것 때 라도 중이 정도 자문 상 오 최근 때 근처 663 전 후 전문 파트 담당 년 대학 대학병원 병원 개월 강남역 강남 주말 이번 월드 캐논 캐논매 산부인 한번 내원 자세 생각 1 2 3 4 5 6 7 8 9 행복 하루 세요 -5712 전문의 상담 대장 차 차상헌 상헌 김정우 김 정우 가정 캐논매장 하이 하이닥 닥 은종 운 은종운 의 났데도 관련 시 말씀주신 주신 검사인 규 다 답글 글 요서 데는 사항 헌관 임 임헌관 김경구 김진국 진국 경구 때문 대게 못 저희 너희 일어 이때 재가 현재가 의해 전과 년 복 량 해당 오시 지 예 적인 달뒤 만이 음 파 이것을 그 쪽 내과원 하 등등 다다 코넬 넬 규섭 심상인 박현주 현주 김시현 안상석 호성 홍주희 승 철 김승철 김주남 노태 김우영 우영 허 과 장수연 승헤 김정 질문자 부인과 영상 결정하세 변상권 상권 황인섭 인섭 최호 만 터 이진수 사료 상식 이남호 경구 윤 윤덕 네이버 지식인 글 마티스 류마티스내과 정재 부의 거기 저기 윤덕경 덕 경 류필건 류 필 건 홍현기 홍 현기 김신아 신아 김정태 정태 정현주 현주 박기정 기정 박 박희 김태성 김해성 조창근 조창 김신아입니다야즈 입니다야즈 태익 상훈 장재 박동수 김덕 김정한 정연환 클라 박평식 평 식 이진수 양수진 수진 최호성입니다잔뇨감 강미지 미지 강 황태 황태영  영 조에성 예성 강미 김태한 태한 권 권오 여경아 경아 주셨네요쿠퍼액으 신미영 신미 박동수입 수입 맥도 널드 조병 조병구 조병구입 일로 서운 운 하면 가요 조택우 택우 운희입 희입 이윤길 이윤 송지 송지홍 배덕 홍 정재혁 박선민 선 민 답변이 이호 정소 이재 호 말씀"
stopwords = stopwords.split(' ')
print(len(stopwords))
for i in range(len(df)):
    #제목 불용어 처리
    token_list_title = df['제목'][i].replace("'","").replace(" ","").replace("[","").replace("]","").split(',')
    new_title_list =[]
    for j in range(len(token_list_title)):
        if j ==0:
            token_list_title[j] = token_list_title[j].replace('[','')
            if token_list_title[j] not in stopwords:
                new_title_list.append(token_list_title[j])
        if j ==len(token_list_title)-1:
            token_list_title[j] = token_list_title[j].replace(']','')
            if token_list_title[j] not in stopwords:
                new_title_list.append(token_list_title[j])
        if j > 0 and j < len(token_list_title)-1:
            if token_list_title[j] not in stopwords:
                new_title_list.append(token_list_title[j])
    df['제목'][i] = new_title_list

    # 질문 불용어 처리
    token_list_question = df['질문'][i].replace("'", "").replace(" ", "").replace("[","").replace("]","").split(',')
    new_question_list=[]
    for j in range(len(token_list_question)):
        if j ==0:
            if token_list_question[j] not in stopwords:
                new_question_list.append(token_list_question[j])
        if j ==len(token_list_question)-1:
            if token_list_question[j] not in stopwords:
                new_question_list.append(token_list_question[j])
        if j > 0 and j < len(token_list_question)-1:
            if token_list_question[j] not in stopwords:
                new_question_list.append(token_list_question[j])
    df['질문'][i] = new_question_list

    token_list_answer = df['답변'][i].replace("'", "").replace(" ", "").replace("[","").replace("]","").split(',')
    new_answer_list = []
    for j in range(len(token_list_answer)):
        if j ==0:
            if token_list_answer[j] not in stopwords:
                new_answer_list.append(token_list_answer[j])
        if j ==len(token_list_answer)-1:
            if token_list_answer[j] not in stopwords:
                new_answer_list.append(token_list_answer[j])
        if j > 0 and j < len(token_list_answer)-1:
            if token_list_answer[j] not in stopwords:
                new_answer_list.append(token_list_answer[j])
    df['답변'][i] = new_answer_list

df.to_excel("stopwords.xlsx")
print(df)


