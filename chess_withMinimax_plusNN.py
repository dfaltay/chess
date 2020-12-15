import numpy as np
import random
import sys
import time
import chess_net as cn
# import chess_data as cd
import torch as tr

class MinimaxEngine:

    def __init__(self, max_depth):
        #  max_depth : int    --max depth of the tree
        self.max_depth = max_depth

    def bestAction(self, state, selection, is_max, piece):
        start_time = time.time()
        possibleMoves = getPossibleMoves(selection,state, piece) # List of all states     #### This function is needed ####
        baseScore = -9999
        finalMove = None
        
        # for p in possibleMoves:
            # print("/////////////////////")
            # print(p)

        
        for moves in possibleMoves:

            bestMove = max(baseScore, self.minimax(self.max_depth, moves, -10000, 10000, not is_max, selection, piece))
            
            if(bestMove > baseScore):
                baseScore = bestMove
                finalMove = moves
        
        time_passed = time.time() - start_time
        print("Total amount time for minimax is: %s seconds", time_passed)
        
        return finalMove, baseScore



    def minimax(self, depth, state, alpha, beta, is_max, selection, piece):
        
        if(depth == 0):
            # print("evaluate", self.evaluation(state))
            # print('state in minimax: ',state)
            return self.evaluation(state)
        possibleMoves = getPossibleMoves(selection,state, piece) # List of all states     #### This function is needed ####
        '''for s in possibleMoves: #prints all possible states after each move of black
            print("-------------------")
            print(s)'''
        if(is_max):
            bestMove = -9999
            for state in possibleMoves:
                # print("state1: ")
                # print('state in minimax + is_max :',state)
                bestMove = max(bestMove, self.minimax(depth-1, state, alpha, beta, not is_max, selection, piece))
                alpha = max(alpha, bestMove)
                # print("alpha: ", alpha)
                if beta <= alpha:
                    return bestMove
            return bestMove
        else:
            bestMove = 9999
            for state in possibleMoves:
                # print("state2: ")
                # print(state)
                bestMove = min(bestMove, self.minimax(depth-1, state, alpha, beta, not is_max, selection, piece))
                beta = min(beta,bestMove)
                # print("beta: ", beta)
                if(beta <= alpha):
                    return bestMove
            return bestMove
        


    def evaluation(self, state):

        evaluation = 0
        #print(str(state))
        #print(state.board)
        for i in range(0, len(state.board)):
            for j in range(0, len(state.board[i])):
                evaluation = evaluation + (self.getPieceValue(state.board[i][j]))

        '''for x in state[0]:
            for y in state[1]:
                evaluation = evaluation + (self.getPieceValue(state[x][y]))'''

        return evaluation


    def getPieceValue(self, piece):
        
        #print("piece: ",piece)
        if(piece == None):
            return 0
        value = 0
        if piece == "-1":
            value = -10
        elif piece == "+1": #Pawn
            value = 10
        if piece == "-2":
            value = -30
        elif piece == "+2": #Knight
            value = 30
        if piece == "-3":
            value = -30
        elif piece == "+3": #Bishop
            value = 30
        if piece == "-4":
            value = -50
        elif piece == "+4": #Rook
            value = 50
        if piece == "-5":
            value = -90
        elif piece == "+5": #Queen
            value = 90
        if piece == '-6':
            value = -900
        elif piece == '+6': #King
            value = 900
        if piece == "WL": #Wall
            value = 0
        if piece == "": #Empty
            value = 0

        return value




