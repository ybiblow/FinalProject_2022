import sys
from os import listdir
import time
import RewardFSM
from StoryGame import StoryGame

print(sys.executable)
print('Good luck!')

# sg.showListOfStories()
# sg.chooseStory()


sg = StoryGame()
sg.start_game(sg)
print(sg.qe_lv3)
print(sg.qe_lv4)


sg.get_quest()
sg.get_quest()
sg.get_quest()
sg.get_quest()
sg.get_quest()
sg.end_game()
# sg.chooseDefaultStory()
# sg.make_fill_question_dict()
# open_qe_L = sg.generateQuestions(20, 'sentences')
# qmc_lv2 = sg.generateQuestions(5, 'multiple_choice')
# sg.make_que_lv3(open_qe_L)
# sg.make_que_lv4(open_qe_L)
# sg.make_que_lv2(qmc_lv2)





