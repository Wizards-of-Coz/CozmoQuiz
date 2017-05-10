import asyncio
import cozmo
from cozmo.objects import CustomObjectMarkers, CustomObjectTypes
from Common.woc import WOC
from Common.colors import Colors
from os import system
import random
import _thread
import sys
from threading import Timer
import os
import math
from cozmo.util import degrees
from questions import Questions
import operator

# pip3 install python-dateutil
# pip3 install pyowm
# pip3 install Pillow

'''
CozmoQuiz Module
@class CozmoQuiz
@author - Team Wizards of Coz
'''

class CozmoQuiz(WOC):
    
    cl = None
    exit_flag = False
    audioThread = None
    curEvent = None
    idleAnimations = ['anim_sparking_idle_03','anim_sparking_idle_02','anim_sparking_idle_01']
    attractAttentionAnimations = ['anim_keepaway_pounce_02','reacttoblock_triestoreach_01']
    numMap = {'CustomObjectTypes.CustomType00':'0','CustomObjectTypes.CustomType01':'1','CustomObjectTypes.CustomType02':'2',
              'CustomObjectTypes.CustomType03':'3','CustomObjectTypes.CustomType04':'4','CustomObjectTypes.CustomType05':'5',
              'CustomObjectTypes.CustomType06':'6','CustomObjectTypes.CustomType07':'7','CustomObjectTypes.CustomType08':'8',
              'CustomObjectTypes.CustomType09':'9'}
    animCtr = 0
    face = None
    lookingForFace = False
    buzzerWinner = None
    timeToAnswer = 15
    currentPlayer = 0
    numPlayers = 2 #get input later from command line
    turnsCompleted = 0
    numList = []
    answerGiven = False
    questions = None
    currentQuestion = None
    questionAsked = False
    playerTries = []
    startPose = None
    totalQuestions = 4
    questionsAsked = []
    playerScores = []
    points = [10,5]
    questionNum = 0
    
    
    def __init__(self, *a, **kw):
        
        sys.setrecursionlimit(0x100000)
        
        self.questions = Questions()
        
        cozmo.setup_basic_logging()