class ChessState(object):
    def __init__(self,selection):
        if selection == "1":
            self.board = np.empty((8,8),dtype="U2")
            self.board[:] = "  "
        elif selection == "2":
            self.board = np.empty((8,7),dtype="U2")
            self.board[:] = "  "
        elif selection == "3":
            self.board = np.empty((8,6),dtype="U2")
            self.board[:] = "  "
        elif selection == "4":
            self.board = np.empty((8,5),dtype="U2")
            self.board[:] = "  "
        elif selection == "5":
            self.board = np.empty((8,4),dtype="U2")
            self.board[:] = "  "
    def __str__(self):
        string = ""
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                string += self.board[i,j]
            string += "\n"
        return string[:-1]
    def piece_positions(self,piece_name,selection):
        state = ChessState(selection)
        state.board = np.copy(self.board)
        positions = []
        np_where = np.argwhere(state.board == piece_name)
        for i in range(0, len(np_where)):
            positions.append("(" + str(np_where[i,0]) + "," + str(np_where[i,1]) + ")")
          
        return positions
    def pawn_actions(self,x,y,player,isAttack,selection):
        state = ChessState(selection)
        state.board = np.copy(self.board)
        actions = []
        
        #print("board size: ", len(state.board))
        if player == "+":
            #If it is an opening move, move -2x
            if x-2 >= 0 and x-2 <= len(state.board)-1 and y >= 0 and y <= len(state.board[0])-1 and isAttack == False:
                if x == 6 and state.board[x-2,y] == "  " and state.board[x-1,y] != "WL":
                    actions.append("(" + str(x-2)+ "," + str(y) + ")")
            #move -x
            if x-1 >= 0 and x-1 <= len(state.board)-1 and y >= 0 and y <= len(state.board[0])-1 and isAttack == False:
                if state.board[x-1,y] == "  ":
                    actions.append("(" + str(x-1)+ "," + str(y) + ")")
            #move (-x,-y)
            if x-1 >= 0 and x-1 <= len(state.board)-1 and y-1 >= 0 and y-1 <= len(state.board[0])-1:
                if state.board[x-1,y-1] != "  " and state.board[x-1,y-1][0] != player and state.board[x-1,y-1] != "WL":
                    actions.append("(" + str(x-1)+ "," + str(y-1) + ")")
            #move (-x,+y)
            if x-1 >= 0 and x-1 <= len(state.board)-1 and y+1 >= 0 and y+1 <= len(state.board[0])-1:
                if state.board[x-1,y+1] != "  " and state.board[x-1,y+1][0] != player and state.board[x-1,y+1] != "WL":
                    actions.append("(" + str(x-1)+ "," + str(y+1) + ")")
        else:
            #If it is an opening move, move +2x
            if x+2 >= 0 and x+2 <= len(state.board)-1 and y >= 0 and y <= len(state.board[0])-1 and isAttack == False:
                if x == 1 and state.board[x+2,y] == "  " and state.board[x+1,y] != "WL":
                    actions.append("(" + str(x+2)+ "," + str(y) + ")")
            #move +x
            if x+1 >= 0 and x+1 <= len(state.board)-1 and y >= 0 and y <= len(state.board[0])-1 and isAttack == False:
                if state.board[x+1,y] == "  ":
                    actions.append("(" + str(x+1)+ "," + str(y) + ")")
            #move (+x,-y)
            if x+1 >= 0 and x+1 <= len(state.board)-1 and y-1 >= 0 and y-1 <= len(state.board[0])-1:
                if state.board[x+1,y-1] != "  " and state.board[x+1,y-1][0] != player and state.board[x+1,y-1] != "WL":
                    actions.append("(" + str(x+1)+ "," + str(y-1) + ")")
            #move (+x,+y)
            if x+1 >= 0 and x+1 <= len(state.board)-1 and y+1 >= 0 and y+1 <= len(state.board[0])-1:
                if state.board[x+1,y+1] != "  " and state.board[x+1,y+1][0] != player and state.board[x+1,y+1] != "WL":
                    actions.append("(" + str(x+1)+ "," + str(y+1) + ")")
        
        
        return actions
    def knight_actions(self,x,y,player,selection):
        state = ChessState(selection)
        state.board = np.copy(self.board)
        actions = []
              
        #long L in (-x,-y) direction
        if x-2 >= 0 and x-2 <=len(state.board)-1 and y-1 >= 0 and y-1 <= len(state.board[0])-1:
            if state.board[x-2,y-1] != "WL" and state.board[x-2,y-1][0] != player and((state.board[x-1,y] != "WL" and state.board[x-2,y] != "WL") or(state.board[x,y-1] != "WL" and state.board[x-1,y-1] != "WL")):      
                actions.append("(" + str(x-2)+ "," + str(y-1) + ")")
        #long L in (-x, +y) direction
        if x-2 >= 0 and x-2 <=len(state.board)-1 and y+1 >= 0 and y+1 <= len(state.board[0])-1:
            if state.board[x-2,y+1] != "WL" and state.board[x-2,y+1][0] != player and((state.board[x-1,y] != "WL" and state.board[x-2,y] != "WL") or(state.board[x,y+1] != "WL" and state.board[x-1,y+1] != "WL")):                
                actions.append("(" + str(x-2)+ "," + str(y+1) + ")")
        #short L in (-x, -y) direction
        if x-1 >= 0 and x-1 <=len(state.board)-1 and y-2 >= 0 and y-2 <= len(state.board[0])-1:        
            if state.board[x-1,y-2] != "WL" and state.board[x-1,y-2][0] != player and((state.board[x-1,y] != "WL" and state.board[x-1,y-1] != "WL") or(state.board[x,y-1] != "WL" and state.board[x,y-2] != "WL")):               
                actions.append("(" + str(x-1)+ "," + str(y-2) + ")")
        #short L in (-x,+y) direction
        if x-1 >= 0 and x-1 <=len(state.board)-1 and y+2 >= 0 and y+2 <= len(state.board[0])-1:
            if state.board[x-1,y+2] != "WL" and state.board[x-1,y+2][0] != player and((state.board[x-1,y] != "WL" and state.board[x-1,y+1] != "WL") or(state.board[x,y+1] != "WL" and state.board[x,y+2] != "WL")):                   
                actions.append("(" + str(x-1)+ "," + str(y+2) + ")")
        #long L in (+x,-y) direction
        if x+2 >= 0 and x+2 <=len(state.board)-1 and y-1 >= 0 and y-1 <= len(state.board[0])-1:
            if state.board[x+2,y-1] != "WL" and state.board[x+2,y-1][0] != player and((state.board[x+1,y] != "WL" and state.board[x+2,y] != "WL") or(state.board[x,y-1] != "WL" and state.board[x+1,y-1] != "WL")):                
                actions.append("(" + str(x+2)+ "," + str(y-1) + ")")
        #long L in (+x,+y) direction       
        if x+2 >= 0 and x+2 <=len(state.board)-1 and y+1 >= 0 and y+1 <= len(state.board[0])-1:        
            if state.board[x+2,y+1] != "WL" and state.board[x+2,y+1][0] != player and((state.board[x+1,y] != "WL" and state.board[x+2,y] != "WL") or(state.board[x,y+1] != "WL" and state.board[x+1,y+1] != "WL")):                
                actions.append("(" + str(x+2)+ "," + str(y+1) + ")")
        #short L in (+x,-y) direction
        if x+1 >= 0 and x+1 <=len(state.board)-1 and y-2 >= 0 and y-2 <= len(state.board[0])-1:
            if state.board[x+1,y-2] != "WL" and state.board[x+1,y-2][0] != player and((state.board[x+1,y] != "WL" and state.board[x+1,y-1] != "WL") or(state.board[x,y-1] != "WL" and state.board[x,y-2] != "WL")):               
                actions.append("(" + str(x+1)+ "," + str(y-2) + ")")
        #short L in (+x,+y) direction
        if x+1 >= 0 and x+1 <=len(state.board)-1 and y+2 >= 0 and y+2 <= len(state.board[0])-1:        
            if state.board[x+1,y+2] != "WL" and state.board[x+1,y+2][0] != player and((state.board[x+1,y] != "WL" and state.board[x+1,y+1] != "WL") or(state.board[x,y+1] != "WL" and state.board[x,y+2] != "WL")):                
                actions.append("(" + str(x+1)+ "," + str(y+2) + ")")
        
        
        return actions
    def bishop_actions(self,x,y,player,selection):
        state = ChessState(selection)
        state.board = np.copy(self.board)
        actions = []
        idx = 1
        if player == "+":
            opponent = "-"
        elif player == "-":
            opponent = "+"
        #moving in (-x,-y) direction
        while True:
            if y-idx < 0 or x-idx < 0:
                break
            else:
                if state.board[x-idx,y-idx] != "WL" and state.board[x-idx,y-idx][0] != player:
                    #if we encounter counter piece, remove the counter piece and terminate, if not resume
                    if state.board[x-idx,y-idx][0] == opponent:
                        actions.append("(" + str(x-idx)+ "," + str(y-idx) + ")")
                        break
                    else:
                       actions.append("(" + str(x-idx)+ "," + str(y-idx) + ")") 
                else:
                    break
            idx = idx+1
        idx = 1
        #moving in (-x,+y) direction
        while True:
            if y+idx > len(state.board[0])-1 or x-idx < 0:
                break
            else:
                if state.board[x-idx,y+idx] != "WL" and state.board[x-idx,y+idx][0] != player:
                    #if we encounter counter piece, remove the counter piece and terminate, if not resume
                    if state.board[x-idx,y+idx][0] == opponent:
                        actions.append("(" + str(x-idx)+ "," + str(y+idx) + ")")
                        break
                    else:
                        actions.append("(" + str(x-idx)+ "," + str(y+idx) + ")")
                else:
                    break
            idx = idx+1
        idx = 1
        #moving in (+x,-y direction)
        while True:
            if y-idx < 0 or x+idx > len(state.board)-1:
                break
            else:
                if state.board[x+idx,y-idx] != "WL" and state.board[x+idx,y-idx][0] != player:
                    #if we encounter counter piece, remove the counter piece and terminate, if not resume
                    if state.board[x+idx,y-idx][0] == opponent:
                        actions.append("(" + str(x+idx)+ "," + str(y-idx) + ")")
                        break
                    else:
                        actions.append("(" + str(x+idx)+ "," + str(y-idx) + ")")
                else:
                    break
            idx = idx+1
        idx = 1
        #moving in (+x,+y) direction
        while True:
            if y+idx > len(state.board[0])-1 or x+idx > len(state.board)-1:
                break
            else:
                if state.board[x+idx,y+idx] != "WL" and state.board[x+idx,y+idx][0] != player:
                    #if we encounter counter piece, remove the counter piece and terminate, if not resume
                    if state.board[x+idx,y+idx][0] == opponent:
                        actions.append("(" + str(x+idx)+ "," + str(y+idx) + ")")
                        break
                    else:
                        actions.append("(" + str(x+idx)+ "," + str(y+idx) + ")")
                else:
                    break
            idx = idx+1
        idx = 1
        return actions
    def rook_actions(self,x,y,player,selection):
        state = ChessState(selection)
        state.board = np.copy(self.board)
        actions = []
        idx = 1
        if player == "+":
            opponent = "-"
        elif player == "-":
            opponent = "+"
        #moving in (-x) direction
        while True:
            if x-idx < 0:
                break
            else:
                if state.board[x-idx,y] != "WL" and state.board[x-idx,y][0] != player:
                    #if we encounter counter piece, remove the counter piece and terminate, if not resume
                    if state.board[x-idx,y][0] == opponent:
                        actions.append("(" + str(x-idx)+ "," + str(y) + ")")
                        break
                    else:
                        actions.append("(" + str(x-idx)+ "," + str(y) + ")")
                else:
                    break
            idx = idx+1
        idx = 1
        #moving in (+x) direction
        while True:
            if x+idx > len(state.board)-1:
                break
            else:
                if state.board[x+idx,y] != "WL" and state.board[x+idx,y][0] != player:
                    #if we encounter counter piece, remove the counter piece and terminate, if not resume
                    if state.board[x+idx,y][0] == opponent:
                        actions.append("(" + str(x+idx)+ "," + str(y) + ")")
                        break
                    else:
                        actions.append("(" + str(x+idx)+ "," + str(y) + ")")
                else:
                    break
            idx = idx+1
        idx = 1
        #moving in (-y) direction
        while True:
            if y-idx < 0:
                break
            else:
                if state.board[x,y-idx] != "WL" and state.board[x,y-idx][0] != player:
                    #if we encounter counter piece, remove the counter piece and terminate, if not resume
                    if state.board[x,y-idx][0] == opponent:
                        actions.append("(" + str(x)+ "," + str(y-idx) + ")")
                        break
                    else:
                        actions.append("(" + str(x)+ "," + str(y-idx) + ")")
                else:
                    break
            idx = idx+1
        idx = 1
        #moving in (+y) direction
        while True:
            if y+idx > len(state.board[0])-1:
                break
            else:
                if state.board[x,y+idx] != "WL" and state.board[x,y+idx][0] != player:
                    #if we encounter counter piece, remove the counter piece and terminate, if not resume
                    if state.board[x,y+idx][0] == opponent:
                        actions.append("(" + str(x)+ "," + str(y+idx) + ")")
                        break
                    else:
                        actions.append("(" + str(x)+ "," + str(y+idx) + ")")
                else:
                    break
            idx = idx+1
        idx = 1
        return actions
    def king_actions(self,x,y,player,selection):
        state = ChessState(selection)
        state.board = np.copy(self.board)
        actions = []
        #moving in -x direction
        if x-1 >= 0 and x-1 <=len(state.board)-1 and y >= 0 and y <= len(state.board[0])-1:
            if state.board[x-1,y] != "WL" and state.board[x-1,y][0] != player:
                actions.append("(" + str(x-1)+ "," + str(y) + ")")
        #moving in (-x,-y) direction
        if x-1 >= 0 and x-1 <=len(state.board)-1 and y-1 >= 0 and y-1 <= len(state.board[0])-1:
            if state.board[x-1,y-1] != "WL" and state.board[x-1,y-1][0] != player:
                actions.append("(" + str(x-1)+ "," + str(y-1) + ")")
        #moving in (-x,+y) direction
        if x-1 >= 0 and x-1 <=len(state.board)-1 and y+1 >= 0 and y+1 <= len(state.board[0])-1:
            if state.board[x-1,y+1] != "WL" and state.board[x-1,y+1][0] != player:
                actions.append("(" + str(x-1)+ "," + str(y+1) + ")")
        #moving in -y direction
        if x >= 0 and x <=len(state.board)-1 and y-1 >= 0 and y-1 <= len(state.board[0])-1:
            if state.board[x,y-1] != "WL" and state.board[x,y-1][0] != player:
                actions.append("(" + str(x)+ "," + str(y-1) + ")")
        #moving in +y direction
        if x >= 0 and x <=len(state.board)-1 and y+1 >= 0 and y+1 <= len(state.board[0])-1:
            if state.board[x,y+1] != "WL" and state.board[x,y+1][0] != player:
                actions.append("(" + str(x)+ "," + str(y+1) + ")")
        #moving in (+x,+y) direction
        if x+1 >= 0 and x+1 <=len(state.board)-1 and y+1 >= 0 and y+1 <= len(state.board[0])-1:
            if state.board[x+1,y+1] != "WL" and state.board[x+1,y+1][0] != player:
                actions.append("(" + str(x+1)+ "," + str(y+1) + ")")
        #moving in +x direction
        if x+1 >= 0 and x+1 <=len(state.board)-1 and y >= 0 and y <= len(state.board[0])-1:
            if state.board[x+1,y] != "WL" and state.board[x+1,y][0] != player:
                actions.append("(" + str(x+1)+ "," + str(y) + ")")
        #moving in (+x,-y) direction
        if x+1 >= 0 and x+1 <=len(state.board)-1 and y-1 >= 0 and y-1 <= len(state.board[0])-1:
            if state.board[x+1,y-1] != "WL" and state.board[x+1,y-1][0] != player:
                actions.append("(" + str(x+1)+ "," + str(y-1) + ")")
        
        
        return actions
    def is_king_threated(self,x1,y1,x2,y2,player,selection):
        new_state = ChessState(selection)
        new_state.board = np.copy(self.board)
        #if x1,y1,x2,y2 are zero, we check if our player performs check after move function. Else we check if opposition player performs check before move function
        if x1 != -1 and y1 != -1 and x2 != -1 and y2 != -1:
            new_state.board[x2,y2] = self.board[x1,y1]
            new_state.board[x1,y1] = "  "
        #print("new state board: ", new_state.board)
        black_positions = []
        black_states = []
        white_positions = []
        white_states = []
        if player == "+":
            #retrieve all the positions of black pieces
            black_pieces1 = np.argwhere(new_state.board == "-1")
            for i in range(0, len(black_pieces1)):
                black_positions.append(str(black_pieces1[i,0]) + "," + str(black_pieces1[i,1]) + "," + "-1")
            black_pieces2 = np.argwhere(new_state.board == "-2")
            for i in range(0, len(black_pieces2)):
                black_positions.append(str(black_pieces2[i,0]) + "," + str(black_pieces2[i,1]) + "," + "-2")
            black_pieces3 = np.argwhere(new_state.board == "-3")
            for i in range(0, len(black_pieces3)):
                black_positions.append(str(black_pieces3[i,0]) + "," + str(black_pieces3[i,1]) + "," + "-3")
            black_pieces4 = np.argwhere(new_state.board == "-4")
            for i in range(0, len(black_pieces4)):
                black_positions.append(str(black_pieces4[i,0]) + "," + str(black_pieces4[i,1]) + "," + "-4")
            black_pieces5 = np.argwhere(new_state.board == "-5")
            for i in range(0, len(black_pieces5)):
                black_positions.append(str(black_pieces5[i,0]) + "," + str(black_pieces5[i,1]) + "," + "-5" )
            black_pieces6 = np.argwhere(new_state.board == "-6")
            for i in range(0, len(black_pieces6)):
                black_positions.append(str(black_pieces6[i,0]) + "," + str(black_pieces6[i,1]) + "," + "-6")
            
            #print("black positions:", black_positions)
            #retrieve all the possible moves from pieces in corresponding positions
            for i in range(0, len(black_positions)):
                if black_positions[i][5] == '1':
                    black_states.append(new_state.pawn_actions(int(black_positions[i][0]),int(black_positions[i][2]),"-",True,selection))
                if black_positions[i][5] == '2':
                    black_states.append(new_state.knight_actions(int(black_positions[i][0]),int(black_positions[i][2]),"-",selection))
                elif black_positions[i][5] == '3':
                    black_states.append(new_state.bishop_actions(int(black_positions[i][0]),int(black_positions[i][2]),"-",selection))
                elif black_positions[i][5] == '4':
                    black_states.append(new_state.rook_actions(int(black_positions[i][0]),int(black_positions[i][2]),"-",selection))
                elif black_positions[i][5] == '5':
                    black_states.append(new_state.bishop_actions(int(black_positions[i][0]),int(black_positions[i][2]),"-",selection) + new_state.rook_actions(int(black_positions[i][0]),int(black_positions[i][2]),"-",selection))
                elif black_positions[i][5] == '6':
                    black_states.append(new_state.king_actions(int(black_positions[i][0]),int(black_positions[i][2]),"-",selection))
            #print("black states: ", black_states)
            
            for i in range(0, len(black_states)):
                for j in range(0, len(black_states[i])):
                    #if king is in one of those positions, return false, because move will be invalid 
                    if(new_state.board[int(black_states[i][j][1]),int(black_states[i][j][3])] == "+6"):
                        return True
                    #print(black_states[i][j][1])
                    #print(black_states[i][j][3])
            return False
        elif player == "-":
            #retrieve all the positions of white pieces
            white_pieces1 = np.argwhere(new_state.board == "+1")
            for i in range(0, len(white_pieces1)):
                white_positions.append(str(white_pieces1[i,0]) + "," + str(white_pieces1[i,1]) + "," + "+1")
            white_pieces2 = np.argwhere(new_state.board == "+2")
            for i in range(0, len(white_pieces2)):
                white_positions.append(str(white_pieces2[i,0]) + "," + str(white_pieces2[i,1]) + "," + "+2")
            white_pieces3 = np.argwhere(new_state.board == "+3")
            for i in range(0, len(white_pieces3)):
                white_positions.append(str(white_pieces3[i,0]) + "," + str(white_pieces3[i,1]) + "," + "+3")
            white_pieces4 = np.argwhere(new_state.board == "+4")
            for i in range(0, len(white_pieces4)):
                white_positions.append(str(white_pieces4[i,0]) + "," + str(white_pieces4[i,1]) + "," + "+4")
            white_pieces5 = np.argwhere(new_state.board == "+5")
            for i in range(0, len(white_pieces5)):
                white_positions.append(str(white_pieces5[i,0]) + "," + str(white_pieces5[i,1]) + "," + "+5" )
            white_pieces6 = np.argwhere(new_state.board == "+6")
            for i in range(0, len(white_pieces6)):
                white_positions.append(str(white_pieces6[i,0]) + "," + str(white_pieces6[i,1]) + "," + "+6")
            
            #print("white positions:", white_positions)
            #retrieve all the possible moves from pieces in corresponding positions
            for i in range(0, len(white_positions)):
                if white_positions[i][5] == '1':
                    white_states.append(new_state.pawn_actions(int(white_positions[i][0]),int(white_positions[i][2]),"+",True,selection))
                if white_positions[i][5] == '2':
                    white_states.append(new_state.knight_actions(int(white_positions[i][0]),int(white_positions[i][2]),"+",selection))
                elif white_positions[i][5] == '3':
                    white_states.append(new_state.bishop_actions(int(white_positions[i][0]),int(white_positions[i][2]),"+",selection))
                elif white_positions[i][5] == '4':
                    white_states.append(new_state.rook_actions(int(white_positions[i][0]),int(white_positions[i][2]),"+",selection))
                elif white_positions[i][5] == '5':
                    white_states.append(new_state.bishop_actions(int(white_positions[i][0]),int(white_positions[i][2]),"+",selection) + new_state.rook_actions(int(white_positions[i][0]),int(white_positions[i][2]),"+",selection))
                elif white_positions[i][5] == '6':
                    white_states.append(new_state.king_actions(int(white_positions[i][0]),int(white_positions[i][2]),"+",selection))
            #print("white states: ", white_states)
            
            for i in range(0, len(white_states)):
                for j in range(0, len(white_states[i])):
                    #if king is in one of those positions, return false, because move will be invalid 
                    if(new_state.board[int(white_states[i][j][1]),int(white_states[i][j][3])] == "-6"):
                        return True
                    #print(black_states[i][j][1])
                    #print(black_states[i][j][3])
            return False
            
    def move(self,x1,y1,x2,y2,piece_name,selection):
        #is_check = False
        new_state = ChessState(selection)
        new_state.board = np.copy(self.board)
        new_state.board[x2,y2] = self.board[x1,y1]
        new_state.board[x1,y1] = "  "
        '''if piece_name == "+1":
            try:
                if new_state.board[x1-1,y1-1] == "-6" or new_state.board[x1-1,y1+1] == "-6":
                    is_check = True
            except:
                pass
        elif piece_name == "+2":
            try:
                if new_state.board[x1-2,y1-1] == "-6" or new_state.board[x1-2,y1+1] == "-6" or new_state.board[x1-1,y1-2] == "-6" or new_state.board[x1-1,y1+2]:
                    is_check = True
            except:
                pass'''
        return new_state
