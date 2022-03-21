from question_generator.questiongenerator import QuestionGenerator
from os import listdir


class StoryGame:
    def __init__(self):
        #self.qg = QuestionGenerator()
        pass

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
