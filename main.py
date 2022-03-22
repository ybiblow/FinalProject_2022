import sys
from os import listdir
import time
import RewardFSM
from StoryGame import StoryGame

print(sys.executable)
print('Good luck!')
sg = StoryGame()
# sg.showListOfStories()
# sg.chooseStory()



sg.start_game()
sg.pr_fsm.send('y')
sg.pr_fsm.send('y')
sg.get_quest()
sg.get_quest()
sg.get_quest()
sg.get_quest()
sg.get_quest()
sg.get_quest()
sg.get_quest()
sg.get_quest()
sg.get_quest()
print("----")
print(sg.pr_fsm.show_state())
sg.end_game()
print("after end")
print(sg.pr_fsm.show_state())
sg.get_quest()
sg.get_quest()
sg.get_quest()




# sg.chooseDefaultStory()
# sg.make_fill_question_dict()
# open_qe_L = sg.generateQuestions(20, 'sentences')
# qmc_lv2 = sg.generateQuestions(5, 'multiple_choice')
# sg.make_que_lv3(open_qe_L)
# sg.make_que_lv4(open_qe_L)
# sg.make_que_lv2(qmc_lv2)





