import json
import os

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


class QuizGame:
    def add_quiz(self):
        """새로운 퀴즈를 생성하여 목록에 추가합니다."""
        print("\n--- ➕ 새 퀴즈 추가 ---")

        question = input("문제를 입력하세요: ").strip()
        if not question:
            print("⚠️ 문제는 비어 있을 수 없습니다.")
            return

        choices = []
        for i in range(1, 5):
            while True:
                choice = input(f"선택지 {i}번을 입력하세요: ").strip()
                if choice:
                    choices.append(choice)
                    break
                print("⚠️ 선택지는 비어 있을 수 없습니다.")

        while True:
            answer_input = input("정답 번호(1-4)를 입력하세요: ").strip()
            if answer_input.isdigit() and 1 <= int(answer_input) <= 4:
                answer = int(answer_input)
                break
            print("⚠️ 1에서 4 사이의 숫자를 입력해 주세요.")

        # 새로운 Quiz 객체 생성 및 리스트 추가
        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)
        self.save_state()  # 파일에 바로 저장
        print("✅ 퀴즈가 성공적으로 추가되었습니다!")

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

    def play_quiz(self):
        """저장된 퀴즈를 풀고 결과를 출력합니다."""
        if not self.quizzes:
            print("\n⚠️ 풀 수 있는 퀴즈가 없습니다. 퀴즈를 먼저 추가해 주세요.")
            return

        print("\n--- 📝 퀴즈를 시작합니다! ---")
        current_score = 0

        for quiz in self.quizzes:
            quiz.display()

            while True:
                user_input = input("정답 번호(1-4)를 입력하세요 (0: 중단): ").strip()

                if user_input == '0':
                    print("퀴즈를 중단합니다.")
                    return

                if not user_input.isdigit():
                    print("⚠️ 숫자만 입력 가능합니다. 다시 입력해 주세요.")
                    continue

                choice_num = int(user_input)
                if 1 <= choice_num <= 4:
                    if quiz.check_answer(choice_num):
                        print("✅ 정답입니다!")
                        current_score += 1
                    else:
                        print(f"❌ 틀렸습니다. (정답: {quiz.answer})")
                    break
                else:
                    print("⚠️ 1에서 4 사이의 번호를 입력해 주세요.")

        print(f"\n=== 🏁 결과 발표 ===")
        print(f"맞춘 개수: {current_score} / {len(self.quizzes)}")

        if current_score > self.best_score:
            print(f"🎊 축하합니다! 최고 기록을 경신했습니다! ({self.best_score} -> {current_score})")
            self.best_score = current_score
            self.save_state()
        else:
            print(f"최고 기록: {self.best_score}")

    def show_quiz_list(self):
        """저장된 모든 퀴즈 목록을 출력합니다."""
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return

        print(f"\n--- 현재 등록된 퀴즈 목록 (총 {len(self.quizzes)}개) ---")
        for i, q in enumerate(self.quizzes, 1):
            print(f"{i}. {q.question}")

    def run(self):
        """메뉴를 출력하고 사용자 입력을 받아 기능을 실행합니다."""
        while True:
            try:
                print("\n=== 💡 계산 퀴즈 게임 ===")
                print("1. 퀴즈 풀기")
                print("2. 퀴즈 추가")
                print("3. 퀴즈 목록 보기")
                print("4. 최고 점수 확인")
                print("5. 종료")

                choice = input("번호를 선택하세요: ").strip()

                if choice == '1':
                    self.play_quiz()
                elif choice == '2':
                    self.add_quiz()
                elif choice == '3':
                    self.show_quiz_list()
                elif choice == '4':
                    print(f"\n현재 최고 점수: {self.best_score}점")
                elif choice == '5':
                    print("게임을 종료합니다. 다음에 또 만나요!")
                    self.save_state()
                    break
                elif not choice:
                    print("⚠️ 입력이 비어 있습니다. 번호를 입력해 주세요.")
                else:
                    print("⚠️ 잘못된 번호입니다. 1~5 사이의 숫자를 입력해 주세요.")

            except KeyboardInterrupt:
                print("\n\n[!] Ctrl+C 감지: 데이터를 안전하게 저장하고 종료합니다.")
                self.save_state()
                break
            except EOFError:
                print("\n\n[!] 입력 스트림 종료: 프로그램을 종료합니다.")
                break

# 프로그램 시작점
if __name__ == "__main__":
    game = QuizGame()
    game.run()