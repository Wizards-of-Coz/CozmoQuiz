# Quiz Master
## Project Description
This is a two player math quiz game for kids, with Cozmo acting as a Quiz Master. The cubes can be used as buzzers. After Cozmo poses the question, whoever taps the cubes first, gets to answer the question. There are flash-cards with numbers, that the kids need to use, to form the answer.

## Video
https://www.youtube.com/watch?v=RFI7NsObF2w

## Implementation Details
This game uses Cozmo SDK’s Custom Markers to help Cozmo recognize numbers. We made flashcards with custom markers on one side and the number on the other. The questions.json file in the Resources folder has the list of questions that can be customized. The code will pick up the questions from this file for Cozmo to speak out. Each custom marker is mapped to a number. So, to form 30, the player will have to hold the 2 cards labelled 3 and 0 in front of Cozmo for him to see.

## Instructions
### Dependencies 
Common - ( Download it from https://github.com/Wizards-of-Coz/Common )

The experience starts with Cozmo looking for the two buzzer cubes to know where the 2 players are sitting. They glow white as soon as they are recognized and the game starts. Make sure the cubes are visible to Cozmo at the start of the experience. Cozmo voices the questions using his speech out (say_text SDK method). Download and print out the custom markers from here. The mapping between the markers and the numbers are defined in the dictionary in line 35 (numMap).

## Thoughts for the Future
The quiz game opens up possibilities of creating Flash card based games that could be played with/against cozmo. This game is unique because players are now playing against each other with cozmo mediating the whole experience. Treating the cubes as buzzers makes the input mechanism more intuitive and contextualized.
