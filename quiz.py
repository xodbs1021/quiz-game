class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question  # 문제 (str)
        self.choices = choices    # 선택지 리스트 (list)
        self.answer = answer      # 정답 번호 (int, 1-4)

    def display(self):
        """문제를 화면에 출력합니다."""
        print(f"\n[문제] {self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice}")

    def check_answer(self, user_input):
        """사용자 입력값이 정답과 일치하는지 확인합니다."""
        return user_input == self.answer


import json
import os

class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.file_path = "state.json"
        self.load_state()  # 시작할 때 데이터를 불러옵니다.

        # 만약 불러온 퀴즈가 없다면 기본 계산 문제 5개를 세팅합니다.
        if not self.quizzes:
            self.set_default_quizzes()

    def set_default_quizzes(self):
        """과제 요구사항: 기본 주제(계산) 퀴즈 5개 생성"""
        default_data = [
            Quiz("5 + 7은 얼마인가요?", ["10", "11", "12", "14"], 3),
            Quiz("12 * 3은 얼마인가요?", ["32", "36", "38", "42"], 2),
            Quiz("100 / 4는 얼마인가요?", ["20", "25", "30", "35"], 2),
            Quiz("15 - 9는 얼마인가요?", ["4", "5", "6", "7"], 3),
            Quiz("7 * 8은 얼마인가요?", ["54", "56", "58", "60"], 2)
        ]
        self.quizzes = default_data

    def load_state(self):
        """JSON 파일에서 데이터를 불러옵니다."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # JSON 데이터를 다시 Quiz 객체 리스트로 변환
                    self.quizzes = [Quiz(q['question'], q['choices'], q['answer']) for q in data['quizzes']]
                    self.best_score = data.get('best_score', 0)
            except (json.JSONDecodeError, KeyError):
                print("⚠️ 데이터 파일이 손상되었습니다. 기본 데이터로 시작합니다.")
                self.quizzes = []

    def save_state(self):
        """현재 상태를 JSON 파일에 저장합니다."""
        data = {
            "quizzes": [
                {"question": q.question, "choices": q.choices, "answer": q.answer}
                for q in self.quizzes
            ],
            "best_score": self.best_score
        }
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)