def getPossibleMoves(selection,state,piece):
    total_states = []
    piece_states = []
    piece_actions = []
    if piece == "-":
        if is_unavailable("-1",selection, state) == False:
            pawn_states = state.piece_positions("-1",selection)
            piece_states.append(pawn_states)
            for i in range(0, len(pawn_states)):
                piece_actions.append(state.pawn_actions(int(pawn_states[i][1]),int(pawn_states[i][3]),"-",False,selection))
        if is_unavailable("-2",selection, state) == False:
            knight_states = state.piece_positions("-2",selection)
            piece_states.append(knight_states)
            for i in range(0, len(knight_states)):
                piece_actions.append(state.knight_actions(int(knight_states[i][1]),int(knight_states[i][3]),"-",selection))
        if is_unavailable("-3",selection, state) == False:
            bishop_states = state.piece_positions("-3",selection)
            piece_states.append(bishop_states)
            for i in range(0, len(bishop_states)):
                piece_actions.append(state.bishop_actions(int(bishop_states[i][1]),int(bishop_states[i][3]),"-",selection))
        if is_unavailable("-4",selection, state) == False:
            rook_states = state.piece_positions("-4",selection)
            piece_states.append(rook_states)
            for i in range(0, len(rook_states)):
                piece_actions.append(state.rook_actions(int(rook_states[i][1]),int(rook_states[i][3]),"-",selection))
        if is_unavailable("-5",selection, state) == False:
            queen_states = state.piece_positions("-5",selection)
            piece_states.append(queen_states)
            for i in range(0, len(queen_states)):
                piece_actions.append(state.bishop_actions(int(queen_states[i][1]),int(queen_states[i][3]),"-",selection) + state.rook_actions(int(queen_states[i][1]),int(queen_states[i][3]),"-",selection))
        if is_unavailable("-6",selection, state) == False:
            king_states = state.piece_positions("-6",selection)
            piece_states.append(king_states)
            for i in range(0, len(king_states)):
                piece_actions.append(state.king_actions(int(king_states[i][1]),int(king_states[i][3]),"-",selection))
    elif piece == "+":
        if is_unavailable("+1",selection, state) == False:
            pawn_states = state.piece_positions("+1",selection)
            piece_states.append(pawn_states)
            for i in range(0, len(pawn_states)):
                piece_actions.append(state.pawn_actions(int(pawn_states[i][1]),int(pawn_states[i][3]),"+",False,selection))
        if is_unavailable("+2",selection, state) == False:
            knight_states = state.piece_positions("+2",selection)
            piece_states.append(knight_states)
            for i in range(0, len(knight_states)):
                piece_actions.append(state.knight_actions(int(knight_states[i][1]),int(knight_states[i][3]),"+",selection))
        if is_unavailable("+3",selection, state) == False:
            bishop_states = state.piece_positions("+3",selection)
            piece_states.append(bishop_states)
            for i in range(0, len(bishop_states)):
                piece_actions.append(state.bishop_actions(int(bishop_states[i][1]),int(bishop_states[i][3]),"+",selection))
        if is_unavailable("+4",selection, state) == False:
            rook_states = state.piece_positions("+4",selection)
            piece_states.append(rook_states)
            for i in range(0, len(rook_states)):
                piece_actions.append(state.rook_actions(int(rook_states[i][1]),int(rook_states[i][3]),"+",selection))
        if is_unavailable("+5",selection, state) == False:
            queen_states = state.piece_positions("+5",selection)
            piece_states.append(queen_states)
            for i in range(0, len(queen_states)):
                piece_actions.append(state.bishop_actions(int(queen_states[i][1]),int(queen_states[i][3]),"+",selection) + state.rook_actions(int(queen_states[i][1]),int(queen_states[i][3]),"+",selection))
        if is_unavailable("+6",selection, state) == False:
            king_states = state.piece_positions("+6",selection)
            piece_states.append(king_states)
            for i in range(0, len(king_states)):
                piece_actions.append(state.king_actions(int(king_states[i][1]),int(king_states[i][3]),"+",selection))

        
    '''piece_states = [el for el in piece_states if el != []]
    piece_actions = [el for el in piece_actions if el != []]'''
    piece_states = sum(piece_states,[])
    for i in range(0, len(piece_states)):
        for j in range(0, len(piece_actions[i])):
            x1, y1 = piece_states[i][1], piece_states[i][3]
            x2, y2 = piece_actions[i][j][1], piece_actions[i][j][3]
            #print("-----------------------------------------------------")
            #print(type(state.move(int(x1),int(y1),int(x2),int(y2),"",selection)))
            #print(state.move(int(x1),int(y1),int(x2),int(y2),"",selection))
            total_states.append(state.move(int(x1),int(y1),int(x2),int(y2),"",selection))
    return total_states
        
        
    
