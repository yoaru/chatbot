import pandas as pd
import sys , os

class SimpleChatBot:
    def __init__(self, filepath):
         # 생성자: CSV 파일에서 질문과 답변 데이터를 로드
        self.questions, self.answers = self.load_data(filepath)

    def load_data(self, filepath):
         # CSV 파일을 불러와서 질문(Q)과 답변(A) 열을 각각 리스트로 반환
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()  # 질문열만 뽑아 파이썬 리스트로 저장
        answers = data['A'].tolist()   # 답변열만 뽑아 파이썬 리스트로 저장
        return questions, answers

    def calc_distance(self, a, b):
        if a == b: return 0  # 같으면 0을 반환
        a_len = len(a)  # a 길이
        b_len = len(b)  # b 길이
        if a == "": return b_len # 한 쪽이 비어 있으면 다른 쪽 길이만큼 삽입 필요
        if b == "": return a_len

        # 리스트 컴프리헨션으로 행렬 초기화(거리 계산용 2차원 배열)
        matrix = [[0 for _ in range(b_len+1)] for _ in range(a_len+1)]
        
        # 0일 때 초깃값을 설정
        for i in range(a_len+1):
            matrix[i][0] = i
        for j in range(b_len+1):
            matrix[0][j] = j

        # 레벤슈타인 거리 계산
        for i in range(1, a_len+1):
            ac = a[i-1]  # 첫 번째 문자열의 현재 문자
            for j in range(1, b_len+1):
                bc = b[j-1]  # 두 번째 문자열의 현재 문자
                cost = 0 if (ac == bc) else 1  # 두 문자가 같으면 비용은 0, 다르면 1
                
                # 세 가지 경우 중 최소값을 선택
                matrix[i][j] = min([
                    matrix[i-1][j] + 1,     # 문자 제거
                    matrix[i][j-1] + 1,     # 문자 삽입
                    matrix[i-1][j-1] + cost # 문자 변경
                ])
        
        return matrix[a_len][b_len]  # 최종 편집 거리 반환

    def find_best_answer(self, input_sentence):
        # 각 질문과의 레벤슈타인 거리 계산
        distances = [(i, self.calc_distance(input_sentence, question)) 
                    for i, question in enumerate(self.questions)]
            
        # 레벤슈타인_테스트.py에서 실행된 경우에만 거리 출력
        if os.path.basename(sys.modules['__main__'].__file__) == "b.py":
            for i, dist in distances:
                print(f"[{i}] \"{self.questions[i]}\" -> 거리: {dist}")
               
        # 거리가 가장 작은 질문의 인덱스 반환
        best_match_index = min(distances, key=lambda x: x[1])[0]
        return self.answers[best_match_index]

# CSV 파일 경로를 지정하세요.
filepath = 'ChatbotData.csv'

# 간단한 챗봇 인스턴스를 생성합니다.
chatbot = SimpleChatBot(filepath)

# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복합니다.
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.find_best_answer(input_sentence)
    print('Chatbot:', response)



