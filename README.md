# Chess

This repository is created for CIS 667 - Intro to Artificial Intelligence class

## Prerequisites
* python 3.6 or later
* numpy

## Game Description
Chess is a two-player board game which requires a checkered board with 64 squares arranged as 8 x 8 grids. Each player begins with 16 pieces. These pieces are pawns (8), bishops (2), knights (2), rooks (2), queen (1) and king (1). Each piece has its unique moves. The most powerful piece is the queen and the least powerful one is the pawn. The main objective is to checkmate the opponent’s king, basically by placing it into a situation where all possible grids that it can move are blocked by at least one or more pieces.

## Required Modifications
* At the beginning of a game, randomly select a small number of positions (say 3) to be "obstacles".  No pieces can be placed at obstacle positions or move through obstacles (for knights, "moving through" means moving along an "L" path that contains an obstacle)
* For state representation, represent an 8x8x12 array.  The third dimension has 12 entries (6 pieces for 2 players), which are 1 if the corresponding piece is at that position, and 0 otherwise.

## Gameplay
* Player selects a chess piece first by showing all the options including how to select that piece (printing string formats to enter)
![1](/images/1.jpg)
* After that game prints x and y coordinates of available chess pieces based on the selection
![2](/images/2.jpg)
* When a specific piece is selected, player makes the move for that piece based on available actions given by the game. Let's say the pawn located in location (6,6) is selected, then the game shows all available actions for that specific pawn such as moving it to locations (4,6) or (5,6) 
 ![3](/images/3.jpg)
* Finally, when one of the available actions is selected, that pieces moves to its new location. Then the game prints new state for the board
![4](/images/4.jpg)
* Game prints states of black and white players as well as their positions after each move. During the selection of the move, game checks whether the players move is a threat for the opponent player’s king or not. On the other hand, game also checks the players move for any checks. If a player moves a piece to a location where the king of the opponent player is threatened, game prints that information to let players know
![5](/images/5.jpg)

## End Game
At the end if a king is threatened by one of the players (checkmate) and there is no place to move for the king, then the game ends with a win for the player who does the checkmate. 

