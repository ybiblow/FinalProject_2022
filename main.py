import sys
from os import listdir
import time

from StoryGame import StoryGame

print(sys.executable)
print('hello world!')

sg = StoryGame()
sg.showListOfStories()
sg.chooseStory()

# start = time.time()
# sg.generateQuestions()
# end = time.time()
# print('Time for creating QG: ', end - start)