#         cozmo.connect_with_tkviewer(self.startResponding)
        cozmo.connect(self.startResponding)
        
        
        
        
    def startResponding(self, coz_conn):
        asyncio.set_event_loop(coz_conn._loop)
        self.coz = coz_conn.wait_for_robot()
        
        self.coz.world.define_custom_cube(CustomObjectTypes.CustomType00,CustomObjectMarkers.Circles2,100,90, 90, False)
        self.coz.world.define_custom_cube(CustomObjectTypes.CustomType01,CustomObjectMarkers.Diamonds2,100,90, 90, False)
        self.coz.world.define_custom_cube(CustomObjectTypes.CustomType02,CustomObjectMarkers.Hexagons2,100,90, 90, False)
        self.coz.world.define_custom_cube(CustomObjectTypes.CustomType03,CustomObjectMarkers.Circles3,100,90, 90, False)
        self.coz.world.define_custom_cube(CustomObjectTypes.CustomType04,CustomObjectMarkers.Diamonds3,100,90, 90, False)
        self.coz.world.define_custom_cube(CustomObjectTypes.CustomType05,CustomObjectMarkers.Hexagons3,100,90, 90, False)
        self.coz.world.define_custom_cube(CustomObjectTypes.CustomType06,CustomObjectMarkers.Circles4,100,90, 90, False)
        self.coz.world.define_custom_cube(CustomObjectTypes.CustomType07,CustomObjectMarkers.Diamonds4,100,90, 90, False)
        self.coz.world.define_custom_cube(CustomObjectTypes.CustomType08,CustomObjectMarkers.Hexagons4,100,90, 90, False)
        self.coz.world.define_custom_cube(CustomObjectTypes.CustomType09,CustomObjectMarkers.Circles5,100,90, 90, False)
        
        self.startPose = self.coz.pose
        look_around = self.coz.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)

        try:
            self.cubes = self.coz.world.wait_until_observe_num_objects(self.numPlayers, object_type = cozmo.objects.LightCube,timeout=60)
        except asyncio.TimeoutError:
            print("Didn't find a cube :-(")
            return
        finally:
            look_around.stop()
            for i in range(0,len(self.cubes)):
                self.cubes[i].set_lights(Colors.WHITE);
                self.playerScores.append(0)
            self.coz.go_to_pose(self.startPose).wait_for_completed()
            self.coz.say_text("Welcome to Math Buzz",duration_scalar=1.5,voice_pitch=-1,in_parallel=False).wait_for_completed()
            self.coz.play_anim('anim_greeting_happy_01').wait_for_completed()
            self.coz.say_text("Let's start!!",duration_scalar=1,voice_pitch=-1,in_parallel=False).wait_for_completed()
            self.askNextQuestion()
        
        while not self.exit_flag:
            asyncio.sleep(0)
        self.coz.abort_all_actions()
    
    
    
    
    def on_object_tapped(self, event, *, obj, tap_count, tap_duration, tap_intensity, **kw):
        if self.questionAsked is True:
            if obj not in self.playerTries:
                self.playerTries.append(obj)
                for i in range(0,len(self.cubes)):
                    self.cubes[i].set_lights_off();
                    if obj == self.cubes[i]:
                        self.currentPlayer = i
                        self.coz.go_to_object(obj,cozmo.util.distance_mm(250),in_parallel=False).wait_for_completed()
                        self.startTimerAndWaitForAnswer()
                        obj.set_lights(Colors.BLUE);
              
    
    
    
    def startTimerAndWaitForAnswer(self):
        
        #Set up event handlerss
        self.coz.world.add_event_handler(cozmo.objects.EvtObjectAppeared, self.foundMarker)
        self.coz.world.add_event_handler(cozmo.objects.EvtObjectDisappeared, self.removeMarker)
        
        Timer(self.timeToAnswer, self.checkAnswer).start()
    
    
    
    
    def checkAnswer(self):
        
        self.numList.sort(key = lambda c: c.pose.position.y)
     
        num = ""
         
        for i in range(0,len(self.numList)):
            num += self.numMap[str(self.numList[i].object_type)]
        
        print("The number is ")
        
        if num == '':
            num = '0'
        
        print(num)
        if int(num) == int(self.currentQuestion['answer']) :
            self.playerScores[self.currentPlayer] += self.points[len(self.playerTries)-1]
            self.coz.say_text("Right Answer! You win "+str(self.points[len(self.playerTries)-1])+" points",duration_scalar=1.5,voice_pitch=-1,in_parallel=False).wait_for_completed()
            self.coz.play_anim('anim_rtpkeepaway_playeryes_02').wait_for_completed()
            self.askNextQuestion()
        else:
            self.coz.play_anim('anim_keepaway_losegame_01').wait_for_completed()
            self.playerScores[self.currentPlayer] -= 10
            print(self.playerScores)
            self.goToNextPlayer()
        
        
    
    
    def goToNextPlayer(self):
        
        self.numList = [];
        
        self.coz.say_text("You are wrong.. You lose 10 points",duration_scalar=1.5,voice_pitch=-1,in_parallel=False).wait_for_completed()
        self.turnsCompleted += 1
        
        if self.turnsCompleted < self.numPlayers - 1:
            
            for i in range(0,len(self.cubes)):
                self.cubes[i].set_lights_off();
                if i != self.currentPlayer  and i not in self.playerTries:
                    self.cubes[i].set_lights(Colors.WHITE.flash());
                    self.buzzerWinner = None
        else:
            self.askNextQuestion()
    
    
    
    
    def askNextQuestion(self):
        
        self.questionNum += 1
        
        if self.questionNum<self.totalQuestions:
            self.coz.go_to_pose(self.startPose).wait_for_completed()
            allPlayerScores = ' '.join(str(score) for score in self.playerScores)
            if self.questionNum>1:
                self.coz.say_text("End of Round "+str(self.questionNum-1)+". The scores are "+allPlayerScores,duration_scalar=1.75,voice_pitch=-1,in_parallel=False).wait_for_completed()
            self.coz.say_text("Round "+str(self.questionNum),duration_scalar=1.75,voice_pitch=-1,in_parallel=False).wait_for_completed()
            self.playerTries = []
            self.currentPlayer = 0
            self.buzzerWinner = None
            self.questionAsked = False
            
            for i in range(0,len(self.cubes)):
                self.cubes[i].set_lights_off();
                    
            self.coz.world.add_event_handler(cozmo.objects.EvtObjectTapped, self.on_object_tapped)
            self.turnsCompleted = 0
            self.currentPlayer = 0
            #go to next question
            
            while(True): 
                self.currentQuestion = self.questions.getRandomQuestion()
                if self.currentQuestion in self.questionsAsked:
                    continue
                else:
                    self.questionsAsked.append(self.currentQuestion)
                    break
            
            self.coz.say_text("What is "+self.currentQuestion['question'],duration_scalar=1.75,voice_pitch=-1,in_parallel=False).wait_for_completed()
            self.coz.say_text("GO",duration_scalar=1,voice_pitch=-1,in_parallel=False).wait_for_completed()
            for i in range(0,len(self.cubes)):
                    self.cubes[i].set_lights(Colors.WHITE.flash());
            self.questionAsked = True
        else:
            self.findWinner()
    
    
    
    
    def findWinner(self):
        for i in range(0,len(self.cubes)):
            self.cubes[i].set_lights_off()
        self.coz.go_to_pose(self.startPose).wait_for_completed()
        self.coz.say_text("Game over",duration_scalar=1.75,voice_pitch=-1,in_parallel=False).wait_for_completed()
        index, value = max(enumerate(self.playerScores), key=operator.itemgetter(1))
        print("The winner is "+str(index))
        self.cubes[index].set_lights(Colors.YELLOW.flash());
        self.coz.go_to_object(self.cubes[index],cozmo.util.distance_mm(150)).wait_for_completed()
        self.coz.play_anim('anim_memorymatch_successhand_cozmo_04').wait_for_completed()
        self.coz.say_text("You win! Congratulations!!",duration_scalar=1.75,voice_pitch=-1,in_parallel=False).wait_for_completed()
    
    
    
    
    def foundMarker(self, event, *, image_box, obj, pose, updated, **kw):
        if self.questionAsked == True:
            if 'Custom' in str(type(obj)):
                if obj not in self.numList:
                    self.numList.append(obj)
                    print(len(self.numList))



    def removeMarker(self, event, *, obj):
        if self.questionAsked == True:
            if obj in self.numList:
                self.numList.remove(obj)
    
    
    
    
    def playIdle(self):
        if self.lookingForFace == False:
            self.coz.play_anim(self.idleAnimations[self.animCtr]).wait_for_completed()
            self.playIdle()
            
            

if __name__ == '__main__':
    CozmoQuiz()