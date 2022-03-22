import random

from question_generator.questiongenerator import QuestionGenerator, print_qa
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
        self.current_state_points = 10
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

    def checkAns(self, ans=''):
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

    def checkAns(self, ans):
        return self.answerChoices[int(ans) - 1]['answer'] == self.answer


class StoryGame:
    def __init__(self):
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
        self.player_coins = 0
        self.correct_ans1 = 0
        self.wrong_ans1 = 0
        self.correct_ans2 = 0
        self.wrong_ans2 = 0
        self.correct_ans3 = 0
        self.wrong_ans3 = 0
        self.correct_ans4 = 0
        self.wrong_ans4 = 0

    def make_fill_question_dict(self):  ##must be used first
        the_story = self.story
        sentences = the_story.split('.')
        shortest_sentence = min([len(j.split()) for j in sentences])
        x = [random.randint(0, shortest_sentence) for i in range(0, len(sentences))]
        # print(x)
        self.q_lv1 = {(sentences[i].replace(sentences[i].split()[x[i]], "_")).strip(): sentences[i].split()[x[i]] for i
                      in range(8)}
        # print(self.q_lv1)

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
        return self.q_lv2[self.qe_lv2_ind - 1]

    def make_que_lv3(self, open_qe_list):
        self.qe_lv3 = [y['question'] for y in [x for x in open_qe_list] if
                       not y['question'].startswith('How') and not y['question'].startswith('Why')]

    def make_que_lv4(self, open_qe_list):
        self.qe_lv4 = [y['question'] for y in [x for x in open_qe_list] if
                       y['question'].startswith('Why') or y['question'].startswith('How')]

    def get_quest(self):
        if self.pr_fsm.show_state() == 1:
            if self.ask_fill_question():
                self.correct_ans1 += 1
                self.player_coins += self.re_fsm.current_state_points
                print("Good Job you gained " + str(self.re_fsm.current_state_points) + " coins")
                self.pr_fsm.send('y')
                self.re_fsm.send('y')
            else:
                self.player_coins -= self.re_fsm.current_state_points
                self.wrong_ans1 += 1
                self.pr_fsm.send('n')
                self.re_fsm.send('n')
                print(" NOT correct")
        elif self.pr_fsm.show_state() == 2:
            q = self.get_qlv2()
            q.displayQ()
            ans = input("Your answer: ")
            if q.checkAns(ans):
                self.player_coins += self.re_fsm.current_state_points
                print("Good Job you gained " + str(self.re_fsm.current_state_points) + " coins")
                self.pr_fsm.send('y')
                self.re_fsm.send('y')
                self.correct_ans2 += 1
            else:
                self.player_coins -= self.re_fsm.current_state_points
                self.wrong_ans2 += 1
                self.pr_fsm.send('n')
                self.re_fsm.send('n')
                print(" NOT correct")
        elif self.pr_fsm.show_state() == 3:
            ans = input(self.qe_lv3[self.qe_lv3_ind])
            self.qe_lv3_ind = self.qe_lv3_ind + 1
            if self.qe_lv3_ind > len(self.qe_lv3):
                self.qe_lv3_ind = 0
            if ans == '':
                self.player_coins -= self.re_fsm.current_state_points
                self.wrong_ans3 += 1
                self.pr_fsm.send('n')
                self.re_fsm.send('n')
                print("NOT correct ")
            else:
                self.player_coins += self.re_fsm.current_state_points
                self.correct_ans3 += 1
                print("Good Job you gained " + str(self.re_fsm.current_state_points) + "coins")
                self.pr_fsm.send('y')
                self.re_fsm.send('y')
        else:
            ans = input(self.qe_lv4[self.qe_lv4_ind])
            self.qe_lv4_ind = self.qe_lv4_ind + 1
            if ans == '':
                print("wrong answer")
                self.player_coins -= self.re_fsm.current_state_points
                self.wrong_ans4 += 1
                self.pr_fsm.send('n')
                self.re_fsm.send('n')
            else:
                print("Good Job you gained " + str(self.re_fsm.current_state_points) + "coins")
                self.player_coins += self.re_fsm.current_state_points
                self.correct_ans4 += 1
                self.pr_fsm.send('y')
                self.re_fsm.send('y')

    def showListOfStories(self):
        self.list_of_stories = listdir('dataset')
        print("List of stories: ")
        for story in self.list_of_stories:
            print(story)

    def chooseStory(self):
        user_input = input("Enter number: ")
        try:
            num = int(user_input)
            print(self.list_of_stories)
        except ValueError:
            print("That's not an int!")

    def chooseDefaultStory(self):
        self.storyPath = 'dataset/1. A jataka tale.txt'
        self.story = open(self.storyPath, encoding="utf-8").read()

    def start_game(self, sg):
        sg.chooseDefaultStory()
        open_qe_L = sg.generateQuestions(20, 'sentences')
        print(open_qe_L)
        qmc_lv2 = sg.generateQuestions(5, 'multiple_choice')
        sg.make_fill_question_dict()
        sg.make_que_lv2(qmc_lv2)
        sg.make_que_lv3(open_qe_L)
        sg.make_que_lv4(open_qe_L)


    def end_game(self):
        print("you finish the game with " + str(self.player_coins))
        if self.correct_ans1 + self.wrong_ans1 > 0:
            print("your lvl 1 success was " + str((self.correct_ans1 / (self.correct_ans1 + self.wrong_ans1)) * 100))
        if self.correct_ans2 + self.wrong_ans2 > 0:
            print("your lvl 2 success was " + str((self.correct_ans2 / (self.correct_ans2 + self.wrong_ans2)) * 100))
        if self.correct_ans3 + self.wrong_ans3 > 0:
            print("your lvl 3 success was " + str(((self.correct_ans3) / (self.correct_ans3 + self.wrong_ans3)) * 100))
        if self.correct_ans4 + self.wrong_ans4 > 0:
            print("your lvl 4 success was " + str((self.correct_ans4 / (self.correct_ans4 + self.wrong_ans4)) * 100))



    def next_game(self):
        if self.correct_ans1 + self.wrong_ans1 > 0:
            q1_rate = (self.correct_ans1 / (self.correct_ans1 + self.wrong_ans1)) * 100
        if self.correct_ans2 + self.wrong_ans2 > 0:
            q2_rate = (self.correct_ans2 / (self.correct_ans2 + self.wrong_ans2)) * 100
        else: q2_rate = 0
        if self.correct_ans3 + self.wrong_ans3 > 0:
            q3_rate = (self.correct_ans3 / (self.correct_ans3 + self.wrong_ans3)) * 100
        else:
            q3_rate = 0
        if self.correct_ans4 + self.wrong_ans4 > 0:
            q4_rate = (self.correct_ans4 / (self.correct_ans4 + self.wrong_ans4)) * 100
        else:
            q4_rate = 0

        if q4_rate>70:
            print("u can go next game")



