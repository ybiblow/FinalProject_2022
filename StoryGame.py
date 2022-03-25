import random
from question_generator.questiongenerator import QuestionGenerator
from os import listdir


def prime(fn):
    def wrapper(*args, **kwargs):
        v = fn(*args, **kwargs)
        v.send(None)
        return v

    return wrapper


class RewardFSM:
    def __init__(self):
        self.q1a = self._create_q1a()
        self.q1b = self._create_q1b()
        self.q2 = self._create_q2()
        self.q3a = self._create_q3a()
        self.q3b = self._create_q3b()
        self.q4 = self._create_q4()
        self.current_state_index = 1
        self.current_state_points = 10
        self.current_state = self.q1a
        self.stopped = False

    def send(self, char):
        try:
            self.current_state.send(char)
        except StopIteration:
            self.stopped = True

    def show_state(self):
        # print(self.current_state_index)
        return self.current_state_index

    @prime
    def _create_q1a(self):
        while True:
            char = yield
            if char == 'y':
                self.current_state = self.q1b
                self.current_state_index = 1
                self.current_state_points = 10
            else:
                break

    @prime
    def _create_q1b(self):
        while True:
            char = yield
            if char == 'y':
                self.current_state = self.q2
                self.current_state_index = 2
                self.current_state_points = 20
            else:
                self.current_state = self.q1a
                self.current_state_index = 1
                self.current_state_points = 10

    @prime
    def _create_q2(self):
        while True:
            char = yield
            if char == 'y':
                self.current_state = self.q3a
                self.current_state_index = 3
                self.current_state_points = 30
            else:
                self.current_state = self.q1a
                self.current_state_index = 1
                self.current_state_points = 10

    @prime
    def _create_q3a(self):
        while True:
            char = yield
            if char == 'y':
                self.current_state = self.q3b
                self.current_state_index = 3
            else:
                self.current_state = self.q2
                self.current_state_index = 2
                self.current_state_points = 20

    @prime
    def _create_q3b(self):
        while True:
            char = yield
            if char == 'y':
                self.current_state = self.q4
                self.current_state_index = 4
                self.current_state_points = 40
            else:
                self.current_state = self.q3a
                self.current_state_index = 3
                self.current_state_points = 30

    @prime
    def _create_q4(self):
        while True:
            char = yield
            if char != 'y':
                self.current_state = self.q3a
                self.current_state_index = 3
                self.current_state_points = 30
            else:
                break


############################################################

class ProgressFSM:
    def __init__(self):
        self.q1 = self._create_q1()
        self.q2 = self._create_q2()
        self.q3 = self._create_q3()
        self.q4 = self._create_q4()
        self.current_state_index = 1
        self.counter = 0
        self.neg_counter = 0
        self.current_state = self.q1
        self.stopped = False

    def send(self, char):
        try:
            self.current_state.send(char)
        except StopIteration:
            self.stopped = True

    def show_state(self):
        # print(self.current_state_index)
        return self.current_state_index

    def pick_state(self, state):
        self.counter = 0
        self.neg_counter = 0
        if state == 1:
            self.current_state = self.q1
            self.current_state_index = 1
        if state == 2:
            self.current_state = self.q2
            self.current_state_index = 2
        if state == 3:
            self.current_state = self.q3
            self.current_state_index = 3
        if state == 4:
            self.current_state = self.q4
            self.current_state_index = 4

    @prime
    def _create_q1(self):
        while True:
            char = yield
            if char == 'y':
                self.counter = self.counter + 1
                if self.counter > 2:
                    self.counter = 0
                    self.neg_counter = 0
                    self.current_state = self.q2
                    self.current_state_index = 2
                    self.current_state_points = 10
            else:
                self.counter = 0

    @prime
    def _create_q2(self):
        while True:
            char = yield
            if char == 'y':
                self.counter = self.counter + 1
                if self.counter > 1:
                    self.counter = 0
                    self.neg_counter = 0
                    self.current_state = self.q3
                    self.current_state_index = 3
                    self.current_state_points = 30
            else:
                self.counter = 0
                self.neg_counter = self.neg_counter + 1
                if self.neg_counter == 2:
                    self.neg_counter = 0
                    self.counter = 0
                    self.current_state = self.q1
                    self.current_state_index = 1
                    self.current_state_points = 10

    @prime
    def _create_q3(self):
        while True:
            char = yield
            if char == 'y':
                self.counter = self.counter + 1
                if self.counter == 4:
                    self.counter = 0
                    self.neg_counter = 0
                    self.current_state = self.q4
                    self.current_state_index = 4
                    self.current_state_points = 40
            else:
                self.counter = 0
                self.neg_counter = self.neg_counter + 1
                if self.neg_counter == 2:
                    self.counter = 0
                    self.neg_counter = 0
                    self.current_state = self.q2
                    self.current_state_index = 2
                    self.current_state_points = 20

    @prime
    def _create_q4(self):
        while True:
            char = yield
            if char != 'y':
                self.current_state = self.q3
                self.current_state_index = 3
                self.current_state_points = 30