def is_unavailable(piece,selection, state):

    if piece == "+1":
        available_pieces = []
        piece_states = state.piece_positions("+1",selection)
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.pawn_actions(int(piece_states[i][1]),int(piece_states[i][3]),"+",False,selection))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"+",selection)
                if is_threat == False:
                    #print("pawn state: ", pawn_states[i])
                    #print("pawn actions: ", pawn_actions[i][j])
                    if piece_states[i] not in available_pieces:
                        available_pieces.append(piece_states[i])
        piece_actions = [el for el in piece_actions if el != []]
        if len(available_pieces) == 0:
            return True
        else:
            return False
    elif piece == "-1":
        available_pieces = []
        piece_states = state.piece_positions("-1",selection)
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.pawn_actions(int(piece_states[i][1]),int(piece_states[i][3]),"-",False,selection))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"-",selection)
                if is_threat == False:
                    #print("pawn state: ", pawn_states[i])
                    #print("pawn actions: ", pawn_actions[i][j])
                    if piece_states[i] not in available_pieces:
                        available_pieces.append(piece_states[i])
        piece_actions = [el for el in piece_actions if el != []]
        #print(piece_actions)
        if len(available_pieces) == 0:
            return True
        else:
            return False
    elif piece == "+2":
        available_pieces = []
        piece_states = state.piece_positions("+2",selection)
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.knight_actions(int(piece_states[i][1]),int(piece_states[i][3]),"+",selection))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"+",selection)
                if is_threat == False:
                    #print("pawn state: ", pawn_states[i])
                    #print("pawn actions: ", pawn_actions[i][j])
                    if piece_states[i] not in available_pieces:
                        available_pieces.append(piece_states[i])
        piece_actions = [el for el in piece_actions if el != []]
        if len(available_pieces) == 0:
            return True
        else:
            return False
    elif piece == "-2":
        available_pieces = []
        piece_states = state.piece_positions("-2",selection)
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.knight_actions(int(piece_states[i][1]),int(piece_states[i][3]),"-",selection))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"-",selection)
                if is_threat == False:
                    #print("pawn state: ", pawn_states[i])
                    #print("pawn actions: ", pawn_actions[i][j])
                    if piece_states[i] not in available_pieces:
                        available_pieces.append(piece_states[i])
        piece_actions = [el for el in piece_actions if el != []]
        if len(available_pieces) == 0:
            return True
        else:
            return False               
    elif piece == "+3":
        available_pieces = []
        piece_states = state.piece_positions("+3",selection)
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.bishop_actions(int(piece_states[i][1]),int(piece_states[i][3]),"+",selection))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"+",selection)
                if is_threat == False:
                    #print("pawn state: ", pawn_states[i])
                    #print("pawn actions: ", pawn_actions[i][j])
                    if piece_states[i] not in available_pieces:
                        available_pieces.append(piece_states[i])
        piece_actions = [el for el in piece_actions if el != []]
        if len(available_pieces) == 0:
            return True
        else:
            return False
    elif piece == "-3":
        available_pieces = []
        piece_states = state.piece_positions("-3",selection)
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.bishop_actions(int(piece_states[i][1]),int(piece_states[i][3]),"-",selection))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"-",selection)
                if is_threat == False:
                    #print("pawn state: ", pawn_states[i])
                    #print("pawn actions: ", pawn_actions[i][j])
                    if piece_states[i] not in available_pieces:
                        available_pieces.append(piece_states[i])
        piece_actions = [el for el in piece_actions if el != []]
        if len(available_pieces) == 0:
            return True
        else:
            return False
    elif piece == "+4":
        available_pieces = []
        piece_states = state.piece_positions("+4",selection)
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.rook_actions(int(piece_states[i][1]),int(piece_states[i][3]),"+",selection))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"+",selection)
                if is_threat == False:
                    #print("pawn state: ", pawn_states[i])
                    #print("pawn actions: ", pawn_actions[i][j])
                    if piece_states[i] not in available_pieces:
                        available_pieces.append(piece_states[i])
        piece_actions = [el for el in piece_actions if el != []]
        if len(available_pieces) == 0:
            return True
        else:
            return False 
    elif piece == "-4":
        available_pieces = []
        piece_states = state.piece_positions("-4",selection)
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.rook_actions(int(piece_states[i][1]),int(piece_states[i][3]),"-",selection))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"-",selection)
                if is_threat == False:
                    #print("pawn state: ", pawn_states[i])
                    #print("pawn actions: ", pawn_actions[i][j])
                    if piece_states[i] not in available_pieces:
                        available_pieces.append(piece_states[i])
        piece_actions = [el for el in piece_actions if el != []]
        if len(available_pieces) == 0:
            return True
        else:
            return False               
    elif piece == "+5":
        available_pieces = []
        piece_states = state.piece_positions("+5",selection)
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.bishop_actions(int(piece_states[i][1]),int(piece_states[i][3]),"+",selection) + state.rook_actions(int(piece_states[i][1]),int(piece_states[i][3]),"+",selection))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"+",selection)
                if is_threat == False:
                    #print("pawn state: ", pawn_states[i])
                    #print("pawn actions: ", pawn_actions[i][j])
                    if piece_states[i] not in available_pieces:
                        available_pieces.append(piece_states[i])
        piece_actions = [el for el in piece_actions if el != []]
        if len(available_pieces) == 0:
            return True
        else:
            return False
    elif piece == "-5":
        available_pieces = []
        piece_states = state.piece_positions("-5",selection)
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.bishop_actions(int(piece_states[i][1]),int(piece_states[i][3]),"-",selection) + state.rook_actions(int(piece_states[i][1]),int(piece_states[i][3]),"-",selection))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"-",selection)
                if is_threat == False:
                    #print("pawn state: ", pawn_states[i])
                    #print("pawn actions: ", pawn_actions[i][j])
                    if piece_states[i] not in available_pieces:
                        available_pieces.append(piece_states[i])
        piece_actions = [el for el in piece_actions if el != []]
        if len(available_pieces) == 0:
            return True
        else:
            return False
    elif piece == "+6":
        available_pieces = []
        piece_states = state.piece_positions("+6",selection)
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.king_actions(int(piece_states[i][1]),int(piece_states[i][3]),"+",selection))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"+",selection)
                if is_threat == False:
                    #print("pawn state: ", pawn_states[i])
                    #print("pawn actions: ", pawn_actions[i][j])
                    if piece_states[i] not in available_pieces:
                        available_pieces.append(piece_states[i])
        piece_actions = [el for el in piece_actions if el != []]
        if len(available_pieces) == 0:
            return True
        else:
            return False
    elif piece == "-6":
        available_pieces = []
        piece_states = state.piece_positions("-6",selection)
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.king_actions(int(piece_states[i][1]),int(piece_states[i][3]),"-",selection))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"-",selection)
                if is_threat == False:
                    #print("pawn state: ", pawn_states[i])
                    #print("pawn actions: ", pawn_actions[i][j])
                    if piece_states[i] not in available_pieces:
                        available_pieces.append(piece_states[i])
        piece_actions = [el for el in piece_actions if el != []]
        if len(available_pieces) == 0:
            return True
        else:
            return False          
