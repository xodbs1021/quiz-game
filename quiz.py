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