class Question:
    def __init__(self, question='', answer=''):
        self.question = question
        self.answer = answer

    def printQA(self):
        print("Question: " + self.question)
        print("Answer: " + str(self.answer))

    def myCheckAns(self, ans=''):
        if ans == '':
            return False
        return True


class QuestionMultipleChoice(Question):
    def __init__(self, question, answers):
        self.answerChoices = answers
        for answer in self.answerChoices:
            if answer['correct']:
                Question.__init__(self, question=question, answer=answer['answer'])

    def printQA(self):
        print("Question: " + self.question)
        for index, choice in enumerate(self.answerChoices):
            print(str(index + 1) + '. ' + choice['answer'])
        print("Correct Answer: " + self.answer)

    def displayQ(self):
        print(self.question)
        for index, choice in enumerate(self.answerChoices):
            print(str(index + 1) + '. ' + choice['answer'])

    def myCheckAns(self, ans=''):
        return self.answerChoices[int(ans) - 1]['answer'] == self.answer


class StoryGame:
    def __init__(self):
        self.exit_game = 1
        self.q_lv1 = None
        self.q_lv2 = list()
        self.qe_lv3 = None
        self.qe_lv4 = None
        self.qe_lv2_ind = 0
        self.qe_lv3_ind = 0
        self.qe_lv4_ind = 0
        self.story = None
        self.storyPath = None
        self.list_of_stories = None
        self.current_q_lv1 = None
        self.qg = QuestionGenerator()
        self.re_fsm = RewardFSM()
        self.pr_fsm = ProgressFSM()
        self.old_pr_state = 1
        self.player_coins = 0
        self.correct_ans1 = 0
        self.wrong_ans1 = 0
        self.correct_ans2 = 0
        self.wrong_ans2 = 0
        self.correct_ans3 = 0
        self.wrong_ans3 = 0
        self.correct_ans4 = 0
        self.wrong_ans4 = 0
        open("output.txt", "w")

    def make_fill_question_dict(self):
        the_story = self.story
        # sentences = the_story.split(' ')
        sentences = the_story.strip()
        sentences = sentences.split('.')
        x = [random.randint(0, 4) for i in range(0, len(sentences))]
        print(x)
        print(sentences)
        for se in sentences:
            print(se)
            for y in se.split():
                print(y)
        self.q_lv1 = {(sentences[i].replace(sentences[i].split()[x[i]], "___", 1)).strip(): sentences[i].split()[x[i]]
                      for i in range(10) if x[i] < len(sentences[i].split())}
        print(self.q_lv1)

    def generateQuestions(self, q_num, ans_style):
        qa_list = self.qg.generate(
            self.story,
            num_questions=q_num,
            answer_style=ans_style
        )
        return qa_list

    def get_fill_question(self):
        for key in self.q_lv1:
            yield key

    def ask_fill_question(self):
        if self.current_q_lv1 is None:
            self.current_q_lv1 = self.get_fill_question()
        current_q = self.current_q_lv1.__next__()
        print(current_q)
        ans = input("fill the missing word: ")
        return ans == self.q_lv1[current_q]

    def make_que_lv2(self, qmc_lv2):
        for question in qmc_lv2:
            q = QuestionMultipleChoice(question=question['question'], answers=question['answer'])
            self.q_lv2.append(q)

    def get_qlv2(self):
        self.qe_lv2_ind += 1
        if self.qe_lv2_ind == len(self.q_lv2):
            self.qe_lv2_ind = 0
        return self.q_lv2[self.qe_lv2_ind - 1]

    def make_que_lv3(self, open_qe_list):
        self.qe_lv3 = [y['question'] for y in [x for x in open_qe_list] if
                       not y['question'].startswith('How') and not y['question'].startswith('Why')]

    def make_que_lv4(self, open_qe_list):
        self.qe_lv4 = [y['question'] for y in [x for x in open_qe_list] if
                       y['question'].startswith('Why') or y['question'].startswith('How')]

    def check_bonus(self):
        if self.old_pr_state != self.pr_fsm.show_state():
            self.player_coins += 25
            self.old_pr_state = self.pr_fsm.show_state()
            print("you went up a lvl and eren extra 20 points")

    def get_quest(self):
        if self.pr_fsm.show_state() == 1:
            if self.ask_fill_question():
                self.correct_ans1 += 1
                self.player_coins += self.re_fsm.current_state_points
                print("\nGood Job you gained " + str(self.re_fsm.current_state_points) + " Points")
                self.pr_fsm.send('y')
                self.re_fsm.send('y')
                self.check_bonus()
                return True
            else:
                self.player_coins -= self.re_fsm.current_state_points
                self.wrong_ans1 += 1
                self.pr_fsm.send('n')
                self.re_fsm.send('n')
                print("that's not it :(\ngive it another try\n")
                return False
        elif self.pr_fsm.show_state() == 2:
            q = self.get_qlv2()
            q.displayQ()
            ans = input("Your answer: ")
            if q.myCheckAns(ans):
                self.player_coins += self.re_fsm.current_state_points
                print("\nGood Job you gained " + str(self.re_fsm.current_state_points) + " Points")
                self.pr_fsm.send('y')
                self.re_fsm.send('y')
                self.check_bonus()
                self.correct_ans2 += 1
                return True
            else:
                self.player_coins -= self.re_fsm.current_state_points
                self.wrong_ans2 += 1
                self.pr_fsm.send('n')
                self.re_fsm.send('n')
                print("its incorrect :(\nbut i am sure Your perseverance will help you succeed\n")
                return False
        elif self.pr_fsm.show_state() == 3:
            ans = input(self.qe_lv3[self.qe_lv3_ind])
            self.qe_lv3_ind = self.qe_lv3_ind + 1
            if self.qe_lv3_ind == len(self.qe_lv3):
                self.qe_lv3_ind = 0
            if ans == '':
                self.player_coins -= self.re_fsm.current_state_points
                self.wrong_ans3 += 1
                self.pr_fsm.send('n')
                self.re_fsm.send('n')
                print("its incorrect :(\nMistakes are proof that you are trying so keep going\n")
                return False
            else:
                self.player_coins += self.re_fsm.current_state_points
                self.correct_ans3 += 1
                print("\nWell done you gained " + str(self.re_fsm.current_state_points) + " Points")
                self.pr_fsm.send('y')
                self.re_fsm.send('y')
                self.check_bonus()
                return True
        else:
            ans = input(self.qe_lv4[self.qe_lv4_ind])
            self.qe_lv4_ind = self.qe_lv4_ind + 1
            if self.qe_lv4_ind == len(self.qe_lv4):
                self.qe_lv4_ind = 0
            if ans == '':
                print("its incorrect :(\nTrust your instincts I sure you can do it\n")
                self.player_coins -= self.re_fsm.current_state_points
                self.wrong_ans4 += 1
                self.pr_fsm.send('n')
                self.re_fsm.send('n')
                return False
            else:
                print("\n WoW That right! gained " + str(self.re_fsm.current_state_points) + " Points")
                self.player_coins += self.re_fsm.current_state_points
                self.correct_ans4 += 1
                self.pr_fsm.send('y')
                self.re_fsm.send('y')
                self.check_bonus()
                return True

    def showListOfStories(self):
        self.list_of_stories = listdir('dataset')
        print("pick a Story or -1 to Exit")
        for story in self.list_of_stories:
            print(story)

    def chooseStory(self):
        user_input = input("Enter number: ")
        if len(user_input) == 1:
            user_input += "."
        if user_input != '-1':
            try:
                for story in self.list_of_stories:
                    if str(story).startswith(user_input):
                        self.storyPath = story.strip()
                        self.storyPath = 'dataset/' + str(self.storyPath)
                        self.story = open(self.storyPath, encoding="utf-8").read()
            except ValueError:
                print("That's not an int!")

        else:
            self.exit_game = 0

    def chooseDefaultStory(self):
        self.storyPath = 'dataset/1. A jataka tale.txt'
        self.story = open(self.storyPath, encoding="utf-8").read()

    def start_game(self):
        self.showListOfStories()
        self.chooseStory()
        if self.exit_game == 1:
            open_qe_L = self.generateQuestions(20, 'sentences')
            # print(open_qe_L)
            qmc_lv2 = self.generateQuestions(5, 'multiple_choice')
            self.make_fill_question_dict()
            self.make_fill_question_dict1()
            self.make_que_lv2(qmc_lv2)
            self.make_que_lv3(open_qe_L)
            self.make_que_lv4(open_qe_L)
        else:
            print("tnx for playing cya next time")

    def end_game(self):
        self.save_to_file()
        print("\nyou finish the game with " + str(self.player_coins) + " Points!")
        if self.correct_ans1 + self.wrong_ans1 > 0:
            print("your lvl 1 success was " + str(
                (self.correct_ans1 / (self.correct_ans1 + self.wrong_ans1)) * 100) + "%")
        if self.correct_ans2 + self.wrong_ans2 > 0:
            print("your lvl 2 success was " + str(
                (self.correct_ans2 / (self.correct_ans2 + self.wrong_ans2)) * 100) + "%")
        if self.correct_ans3 + self.wrong_ans3 > 0:
            print("your lvl 3 success was " + str(
                (self.correct_ans3 / (self.correct_ans3 + self.wrong_ans3)) * 100) + "%")
        if self.correct_ans4 + self.wrong_ans4 > 0:
            print("your lvl 4 success was " + str(
                (self.correct_ans4 / (self.correct_ans4 + self.wrong_ans4)) * 100) + "%")
        self.next_game()

    def reset_game(self, lv=1):
        self.qe_lv2_ind = 0
        self.qe_lv3_ind = 0
        self.qe_lv4_ind = 0
        self.re_fsm = RewardFSM()
        self.pr_fsm = ProgressFSM()
        self.old_pr_state = 1
        self.player_coins = 0
        self.correct_ans1 = 0
        self.wrong_ans1 = 0
        self.correct_ans2 = 0
        self.wrong_ans2 = 0
        self.correct_ans3 = 0
        self.wrong_ans3 = 0
        self.correct_ans4 = 0
        self.wrong_ans4 = 0
        if lv == 0:
            self.showListOfStories()
            self.chooseStory()
            lv = 1
        self.pr_fsm.pick_state(lv)

    def next_game(self):
        if self.correct_ans1 + self.wrong_ans1 > 0:
            q1_rate = (self.correct_ans1 / (self.correct_ans1 + self.wrong_ans1)) * 100
        else:
            q1_rate = 0
        if self.correct_ans2 + self.wrong_ans2 > 0:
            q2_rate = (self.correct_ans2 / (self.correct_ans2 + self.wrong_ans2)) * 100
        else:
            q2_rate = 0
        if self.correct_ans3 + self.wrong_ans3 > 0:
            q3_rate = (self.correct_ans3 / (self.correct_ans3 + self.wrong_ans3)) * 100
        else:
            q3_rate = 0
        if self.correct_ans4 + self.wrong_ans4 > 0:
            q4_rate = (self.correct_ans4 / (self.correct_ans4 + self.wrong_ans4)) * 100
        else:
            q4_rate = 0

        if q4_rate > 50:
            print("well done you successfully finished the story well\nyou can move to the next one")
            self.reset_game(0)  # chose story only here
        elif q3_rate > 60:
            print("you  need to work on your open question skills,lets try agine")
            self.reset_game(4)
        elif q2_rate > 60:
            print("you  need to work on your Basic Open question skills,lets try agine")
            self.reset_game(3)
        elif q1_rate > 70:
            print("you  need to work on your multiple choice question skills,lets try agine")
            self.reset_game(2)
        else:
            self.reset_game(1)  # Same story  here

    def save_to_file(self, new_story=1):
        ca1, wa1 = str(self.correct_ans1) + "\n", str(self.wrong_ans1) + "\n"
        ca2, wa2 = str(self.correct_ans2) + "\n", str(self.wrong_ans2) + "\n"
        ca3, wa3 = str(self.correct_ans3) + "\n", str(self.wrong_ans3) + "\n"
        ca4, wa4 = str(self.correct_ans4) + "\n", str(self.wrong_ans4) + "\n"
        print("Saving to file...")
        output = open("output.txt", "a")
        output.write(ca1 + wa1 + ca2 + wa2 + ca3 + wa3 + ca4 + wa4)
        output.close()
        print("Saved to file!")

    def make_fill_question_dict1(self):
        story = self.story
        sentences = story.split('.')
        for idx, sentence in enumerate(sentences):
            sentences[idx] = sentence.replace('\n', '')
            if len(sentences[idx]) < 10:
                sentences.pop(idx)
        print(sentences)
        self.q_lvl1 = list()
        for sentence in sentences:
            words = sentence.split()
            num_of_words = len(words)
            rand = random.randint(num_of_words)
            answer = words[rand]
            words[rand] = '___'
            question = " ".join(words)
            q = Question(question=question, answer=answer)
            self.q_lvl1.append(q)
        for q in self.q_lvl1:
            q.printQA()