def initial_state(selection):
    if selection == '1':
        state = ChessState(selection)
        state.board[0,0] = state.board[0,7] = "-4"
        state.board[7,0] = state.board[7,7] = "+4"
        state.board[0,1] = state.board[0,6] = "-2"
        state.board[7,1] = state.board[7,6] = "+2"
        state.board[0,2] = state.board[0,5] = "-3"
        state.board[7,2] = state.board[7,5] = "+3"
        state.board[0,3] = "-5"
        state.board[7,3] = "+5"
        state.board[0,4] = "-6"
        state.board[7,4] = "+6"
        state.board[1,0:8] = "-1"
        state.board[6,0:8] = "+1"
        
        for i in range(0,3):
            wallx = random.randint(2,5)
            wally = random.randint(0,7)
            while state.board[wallx,wally] == "WL":
                wallx = random.randint(2,5)
                wally = random.randint(0,7) 
            state.board[wallx,wally] = "WL"
        return state
    elif selection == '2':
        state = ChessState(selection)
        state.board[0,0] = state.board[0,6] = "-4"
        state.board[7,0] = state.board[7,6] = "+4"
        state.board[0,1] = state.board[0,5] = "-2"
        state.board[7,1] = state.board[7,5] = "+2"
        state.board[0,2] = state.board[0,4] = "-3"
        state.board[7,2] = state.board[7,4] = "+3"
        state.board[0,3] = "-6"
        state.board[7,3] = "+6"
        state.board[1,0:7] = "-1"
        state.board[6,0:7] = "+1"
        
        for i in range(0,3):
            wallx = random.randint(2,5)
            wally = random.randint(0,6)
            while state.board[wallx,wally] == "WL":
                wallx = random.randint(2,5)
                wally = random.randint(0,6) 
            state.board[wallx,wally] = "WL"
        return state
    elif selection == '3':
        state = ChessState(selection)
        state.board[0,0] = state.board[0,5] = "-3"
        state.board[7,0] = state.board[7,5] = "+3"
        state.board[0,1] = state.board[0,4] = "-2"
        state.board[7,1] = state.board[7,4] = "+2"
        state.board[0,2] = "-5"
        state.board[7,2] = "+5"
        state.board[0,3] = "-6"
        state.board[7,3] = "+6"
        state.board[1,0:6] = "-1"
        state.board[6,0:6] = "+1"
        
        for i in range(0,3):
            wallx = random.randint(2,5)
            wally = random.randint(0,5)
            while state.board[wallx,wally] == "WL":
                wallx = random.randint(2,5)
                wally = random.randint(0,5) 
            state.board[wallx,wally] = "WL"
        return state
    elif selection == '4':
        state = ChessState(selection)
        state.board[0,0] = state.board[0,4] = "-3"
        state.board[7,0] = state.board[7,4] = "+3"
        state.board[0,1] = state.board[0,3] = "-2"
        state.board[7,1] = state.board[7,3] = "+2"
        state.board[0,2] = "-6"
        state.board[7,2] = "+6"
        state.board[1,0:5] = "-1"
        state.board[6,0:5] = "+1"
        
        for i in range(0,3):
            wallx = random.randint(2,5)
            wally = random.randint(0,4)
            while state.board[wallx,wally] == "WL":
                wallx = random.randint(2,5)
                wally = random.randint(0,4) 
            state.board[wallx,wally] = "WL"
        return state
    elif selection == '5':
        state = ChessState(selection)
        state.board[0,0] = state.board[0,3] = "-3"
        state.board[7,0] = state.board[7,3] = "+3"
        state.board[0,1] = "-5"
        state.board[7,1] = "+5"
        state.board[0,2] = "-6"
        state.board[7,2] = "+6"
        state.board[1,0:4] = "-1"
        state.board[6,0:4] = "+1"
        
        for i in range(0,3):
            wallx = random.randint(2,5)
            wally = random.randint(0,3)
            while state.board[wallx,wally] == "WL":
                wallx = random.randint(2,5)
                wally = random.randint(0,3) 
            state.board[wallx,wally] = "WL"
        return state


def encode(state):
    
    onehot = tr.zeros(3, state.board.shape[0], state.board.shape[1])
    
    for i in range(state.board.shape[0]):
        for j in range(state.board.shape[1]):
            if state.board[i, j][0] == ' ':
                onehot[0, i, j] = 1.
                
            if state.board[i, j][0] == '-':
                onehot[1, i, j] = 1.
            
            if state.board[i, j][0] == '+':
                onehot[2, i, j] = 1.
                
    #print("onehot: ",onehot)
    return onehot



