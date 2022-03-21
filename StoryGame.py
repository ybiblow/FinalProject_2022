from question_generator.questiongenerator import QuestionGenerator
from os import listdir


class StoryGame:
    def __init__(self):
        self.qg = QuestionGenerator()
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

    def chooseDefaultStory(self):
        self.storyPath = 'dataset/1. A jataka tale.txt'
        self.story = open(self.storyPath, encoding="utf-8").read()
        print(self.story)

    def generateQuestions(self, story, num_of_questions, answ_style):
        qa_list = self.qg.generate(self.story, num_questions=num_of_questions, answer_style=answ_style)
        print(qa_list)
