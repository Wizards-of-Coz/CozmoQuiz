import random
import json

QUESTION_PATH = "Resources/questions.json"

class Questions:
    
    def __init__(self):
        self._questionArray = []
        with open('Resources/questions.json') as data_file:
            data = json.load(data_file)
        
        for i in range(0,len(data)):
            self._questionArray.append(data[i])


    def getRandomQuestion(self):
        i = random.randrange(len(self._questionArray))
        return self._questionArray[i]


if __name__ == '__main__':
    q = Questions()