if __name__ == "__main__":
    while True:
        board = input("Choose a board size:('1'= 8x8, '2' = 8x7, '3' = 8x6, '4' = 8x5, '5' = 8x4, 'q' = quit)")
        if board == "q":
            break
        elif board == "1" or board == "2" or board == "3" or board == "4" or board == "5":
            state = initial_state(board)
            break
        else:
            print("Wrong input! Please try again.")
    
    #state = initial_state()
    selection = board
    if selection == "q":
        sys.exit()
        
    iterator = 0
    #isCheck = False
    isMoved = False
    is_check = False
    
    while True:
        if iterator%2 == 0:
            #print("iterator: ", iterator)
            print("---------------------")
            print("White player's turn")
            print("Current state:")
            print(str(state))
            #Check if it is a checkmate
            pawns_list = is_unavailable("+1",selection, state)
            knights_list = is_unavailable("+2",selection, state)
            bishops_list = is_unavailable("+3",selection, state)
            rooks_list = is_unavailable("+4",selection, state)
            queens_list = is_unavailable("+5",selection, state)
            kings_list = is_unavailable("+6",selection, state)
            if pawns_list and knights_list and bishops_list and rooks_list and queens_list and kings_list:
                print("Checkmate! Black wins.")
            a = input("Enter a chess piece('+1'=pawn,'+2'=knight,'+3'=bishop,'+4'=rook,'+5'=queen,'+6'=king,'q'=quit):")
            if a == "q": break
            elif a == "+1":
                while True:
                    available_pawns = []
                    pawn_states = state.piece_positions("+1",selection)
                    pawn_actions = []
                    for i in range(0, len(pawn_states)):
                        pawn_actions.append(state.pawn_actions(int(pawn_states[i][1]),int(pawn_states[i][3]),"+",False,selection))
                    #print(pawn_actions)
                    for i in range(0, len(pawn_actions)):
                        for j in range(0, len(pawn_actions[i])):
                            is_threat = state.is_king_threated(int(pawn_states[i][1]),int(pawn_states[i][3]),int(pawn_actions[i][j][1]), int(pawn_actions[i][j][3]),"+",selection)
                            if is_threat == False:
                                #print("pawn state: ", pawn_states[i])
                                #print("pawn actions: ", pawn_actions[i][j])
                                if pawn_states[i] not in available_pawns:
                                    available_pawns.append(pawn_states[i])
                            
                    #print("available pawns: ", available_pawns)
                    pawn_actions = [el for el in pawn_actions if el != []]
                    #print("available actions: ", pawn_actions)  
                                                             
                    print("-----------------------------------------------------")
                    if len(available_pawns) == 0:
                        print("There are no available pawns to play!")
                        iterator = iterator+1
                        break
                    print("Enter x and y coordinates to select a specific pawn:")
                    print("Available pawns are: ")
                    print(available_pawns)
                    try:
                        px, py = int(input('x: ')), int(input('y: '))
                        try:
                            if state.board[px,py] == "+1":
                                while True:
                                    loc_pawn = "(" + str(px) + "," + str(py) + ")"
                                    print("Select x and y coordinates to move pawn located in " + loc_pawn)
                                    print("Available actions are: ")
                                    idx = available_pawns.index(loc_pawn)                           
                                    print(pawn_actions[idx])
                                    mx, my = int(input('x: ')), int(input('y: '))
                                    action_pawn = "(" + str(mx) + "," + str(my) + ")"
                                    if action_pawn in pawn_actions[idx]:
                                        state = state.move(px,py,mx,my,"+1",selection)
                                        isMoved = True
                                        break
                                    else:
                                        print("Invalid action!")
                                #if player is moved, break the loop and make moved false again
                                if isMoved:
                                    isMoved = False
                                    break
                            else:
                                print("Invalid input!")
                        except:
                            print("Input index is out of bounds!")
                    except:
                        print("Invalid type! please enter a number for specified coordinate")
                
            elif a == "+2":
                while True:
                    available_knights = []
                    knight_states = state.piece_positions("+2",selection)
                    knight_actions = []
                    for i in range(0, len(knight_states)):
                        knight_actions.append(state.knight_actions(int(knight_states[i][1]),int(knight_states[i][3]),"+",selection))
                    #print(pawn_actions)
                    for i in range(0, len(knight_actions)):
                        for j in range(0, len(knight_actions[i])):
                            is_threat = state.is_king_threated(int(knight_states[i][1]),int(knight_states[i][3]),int(knight_actions[i][j][1]), int(knight_actions[i][j][3]),"+",selection)
                            if is_threat == False:
                                #print("knight state: ", knight_states[i])
                                #print("knight actions: ", knight_actions[i][j])
                                if knight_states[i] not in available_knights:
                                    available_knights.append(knight_states[i])
                            
                    #print("available knights: ", available_knights)
                    knight_actions = [el for el in knight_actions if el != []]
                    #print("available actions: ", knight_actions)  
                                                             
                    print("-----------------------------------------------------")
                    if len(available_knights) == 0:
                        print("There are no available knights to play!")
                        iterator = iterator+1
                        break
                    print("Enter x and y coordinates to select a specific knight:")
                    print("Available knights are: ")
                    print(available_knights)
                    try:
                        nx, ny = int(input('x: ')), int(input('y: '))
                        try:
                            if state.board[nx,ny] == "+2":
                                while True:
                                    loc_knight = "(" + str(nx) + "," + str(ny) + ")"
                                    print("Select x and y coordinates to move knight located in " + loc_knight)
                                    print("Available actions are: ")
                                    idx = available_knights.index(loc_knight)                           
                                    print(knight_actions[idx])
                                    mx, my = int(input('x: ')), int(input('y: '))
                                    action_knight = "(" + str(mx) + "," + str(my) + ")"
                                    if action_knight in knight_actions[idx]:
                                        state = state.move(nx,ny,mx,my,"+2",selection)
                                        isMoved = True
                                        break
                                    else:
                                        print("Invalid action!")
                                #if player is moved, break the loop and make moved false again
                                if isMoved:
                                    isMoved = False
                                    break
                            else:
                                print("Invalid input!")
                        except:
                            print("Input index is out of bounds!")
                    except:
                        print("Invalid type! please enter a number for specified coordinate")
                
            elif a == "+3":
                while True:
                    available_bishops = []
                    bishop_states = state.piece_positions("+3",selection)
                    bishop_actions = []
                    for i in range(0, len(bishop_states)):
                        bishop_actions.append(state.bishop_actions(int(bishop_states[i][1]),int(bishop_states[i][3]),"+",selection))
                    #print(bishop_actions)
                    for i in range(0, len(bishop_actions)):
                        for j in range(0, len(bishop_actions[i])):
                            is_threat = state.is_king_threated(int(bishop_states[i][1]),int(bishop_states[i][3]),int(bishop_actions[i][j][1]), int(bishop_actions[i][j][3]),"+",selection)
                            if is_threat == False:
                                #print("bishop state: ", bishop_states[i])
                                #print("bishop actions: ", bishop_actions[i][j])
                                if bishop_states[i] not in available_bishops:
                                    available_bishops.append(bishop_states[i])
                            
                    #print("available bishops: ", available_bishops)
                    bishop_actions = [el for el in bishop_actions if el != []]
                    #print("available actions: ", bishop_actions)  
                                                             
                    print("-----------------------------------------------------")
                    if len(available_bishops) == 0:
                        print("There are no available bishops to play!")
                        iterator = iterator+1
                        break
                    print("Enter x and y coordinates to select a specific bishop:")
                    print("Available bishops are: ")
                    print(available_bishops)
                    try:
                        bx, by = int(input('x: ')), int(input('y: '))
                        try:
                            if state.board[bx,by] == "+3":
                                while True:
                                    loc_bishop = "(" + str(bx) + "," + str(by) + ")"
                                    print("Select x and y coordinates to move bishop located in " + loc_bishop)
                                    print("Available actions are: ")
                                    idx = available_bishops.index(loc_bishop)                           
                                    print(bishop_actions[idx])
                                    mx, my = int(input('x: ')), int(input('y: '))
                                    action_bishop = "(" + str(mx) + "," + str(my) + ")"
                                    if action_bishop in bishop_actions[idx]:
                                        state = state.move(bx,by,mx,my,"+3",selection)
                                        isMoved = True
                                        break
                                    else:
                                        print("Invalid action!")
                                #if player is moved, break the loop and make moved false again
                                if isMoved:
                                    isMoved = False
                                    break
                            else:
                                print("Invalid input!")
                        except:
                            print("Input index is out of bounds!") 
                    except:
                        print("Invalid type! please enter a number for specified coordinate")
                
            elif a == "+4":
                while True:
                    available_rooks = []
                    rook_states = state.piece_positions("+4",selection)
                    rook_actions = []
                    for i in range(0, len(rook_states)):
                        rook_actions.append(state.rook_actions(int(rook_states[i][1]),int(rook_states[i][3]),"+",selection))
                    #print(rook_actions)
                    for i in range(0, len(rook_actions)):
                        for j in range(0, len(rook_actions[i])):
                            is_threat = state.is_king_threated(int(rook_states[i][1]),int(rook_states[i][3]),int(rook_actions[i][j][1]), int(rook_actions[i][j][3]),"+",selection)
                            if is_threat == False:
                                #print("rook state: ", rook_states[i])
                                #print("rook actions: ", rook_actions[i][j])
                                if rook_states[i] not in available_rooks:
                                    available_rooks.append(rook_states[i])
                            
                    #print("available rooks: ", available_rooks)
                    rook_actions = [el for el in rook_actions if el != []]
                    #print("available actions: ", rook_actions)  
                                                             
                    print("-----------------------------------------------------")
                    if len(available_rooks) == 0:
                        print("There are no available rooks to play!")
                        iterator = iterator+1
                        break
                    print("Enter x and y coordinates to select a specific rook:")
                    print("Available rooks are: ")
                    print(available_rooks)
                    try:
                        rx, ry = int(input('x: ')), int(input('y: '))
                        try:
                            if state.board[rx,ry] == "+4":
                                while True:
                                    loc_rook = "(" + str(rx) + "," + str(ry) + ")"
                                    print("Select x and y coordinates to move rook located in " + loc_rook)
                                    print("Available actions are: ")
                                    idx = available_rooks.index(loc_rook)                           
                                    print(rook_actions[idx])
                                    mx, my = int(input('x: ')), int(input('y: '))
                                    action_rook = "(" + str(mx) + "," + str(my) + ")"
                                    if action_rook in rook_actions[idx]:
                                        state = state.move(rx,ry,mx,my,"+4",selection)
                                        isMoved = True
                                        break
                                    else:
                                        print("Invalid action!")
                                #if player is moved, break the loop and make moved false again
                                if isMoved:
                                    isMoved = False
                                    break
                            else:
                                print("Invalid input!")
                        except:
                            print("Input index is out of bounds!")    
                    except:
                        print("Invalid type! please enter a number for specified coordinate")
                
            elif a == "+5":
                while True:
                    available_queens = []
                    queen_states = state.piece_positions("+5",selection)
                    queen_actions = []
                    for i in range(0, len(queen_states)):
                        queen_actions.append(state.bishop_actions(int(queen_states[i][1]),int(queen_states[i][3]),"+",selection) + state.rook_actions(int(queen_states[i][1]),int(queen_states[i][3]),"+",selection))
                    #print(queen_actions)
                    for i in range(0, len(queen_actions)):
                        for j in range(0, len(queen_actions[i])):
                            is_threat = state.is_king_threated(int(queen_states[i][1]),int(queen_states[i][3]),int(queen_actions[i][j][1]), int(queen_actions[i][j][3]),"+",selection)
                            if is_threat == False:
                                #print("queen state: ", queen_states[i])
                                #print("queen actions: ", queen_actions[i][j])
                                if queen_states[i] not in available_queens:
                                    available_queens.append(queen_states[i])
                            
                    #print("available queens: ", available_queens)
                    queen_actions = [el for el in queen_actions if el != []]
                    #print("available actions: ", queen_actions)  
                                                             
                    print("-----------------------------------------------------")
                    if len(available_queens) == 0:
                        print("There are no available queens to play!")
                        iterator = iterator+1
                        break
                    print("Enter x and y coordinates to select a specific queen:")
                    print("Available queens are: ")
                    print(available_queens)
                    try:
                        qx, qy = int(input('x: ')), int(input('y: '))
                        try:
                            if state.board[qx,qy] == "+5":
                                while True:
                                    loc_queen = "(" + str(qx) + "," + str(qy) + ")"
                                    print("Select x and y coordinates to move queen located in " + loc_queen)
                                    print("Available actions are: ")
                                    idx = available_queens.index(loc_queen)                           
                                    print(queen_actions[idx])
                                    mx, my = int(input()), int(input())
                                    action_queen = "(" + str(mx) + "," + str(my) + ")"
                                    if action_queen in queen_actions[idx]:
                                        state = state.move(qx,qy,mx,my,"+5",selection)
                                        isMoved = True
                                        break
                                    else:
                                        print("Invalid action!")
                                #if player is moved, break the loop and make moved false again
                                if isMoved:
                                    isMoved = False
                                    break
                            else:
                                print("Invalid input!")
                        except:
                            print("Input index is out of bounds!")     
                    except:
                        print("Invalid type! please enter a number for specified coordinate")                
            
            elif a == "+6":
                while True:
                    available_kings = []
                    king_states = state.piece_positions("+6",selection)
                    king_actions = []
                    for i in range(0, len(king_states)):
                        king_actions.append(state.king_actions(int(king_states[i][1]),int(king_states[i][3]),"+",selection))
                    #print(king_actions)
                    for i in range(0, len(king_actions)):
                        for j in range(0, len(king_actions[i])):
                            is_threat = state.is_king_threated(int(king_states[i][1]),int(king_states[i][3]),int(king_actions[i][j][1]), int(king_actions[i][j][3]),"+",selection)
                            if is_threat == False:
                                #print("king state: ", king_states[i])
                                #print("king actions: ", king_actions[i][j])
                                if king_states[i] not in available_kings:
                                    available_kings.append(king_states[i])
                            
                    #print("available kings: ", available_kings)
                    king_actions = [el for el in king_actions if el != []]
                    #print("available actions: ", king_actions)  
                                                             
                    print("-----------------------------------------------------")
                    if len(available_kings) == 0:
                        print("There are no available kings to play!")
                        iterator = iterator+1
                        break
                    print("Enter x and y coordinates to select a specific king:")
                    print("Available kings are: ")
                    print(available_kings)
                    try:
                        kx, ky = int(input('x: ')), int(input('y: '))
                        try:
                            if state.board[kx,ky] == "+6":
                                while True:
                                    loc_king = "(" + str(kx) + "," + str(ky) + ")"
                                    print("Select x and y coordinates to move king located in " + loc_king)
                                    print("Available actions are: ")
                                    idx = available_kings.index(loc_king)                           
                                    print(king_actions[idx])
                                    mx, my = int(input('x: ')), int(input('y: '))
                                    action_king = "(" + str(mx) + "," + str(my) + ")"
                                    if action_king in king_actions[idx]:
                                        state = state.move(kx,ky,mx,my,"+6",selection)
                                        isMoved = True
                                        break
                                    else:
                                        print("Invalid action!")
                                #if player is moved, break the loop and make moved false again
                                if isMoved:
                                    isMoved = False
                                    break
                            else:
                                print("Invalid input!")
                        except:
                            print("Input index is out of bounds!")    
                    except:
                        print("Invalid type! please enter a number for specified coordinate")
                
            else:
                print("Invalid input. Please choose again!")
                iterator = iterator+1
                
            iterator = iterator+1
        else:
            print("---------------------")
            print("Current state:")
            print(str(state))
            print("---------------------")
            print("Black player(AI)'s turn")
            #print("Ai is playing...")
            
            #Check if it is a checkmate
            pawns_list = is_unavailable("-1",selection, state)
            knights_list = is_unavailable("-2",selection, state)
            bishops_list = is_unavailable("-3",selection, state)
            rooks_list = is_unavailable("-4",selection, state)
            queens_list = is_unavailable("-5",selection, state)
            kings_list = is_unavailable("-6",selection, state)
            if pawns_list and knights_list and bishops_list and rooks_list and queens_list and kings_list:
                print("Checkmate! White wins.")
                break
            ai = input("Choose an ai:('1'= Tree-based AI, '2' = Baseline AI, '3' = NN-based AI, 'q' = quit)")
            if ai == 'q': break
            elif ai == '1':
                print("Tree-based AI is playing...")
                max_depth = 1
                AI = MinimaxEngine(max_depth)
                new_state, score = AI.bestAction(state,selection,True, '-')
                #print("Current state: ", new_state)
                state = new_state
            elif ai == '2':
                print("Baseline AI is playing..")
                total_states = getPossibleMoves(selection,state, '-')
                new_state = random.choice(total_states)
                state = new_state
            elif ai == '3':
                print("NN-based AI is playing..")
                
                nn = input("Choose an nn:('1'= Linear Model, '2' = Convolutional Model)")
                if nn == '1':
                    net = cn.ChessNet1(selection)
                    net.load_state_dict(tr.load("linear_model/model%d.pth" % int(selection)))
                elif nn == '2':
                    
                    net = cn.ChessNet2(selection)
                    net.load_state_dict(tr.load("convolutional_model/model%d.pth" % int(selection)))              

                with tr.no_grad():
                    x = tr.stack(tuple(map(encode, [child for child in getPossibleMoves(selection, state, '-')])))
                    y = net(x)
                    probs = tr.softmax(y.flatten(), dim=0)
                    a = np.random.choice(len(probs), p=probs.detach().numpy())
                    new_state = getPossibleMoves(selection, state, '-')[a]
                state = new_state
            else:
                print("Wrong input!")
            '''print("Total possible states: ")
            for s in total_states:
                print("------------------------------")
                print(str(s))'''
            
            '''a = input("Enter a chess piece('-1'=pawn,'-2'=knight,'-3'=bishop,'-4'=rook,'-5'=queen,'-6'=king,'q'=quit):")
            if a == "q": break
            elif a == "-1":
                while True:
                    available_pawns = []
                    pawn_states = state.piece_positions("-1",selection)
                    pawn_actions = []
                    for i in range(0, len(pawn_states)):
                        pawn_actions.append(state.pawn_actions(int(pawn_states[i][1]),int(pawn_states[i][3]),"-",False,selection))
                    #print(pawn_actions)
                    for i in range(0, len(pawn_actions)):
                        for j in range(0, len(pawn_actions[i])):
                            is_threat = state.is_king_threated(int(pawn_states[i][1]),int(pawn_states[i][3]),int(pawn_actions[i][j][1]), int(pawn_actions[i][j][3]),"-",selection)
                            if is_threat == False:
                                #print("pawn state: ", pawn_states[i])
                                #print("pawn actions: ", pawn_actions[i][j])
                                if pawn_states[i] not in available_pawns:
                                    available_pawns.append(pawn_states[i])
                            
                    #print("available pawns: ", available_pawns)
                    pawn_actions = [el for el in pawn_actions if el != []]
                    #print("available actions: ", pawn_actions)  
                                                             
                    print("-----------------------------------------------------")
                    if len(available_pawns) == 0:
                        print("There are no available pawns to play!")
                        iterator = iterator+1
                        break
                    print("Enter x and y coordinates to select a specific pawn:")
                    print("Available pawns are: ")
                    print(available_pawns)
                    try:
                        px, py = int(input('x: ')), int(input('y: '))
                        try:
                            if state.board[px,py] == "-1":
                                while True:
                                    loc_pawn = "(" + str(px) + "," + str(py) + ")"
                                    print("Select x and y coordinates to move pawn located in " + loc_pawn)
                                    print("Available actions are: ")
                                    idx = available_pawns.index(loc_pawn)                           
                                    print(pawn_actions[idx])
                                    mx, my = int(input('x: ')), int(input('y: '))
                                    action_pawn = "(" + str(mx) + "," + str(my) + ")"
                                    if action_pawn in pawn_actions[idx]:
                                        state = state.move(px,py,mx,my,"-1",selection)
                                        isMoved = True
                                        break
                                    else:
                                        print("Invalid action!")
                                #if player is moved, break the loop and make moved false again
                                if isMoved:
                                    isMoved = False
                                    break
                            else:
                                print("Invalid input!")
                        except:
                            print("Input index is out of bounds!")    
                    except:
                        print("Invalid type! please enter a number for specified coordinate")
                    
            elif a == "-2":
                while True:
                    available_knights = []
                    knight_states = state.piece_positions("-2",selection)
                    knight_actions = []
                    for i in range(0, len(knight_states)):
                        knight_actions.append(state.knight_actions(int(knight_states[i][1]),int(knight_states[i][3]),"-",selection))
                    #print(knight_actions)
                    for i in range(0, len(knight_actions)):
                        for j in range(0, len(knight_actions[i])):
                            is_threat = state.is_king_threated(int(knight_states[i][1]),int(knight_states[i][3]),int(knight_actions[i][j][1]), int(knight_actions[i][j][3]),"-",selection)
                            if is_threat == False:
                                #print("knight state: ", knight_states[i])
                                #print("knight actions: ", knight_actions[i][j])
                                if knight_states[i] not in available_knights:
                                    available_knights.append(knight_states[i])
                            
                    #print("available knights: ", available_knights)
                    knight_actions = [el for el in knight_actions if el != []]
                    #print("available actions: ", knight_actions)  
                                                             
                    print("-----------------------------------------------------")
                    if len(available_knights) == 0:
                        print("There are no available knights to play!")
                        iterator = iterator+1
                        break
                    print("Enter x and y coordinates to select a specific knight:")
                    print("Available knights are: ")
                    print(available_knights)
                    try:
                        nx, ny = int(input('x: ')), int(input('y: '))
                        try:
                            if state.board[nx,ny] == "-2":
                                while True:
                                    loc_knight = "(" + str(nx) + "," + str(ny) + ")"
                                    print("Select x and y coordinates to move knight located in " + loc_knight)
                                    print("Available actions are: ")
                                    idx = available_knights.index(loc_knight)                           
                                    print(knight_actions[idx])
                                    mx, my = int(input('x: ')), int(input('y: '))
                                    action_knight = "(" + str(mx) + "," + str(my) + ")"
                                    if action_knight in knight_actions[idx]:
                                        state = state.move(nx,ny,mx,my,"-2",selection)
                                        isMoved = True
                                        break
                                    else:
                                        print("Invalid action!")
                                #if player is moved, break the loop and make moved false again
                                if isMoved:
                                    isMoved = False
                                    break
                            else:
                                print("Invalid input!")
                        except:
                            print("Input index is out of bounds!")    
                    except:
                        print("Invalid type! please enter a number for specified coordinate")    
                
            elif a == "-3":
                while True:
                    available_bishops = []
                    bishop_states = state.piece_positions("-3",selection)
                    bishop_actions = []
                    for i in range(0, len(bishop_states)):
                        bishop_actions.append(state.bishop_actions(int(bishop_states[i][1]),int(bishop_states[i][3]),"-",selection))
                    #print(bishop_actions)
                    for i in range(0, len(bishop_actions)):
                        for j in range(0, len(bishop_actions[i])):
                            is_threat = state.is_king_threated(int(bishop_states[i][1]),int(bishop_states[i][3]),int(bishop_actions[i][j][1]), int(bishop_actions[i][j][3]),"-",selection)
                            if is_threat == False:
                                #print("bishop state: ", bishop_states[i])
                                #print("bishop actions: ", bishop_actions[i][j])
                                if bishop_states[i] not in available_bishops:
                                    available_bishops.append(bishop_states[i])
                            
                    #print("available bishops: ", available_bishops)
                    bishop_actions = [el for el in bishop_actions if el != []]
                    #print("available actions: ", bishop_actions)  
                                                             
                    print("-----------------------------------------------------")
                    if len(available_bishops) == 0:
                        print("There are no available bishops to play!")
                        iterator = iterator+1
                        break
                    print("Enter x and y coordinates to select a specific bishop:")
                    print("Available bishops are: ")
                    print(available_bishops)
                    try:
                        bx, by = int(input('x: ')), int(input('y: '))
                        try:
                            if state.board[bx,by] == "-3":
                                while True:
                                    loc_bishop = "(" + str(bx) + "," + str(by) + ")"
                                    print("Select x and y coordinates to move bishop located in " + loc_bishop)
                                    print("Available actions are: ")
                                    idx = available_bishops.index(loc_bishop)                           
                                    print(bishop_actions[idx])
                                    mx, my = int(input('x: ')), int(input('y: '))
                                    action_bishop = "(" + str(mx) + "," + str(my) + ")"
                                    if action_bishop in bishop_actions[idx]:
                                        state = state.move(bx,by,mx,my,"-3",selection)
                                        isMoved = True
                                        break
                                    else:
                                        print("Invalid action!")
                                #if player is moved, break the loop and make moved false again
                                if isMoved:
                                    isMoved = False
                                    break
                            else:
                                print("Invalid input!")
                        except:
                            print("Input index is out of bounds!") 
                    except:
                        print("Invalid type! please enter a number for specified coordinate")
                
            elif a == "-4":
                while True:
                    available_rooks = []
                    rook_states = state.piece_positions("-4",selection)
                    rook_actions = []
                    for i in range(0, len(rook_states)):
                        rook_actions.append(state.rook_actions(int(rook_states[i][1]),int(rook_states[i][3]),"-",selection))
                    #print(rook_actions)
                    for i in range(0, len(rook_actions)):
                        for j in range(0, len(rook_actions[i])):
                            is_threat = state.is_king_threated(int(rook_states[i][1]),int(rook_states[i][3]),int(rook_actions[i][j][1]), int(rook_actions[i][j][3]),"-",selection)
                            if is_threat == False:
                                #print("rook state: ", rook_states[i])
                                #print("rook actions: ", rook_actions[i][j])
                                if rook_states[i] not in available_rooks:
                                    available_rooks.append(rook_states[i])
                            
                    #print("available rooks: ", available_rooks)
                    rook_actions = [el for el in rook_actions if el != []]
                    #print("available actions: ", rook_actions)  
                                                             
                    print("-----------------------------------------------------")
                    if len(available_rooks) == 0:
                        print("There are no available rooks to play!")
                        iterator = iterator+1
                        break
                    print("Enter x and y coordinates to select a specific rook:")
                    print("Available rooks are: ")
                    print(available_rooks)
                    try:
                        rx, ry = int(input('x: ')), int(input('y: '))
                        try:
                            if state.board[rx,ry] == "-4":
                                while True:
                                    loc_rook = "(" + str(rx) + "," + str(ry) + ")"
                                    print("Select x and y coordinates to move rook located in " + loc_rook)
                                    print("Available actions are: ")
                                    idx = available_rooks.index(loc_rook)                           
                                    print(rook_actions[idx])
                                    mx, my = int(input('x: ')), int(input('y: '))
                                    action_rook = "(" + str(mx) + "," + str(my) + ")"
                                    if action_rook in rook_actions[idx]:
                                        state = state.move(rx,ry,mx,my,"-4",selection)
                                        isMoved = True
                                        break
                                    else:
                                        print("Invalid action!")
                                #if player is moved, break the loop and make moved false again
                                if isMoved:
                                    isMoved = False
                                    break
                            else:
                                print("Invalid input!")
                        except:
                            print("Input index is out of bounds!")    
                    except:
                        print("Invalid type! please enter a number for specified coordinate")
                
            elif a == "-5":
                while True:
                    available_queens = []
                    queen_states = state.piece_positions("-5",selection)
                    queen_actions = []
                    for i in range(0, len(queen_states)):
                        queen_actions.append(state.bishop_actions(int(queen_states[i][1]),int(queen_states[i][3]),"-",selection) + state.rook_actions(int(queen_states[i][1]),int(queen_states[i][3]),"-",selection))
                    #print(queen_actions)
                    for i in range(0, len(queen_actions)):
                        for j in range(0, len(queen_actions[i])):
                            is_threat = state.is_king_threated(int(queen_states[i][1]),int(queen_states[i][3]),int(queen_actions[i][j][1]), int(queen_actions[i][j][3]),"-",selection)
                            if is_threat == False:
                                #print("queen state: ", queen_states[i])
                                #print("queen actions: ", queen_actions[i][j])
                                if queen_states[i] not in available_queens:
                                    available_queens.append(queen_states[i])
                            
                    #print("available queens: ", available_queens)
                    queen_actions = [el for el in queen_actions if el != []]
                    #print("available actions: ", queen_actions)  
                                                             
                    print("-----------------------------------------------------")
                    if len(available_queens) == 0:
                        print("There are no available queens to play!")
                        iterator = iterator+1
                        break
                    print("Enter x and y coordinates to select a specific queen:")
                    print("Available queens are: ")
                    print(available_queens)
                    try:
                        qx, qy = int(input('x: ')), int(input('y: '))
                        try:
                            if state.board[qx,qy] == "-5":
                                while True:
                                    loc_queen = "(" + str(qx) + "," + str(qy) + ")"
                                    print("Select x and y coordinates to move queen located in " + loc_queen)
                                    print("Available actions are: ")
                                    idx = available_queens.index(loc_queen)                           
                                    print(queen_actions[idx])
                                    mx, my = int(input('x: ')), int(input('y: '))
                                    action_queen = "(" + str(mx) + "," + str(my) + ")"
                                    if action_queen in queen_actions[idx]:
                                        state = state.move(qx,qy,mx,my,"-5",selection)
                                        isMoved = True
                                        break
                                    else:
                                        print("Invalid action!")
                                #if player is moved, break the loop and make moved false again
                                if isMoved:
                                    isMoved = False
                                    break
                            else:
                                print("Invalid input!")
                        except:
                            print("Input index is out of bounds!")    
                    except:
                        print("Invalid type! please enter a number for specified coordinate")                
            
            elif a == "-6":
                while True:
                    available_kings = []
                    king_states = state.piece_positions("-6",selection)
                    king_actions = []
                    for i in range(0, len(king_states)):
                        king_actions.append(state.king_actions(int(king_states[i][1]),int(king_states[i][3]),"-",selection))
                    #print(king_actions)
                    for i in range(0, len(king_actions)):
                        for j in range(0, len(king_actions[i])):
                            is_threat = state.is_king_threated(int(king_states[i][1]),int(king_states[i][3]),int(king_actions[i][j][1]), int(king_actions[i][j][3]),"-",selection)
                            if is_threat == False:
                                #print("king state: ", king_states[i])
                                #print("king actions: ", king_actions[i][j])
                                if king_states[i] not in available_kings:
                                    available_kings.append(king_states[i])
                            
                    #print("available kings: ", available_kings)
                    king_actions = [el for el in king_actions if el != []]
                    #print("available actions: ", king_actions)  
                                                             
                    print("-----------------------------------------------------")
                    if len(available_kings) == 0:
                        print("There are no available kings to play!")
                        iterator = iterator+1
                        break
                    print("Enter x and y coordinates to select a specific king:")
                    print("Available kings are: ")
                    print(available_kings)
                    try:
                        kx, ky = int(input('x: ')), int(input('y: '))
                        try:
                            if state.board[kx,ky] == "-6":
                                while True:
                                    loc_king = "(" + str(kx) + "," + str(ky) + ")"
                                    print("Select x and y coordinates to move king located in " + loc_king)
                                    print("Available actions are: ")
                                    idx = available_kings.index(loc_king)                           
                                    print(king_actions[idx])
                                    mx, my = int(input('x: ')), int(input('y: '))
                                    action_king = "(" + str(mx) + "," + str(my) + ")"
                                    if action_king in king_actions[idx]:
                                        state = state.move(kx,ky,mx,my,"-6",selection)
                                        isMoved = True
                                        break
                                    else:
                                        print("Invalid action!")
                                #if player is moved, break the loop and make moved false again
                                if isMoved:
                                    isMoved = False
                                    break
                            else:
                                print("Invalid input!")
                        except:
                            print("Input index is out of bounds!")
                    except:
                        print("Invalid type! please enter a number for specified coordinate")    
                
            else:
                print("Invalid input. Please choose again!")
                iterator = iterator+1'''
                
            iterator = iterator+1