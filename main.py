import re
import sys
from os import listdir
import RewardFSM
from StoryGame import StoryGame, Question
from numpy import random

print(sys.executable)
print('Good luck!')
# sg = StoryGame()
# sg.showListOfStories()
# sg.chooseStory()


# sg.start_game()
# sg.get_quest()
# a =sg.get_quest()
# a =sg.get_quest()
# a =sg.get_quest()
# a =sg.get_quest()
# a =sg.get_quest()
# a =sg.get_quest()
# a =sg.get_quest()
# a =sg.get_quest()
# a =sg.get_quest()
# a =sg.get_quest()
# a =sg.get_quest()
#
# print(sg.pr_fsm.show_state())
# sg.end_game()
# print("after end")
# print(sg.pr_fsm.show_state())
# a =sg.get_quest()
# a =sg.get_quest()
# a =sg.get_quest()


# sg.chooseDefaultStory()
# sg.make_fill_question_dict()
# open_qe_L = sg.generateQuestions(20, 'sentences')
# qmc_lv2 = sg.generateQuestions(5, 'multiple_choice')
# sg.make_que_lv3(open_qe_L)
# sg.make_que_lv4(open_qe_L)
# sg.make_que_lv2(qmc_lv2)


##############################
# # Jack's Testing:
# story = open("dataset/1. A jataka tale.txt", "r", encoding="utf-8").read()
# sentences = story.split('.')
# for idx, sentence in enumerate(sentences):
#     sentences[idx] = sentence.replace('\n', '')
#     if len(sentences[idx]) < 10:
#         sentences.pop(idx)
# print(sentences)
# q_list = list()
# for sentence in sentences:
#     words = sentence.split()
#     num_of_words = len(words)
#     rand = random.randint(num_of_words)
#     answer = words[rand]
#     words[rand] = '___'
#     question = " ".join(words)
#     q = Question(question=question, answer=answer)
#     q_list.append(q)
# for q in q_list:
#     q.printQA()
