import numpy as np
import random
class ChessState(object):
    def __init__(self):
        self.board = np.empty((8,8),dtype="U2")
        self.board[:] = "  "
    def __str__(self):
        string = ""
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                string += self.board[i,j]
            string += "\n"
        return string[:-1]
    def piece_positions(self,piece_name):
        state = ChessState()
        state.board = np.copy(self.board)
        positions = []
        np_where = np.argwhere(state.board == piece_name)
        for i in range(0, len(np_where)):
            positions.append("(" + str(np_where[i,0]) + "," + str(np_where[i,1]) + ")")
          
        return positions
    def pawn_actions(self,x,y,player,isAttack):
        state = ChessState()
        state.board = np.copy(self.board)
        actions = []
        
        if player == "+":
            #If it is an opening move, move -2x
            if x-2 >= 0 and x-2 <= 7 and y >= 0 and y <= 7 and isAttack == False:
                if x == 6 and state.board[x-2,y] == "  " and state.board[x-1,y] != "WL":
                    actions.append("(" + str(x-2)+ "," + str(y) + ")")
            #move -x
            if x-1 >= 0 and x-1 <= 7 and y >= 0 and y <= 7 and isAttack == False:
                if state.board[x-1,y] == "  ":
                    actions.append("(" + str(x-1)+ "," + str(y) + ")")
            #move (-x,-y)
            if x-1 >= 0 and x-1 <= 7 and y-1 >= 0 and y-1 <= 7:
                if state.board[x-1,y-1] != "  " and state.board[x-1,y-1][0] != player and state.board[x-1,y-1] != "WL":
                    actions.append("(" + str(x-1)+ "," + str(y-1) + ")")
            #move (-x,+y)
            if x-1 >= 0 and x-1 <= 7 and y+1 >= 0 and y+1 <= 7:
                if state.board[x-1,y+1] != "  " and state.board[x-1,y+1][0] != player and state.board[x-1,y+1] != "WL":
                    actions.append("(" + str(x-1)+ "," + str(y+1) + ")")
        else:
            #If it is an opening move, move +2x
            if x+2 >= 0 and x+2 <= 7 and y >= 0 and y <= 7 and isAttack == False:
                if x == 1 and state.board[x+2,y] == "  " and state.board[x+1,y] != "WL":
                    actions.append("(" + str(x+2)+ "," + str(y) + ")")
            #move +x
            if x+1 >= 0 and x+1 <= 7 and y >= 0 and y <= 7 and isAttack == False:
                if state.board[x+1,y] == "  ":
                    actions.append("(" + str(x+1)+ "," + str(y) + ")")
            #move (+x,-y)
            if x+1 >= 0 and x+1 <= 7 and y-1 >= 0 and y-1 <= 7:
                if state.board[x+1,y-1] != "  " and state.board[x+1,y-1][0] != player and state.board[x+1,y-1] != "WL":
                    actions.append("(" + str(x+1)+ "," + str(y-1) + ")")
            #move (+x,+y)
            if x+1 >= 0 and x+1 <= 7 and y+1 >= 0 and y+1 <= 7:
                if state.board[x+1,y+1] != "  " and state.board[x+1,y+1][0] != player and state.board[x+1,y+1] != "WL":
                    actions.append("(" + str(x+1)+ "," + str(y+1) + ")")
        
        
        return actions
    def knight_actions(self,x,y,player):
        state = ChessState()
        state.board = np.copy(self.board)
        actions = []
              
        #long L in (-x,-y) direction
        if x-2 >= 0 and x-2 <=7 and y-1 >= 0 and y-1 <= 7:
            if state.board[x-2,y-1] != "WL" and state.board[x-2,y-1][0] != player and((state.board[x-1,y] != "WL" and state.board[x-2,y] != "WL") or(state.board[x,y-1] != "WL" and state.board[x-1,y-1] != "WL")):      
                actions.append("(" + str(x-2)+ "," + str(y-1) + ")")
        #long L in (-x, +y) direction
        if x-2 >= 0 and x-2 <=7 and y+1 >= 0 and y+1 <= 7:
            if state.board[x-2,y+1] != "WL" and state.board[x-2,y+1][0] != player and((state.board[x-1,y] != "WL" and state.board[x-2,y] != "WL") or(state.board[x,y+1] != "WL" and state.board[x-1,y+1] != "WL")):                
                actions.append("(" + str(x-2)+ "," + str(y+1) + ")")
        #short L in (-x, -y) direction
        if x-1 >= 0 and x-1 <=7 and y-2 >= 0 and y-2 <= 7:        
            if state.board[x-1,y-2] != "WL" and state.board[x-1,y-2][0] != player and((state.board[x-1,y] != "WL" and state.board[x-1,y-1] != "WL") or(state.board[x,y-1] != "WL" and state.board[x,y-2] != "WL")):               
                actions.append("(" + str(x-1)+ "," + str(y-2) + ")")
        #short L in (-x,+y) direction
        if x-1 >= 0 and x-1 <=7 and y+2 >= 0 and y+2 <= 7:
            if state.board[x-1,y+2] != "WL" and state.board[x-1,y+2][0] != player and((state.board[x-1,y] != "WL" and state.board[x-1,y+1] != "WL") or(state.board[x,y+1] != "WL" and state.board[x,y+2] != "WL")):                   
                actions.append("(" + str(x-1)+ "," + str(y+2) + ")")
        #long L in (+x,-y) direction
        if x+2 >= 0 and x+2 <=7 and y-1 >= 0 and y-1 <= 7:
            if state.board[x+2,y-1] != "WL" and state.board[x+2,y-1][0] != player and((state.board[x+1,y] != "WL" and state.board[x+2,y] != "WL") or(state.board[x,y-1] != "WL" and state.board[x+1,y-1] != "WL")):                
                actions.append("(" + str(x+2)+ "," + str(y-1) + ")")
        #long L in (+x,+y) direction       
        if x+2 >= 0 and x+2 <=7 and y+1 >= 0 and y+1 <= 7:        
            if state.board[x+2,y+1] != "WL" and state.board[x+2,y+1][0] != player and((state.board[x+1,y] != "WL" and state.board[x+2,y] != "WL") or(state.board[x,y+1] != "WL" and state.board[x+1,y+1] != "WL")):                
                actions.append("(" + str(x+2)+ "," + str(y+1) + ")")
        #short L in (+x,-y) direction
        if x+1 >= 0 and x+1 <=7 and y-2 >= 0 and y-2 <= 7:
            if state.board[x+1,y-2] != "WL" and state.board[x+1,y-2][0] != player and((state.board[x+1,y] != "WL" and state.board[x+1,y-1] != "WL") or(state.board[x,y-1] != "WL" and state.board[x,y-2] != "WL")):               
                actions.append("(" + str(x+1)+ "," + str(y-2) + ")")
        #short L in (+x,+y) direction
        if x+1 >= 0 and x+1 <=7 and y+2 >= 0 and y+2 <= 7:        
            if state.board[x+1,y+2] != "WL" and state.board[x+1,y+2][0] != player and((state.board[x+1,y] != "WL" and state.board[x+1,y+1] != "WL") or(state.board[x,y+1] != "WL" and state.board[x,y+2] != "WL")):                
                actions.append("(" + str(x+1)+ "," + str(y+2) + ")")
        
        
        return actions
    def bishop_actions(self,x,y,player):
        state = ChessState()
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
            if y+idx > 7 or x-idx < 0:
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
            if y-idx < 0 or x+idx > 7:
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
            if y+idx > 7 or x+idx > 7:
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
    def rook_actions(self,x,y,player):
        state = ChessState()
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
            if x+idx > 7:
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
            if y+idx > 7:
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
    def king_actions(self,x,y,player):
        state = ChessState()
        state.board = np.copy(self.board)
        actions = []
        #moving in -x direction
        if x-1 >= 0 and x-1 <=7 and y >= 0 and y <= 7:
            if state.board[x-1,y] != "WL" and state.board[x-1,y][0] != player:
                actions.append("(" + str(x-1)+ "," + str(y) + ")")
        #moving in (-x,-y) direction
        if x-1 >= 0 and x-1 <=7 and y-1 >= 0 and y-1 <= 7:
            if state.board[x-1,y-1] != "WL" and state.board[x-1,y-1][0] != player:
                actions.append("(" + str(x-1)+ "," + str(y-1) + ")")
        #moving in (-x,+y) direction
        if x-1 >= 0 and x-1 <=7 and y+1 >= 0 and y+1 <= 7:
            if state.board[x-1,y+1] != "WL" and state.board[x-1,y+1][0] != player:
                actions.append("(" + str(x-1)+ "," + str(y+1) + ")")
        #moving in -y direction
        if x >= 0 and x <=7 and y-1 >= 0 and y-1 <= 7:
            if state.board[x,y-1] != "WL" and state.board[x,y-1][0] != player:
                actions.append("(" + str(x)+ "," + str(y-1) + ")")
        #moving in +y direction
        if x >= 0 and x <=7 and y+1 >= 0 and y+1 <= 7:
            if state.board[x,y+1] != "WL" and state.board[x,y+1][0] != player:
                actions.append("(" + str(x)+ "," + str(y+1) + ")")
        #moving in (+x,+y) direction
        if x+1 >= 0 and x+1 <=7 and y+1 >= 0 and y+1 <= 7:
            if state.board[x+1,y+1] != "WL" and state.board[x+1,y+1][0] != player:
                actions.append("(" + str(x+1)+ "," + str(y+1) + ")")
        #moving in +x direction
        if x+1 >= 0 and x+1 <=7 and y >= 0 and y <= 7:
            if state.board[x+1,y] != "WL" and state.board[x+1,y][0] != player:
                actions.append("(" + str(x+1)+ "," + str(y) + ")")
        #moving in (+x,-y) direction
        if x+1 >= 0 and x+1 <=7 and y-1 >= 0 and y-1 <= 7:
            if state.board[x+1,y-1] != "WL" and state.board[x+1,y-1][0] != player:
                actions.append("(" + str(x+1)+ "," + str(y-1) + ")")
        
        
        return actions
    def is_king_threated(self,x1,y1,x2,y2,player):
        new_state = ChessState()
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
                    black_states.append(new_state.pawn_actions(int(black_positions[i][0]),int(black_positions[i][2]),"-",True))
                if black_positions[i][5] == '2':
                    black_states.append(new_state.knight_actions(int(black_positions[i][0]),int(black_positions[i][2]),"-"))
                elif black_positions[i][5] == '3':
                    black_states.append(new_state.bishop_actions(int(black_positions[i][0]),int(black_positions[i][2]),"-"))
                elif black_positions[i][5] == '4':
                    black_states.append(new_state.rook_actions(int(black_positions[i][0]),int(black_positions[i][2]),"-"))
                elif black_positions[i][5] == '5':
                    black_states.append(new_state.bishop_actions(int(black_positions[i][0]),int(black_positions[i][2]),"-") + new_state.rook_actions(int(black_positions[i][0]),int(black_positions[i][2]),"-"))
                elif black_positions[i][5] == '6':
                    black_states.append(new_state.king_actions(int(black_positions[i][0]),int(black_positions[i][2]),"-"))
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
                    white_states.append(new_state.pawn_actions(int(white_positions[i][0]),int(white_positions[i][2]),"+",True))
                if white_positions[i][5] == '2':
                    white_states.append(new_state.knight_actions(int(white_positions[i][0]),int(white_positions[i][2]),"+"))
                elif white_positions[i][5] == '3':
                    white_states.append(new_state.bishop_actions(int(white_positions[i][0]),int(white_positions[i][2]),"+"))
                elif white_positions[i][5] == '4':
                    white_states.append(new_state.rook_actions(int(white_positions[i][0]),int(white_positions[i][2]),"+"))
                elif white_positions[i][5] == '5':
                    white_states.append(new_state.bishop_actions(int(white_positions[i][0]),int(white_positions[i][2]),"+") + new_state.rook_actions(int(white_positions[i][0]),int(white_positions[i][2]),"+"))
                elif white_positions[i][5] == '6':
                    white_states.append(new_state.king_actions(int(white_positions[i][0]),int(white_positions[i][2]),"+"))
            #print("white states: ", white_states)
            
            for i in range(0, len(white_states)):
                for j in range(0, len(white_states[i])):
                    #if king is in one of those positions, return false, because move will be invalid 
                    if(new_state.board[int(white_states[i][j][1]),int(white_states[i][j][3])] == "-6"):
                        return True
                    #print(black_states[i][j][1])
                    #print(black_states[i][j][3])
            return False
            
    def move(self,x1,y1,x2,y2,piece_name):
        #is_check = False
        new_state = ChessState()
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

def is_unavailable(piece):

    if piece == "+1":
        available_pieces = []
        piece_states = state.piece_positions("+1")
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.pawn_actions(int(piece_states[i][1]),int(piece_states[i][3]),"+",False))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"+")
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
        piece_states = state.piece_positions("-1")
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.pawn_actions(int(piece_states[i][1]),int(piece_states[i][3]),"-",False))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"-")
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
    elif piece == "+2":
        available_pieces = []
        piece_states = state.piece_positions("+2")
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.knight_actions(int(piece_states[i][1]),int(piece_states[i][3]),"+"))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"+")
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
        piece_states = state.piece_positions("-2")
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.knight_actions(int(piece_states[i][1]),int(piece_states[i][3]),"-"))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"-")
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
        piece_states = state.piece_positions("+3")
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.bishop_actions(int(piece_states[i][1]),int(piece_states[i][3]),"+"))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"+")
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
        piece_states = state.piece_positions("-3")
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.bishop_actions(int(piece_states[i][1]),int(piece_states[i][3]),"-"))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"-")
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
        piece_states = state.piece_positions("+4")
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.rook_actions(int(piece_states[i][1]),int(piece_states[i][3]),"+"))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"+")
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
        piece_states = state.piece_positions("-4")
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.rook_actions(int(piece_states[i][1]),int(piece_states[i][3]),"-"))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"-")
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
        piece_states = state.piece_positions("+5")
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.bishop_actions(int(piece_states[i][1]),int(piece_states[i][3]),"+") + state.rook_actions(int(piece_states[i][1]),int(piece_states[i][3]),"+"))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"+")
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
        piece_states = state.piece_positions("-5")
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.bishop_actions(int(piece_states[i][1]),int(piece_states[i][3]),"-") + state.rook_actions(int(piece_states[i][1]),int(piece_states[i][3]),"-"))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"-")
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
        piece_states = state.piece_positions("+6")
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.king_actions(int(piece_states[i][1]),int(piece_states[i][3]),"+"))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"+")
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
        piece_states = state.piece_positions("-6")
        piece_actions = []
        for i in range(0, len(piece_states)):
            piece_actions.append(state.king_actions(int(piece_states[i][1]),int(piece_states[i][3]),"-"))
        #print(piece_actions)
        for i in range(0, len(piece_actions)):
            for j in range(0, len(piece_actions[i])):
                is_threat = state.is_king_threated(int(piece_states[i][1]),int(piece_states[i][3]),int(piece_actions[i][j][1]), int(piece_actions[i][j][3]),"-")
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
def initial_state():
    state = ChessState()
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
  
if __name__ == "__main__":
    state = initial_state()
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
            pawns_list = is_unavailable("+1")
            knights_list = is_unavailable("+2")
            bishops_list = is_unavailable("+3")
            rooks_list = is_unavailable("+4")
            queens_list = is_unavailable("+5")
            kings_list = is_unavailable("+6")
            if pawns_list and knights_list and bishops_list and rooks_list and queens_list and kings_list:
                print("Checkmate! Black wins.")
            a = input("Enter a chess piece('+1'=pawn,'+2'=knight,'+3'=bishop,'+4'=rook,'+5'=queen,'+6'=king,'q'=quit):")
            if a == "q": break
            elif a == "+1":
                while True:
                    available_pawns = []
                    pawn_states = state.piece_positions("+1")
                    pawn_actions = []
                    for i in range(0, len(pawn_states)):
                        pawn_actions.append(state.pawn_actions(int(pawn_states[i][1]),int(pawn_states[i][3]),"+",False))
                    #print(pawn_actions)
                    for i in range(0, len(pawn_actions)):
                        for j in range(0, len(pawn_actions[i])):
                            is_threat = state.is_king_threated(int(pawn_states[i][1]),int(pawn_states[i][3]),int(pawn_actions[i][j][1]), int(pawn_actions[i][j][3]),"+")
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
                                        state = state.move(px,py,mx,my,"+1")
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
                '''while True:                       
                    print("Enter x and y coordinates to select a specific pawn:")
                    print("Available pawns are: ")
                    valid_pawns = state.piece_positions("+1")
                    print(valid_pawns)
                    px = int(input())
                    py = int(input())
                    if(state.board[px,py] == "+1"):
                        #print("asd")
                        while True:
                            valid_actions = state.pawn_actions(px,py,"+",False)
                            print("Select x and y coordinates to move pawn located in ("+ str(px) + "," + str(py) + ")")
                            print("Available actions are: ")
                            print(valid_actions)
                            mx = int(input())
                            my = int(input())
                            action = "(" + str(mx) + "," + str(my) + ")"
                            if valid_actions == []:
                                print("There is no valid action for this pawn. Choose another piece...")                               
                                i = i + 1
                                break
                            elif action in valid_actions:
                                is_threat = state.is_king_threated(px,py,mx,my,"+")
                                if is_threat:
                                    print("is_threat: ", is_threat)
                                    print("Invalid move!(King would be under threat!)")
                                    break
                                else:
                                    print("is_threat: ", is_threat)
                                    state = state.move(px,py,mx,my,"+1")
                                    is_check = state.is_king_threated(-1,-1,-1,-1,"-")                                    
                                    print("is_check: ", is_check)                                
                                    isMoved = True
                                    break
                            else:
                                print("Invalid action!")
                        #if player is moved, break the loop and make moved false again
                        if isMoved:
                            isMoved = False
                            break
                    else:
                        print("Invalid input!")'''
            elif a == "+2":
                while True:
                    available_knights = []
                    knight_states = state.piece_positions("+2")
                    knight_actions = []
                    for i in range(0, len(knight_states)):
                        knight_actions.append(state.knight_actions(int(knight_states[i][1]),int(knight_states[i][3]),"+"))
                    #print(pawn_actions)
                    for i in range(0, len(knight_actions)):
                        for j in range(0, len(knight_actions[i])):
                            is_threat = state.is_king_threated(int(knight_states[i][1]),int(knight_states[i][3]),int(knight_actions[i][j][1]), int(knight_actions[i][j][3]),"+")
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
                                        state = state.move(nx,ny,mx,my,"+2")
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
                '''while True:
                    print("Enter x and y coordinates to select a specific knight:")
                    print("Available knights are: ")
                    valid_knights = state.piece_positions("+2")
                    print(valid_knights)
                    nx = int(input())
                    ny = int(input())
                    if(state.board[nx,ny] == "+2"):
                        #print("asd")
                        while True:
                            valid_actions = state.knight_actions(nx,ny,"+")

                            print("Select x and y coordinates to move knight located in ("+ str(nx) + "," + str(ny) + ")")
                            print("Available actions are: ")
                            print(valid_actions)
                            mx = int(input())
                            my = int(input())
                            action = "(" + str(mx) + "," + str(my) + ")"
                            if valid_actions == []:
                                print("There is no valid action for this knight. Choose another piece...")                              
                                i = i + 1
                                break
                            elif action in valid_actions:
                                is_threat = state.is_king_threated(nx,ny,mx,my,"+")
                                if is_threat:
                                    print("is_threat: ", is_threat)
                                    print("Invalid move!(King would be under threat!)")
                                    break
                                else:
                                    print("is_threat: ", is_threat)
                                    state = state.move(nx,ny,mx,my,"+2")
                                    is_check = state.is_king_threated(-1,-1,-1,-1,"-")                                    
                                    print("is_check: ", is_check)
                                    isMoved = True
                                    break
                            else:
                                print("Invalid action!")            
                        #if player is moved, break the loop and make moved false again
                        if isMoved:
                            isMoved = False
                            break
                        break
                    else:
                        print("Invalid input!")'''
            elif a == "+3":
                while True:
                    available_bishops = []
                    bishop_states = state.piece_positions("+3")
                    bishop_actions = []
                    for i in range(0, len(bishop_states)):
                        bishop_actions.append(state.bishop_actions(int(bishop_states[i][1]),int(bishop_states[i][3]),"+"))
                    #print(bishop_actions)
                    for i in range(0, len(bishop_actions)):
                        for j in range(0, len(bishop_actions[i])):
                            is_threat = state.is_king_threated(int(bishop_states[i][1]),int(bishop_states[i][3]),int(bishop_actions[i][j][1]), int(bishop_actions[i][j][3]),"+")
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
                                        state = state.move(bx,by,mx,my,"+3")
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
                '''while True:
                    print("Enter x and y coordinates to select a specific bishop:")
                    print("Available bishops are: ")
                    valid_bishops = state.piece_positions("+3")
                    print(valid_bishops)
                    bx = int(input())
                    by = int(input())
                    if(state.board[bx,by] == "+3"):
                        #print("asd")
                        while True:
                            valid_actions = state.bishop_actions(bx,by,"+")

                            print("Select x and y coordinates to move bishop located in ("+ str(bx) + "," + str(by) + ")")
                            print("Available actions are: ")
                            print(valid_actions)
                            mx = int(input())
                            my = int(input())
                            action = "(" + str(mx) + "," + str(my) + ")"
                            if valid_actions == []:
                                print("There is no valid action for this bishop. Choose another piece...")                              
                                i = i + 1
                                break
                            elif action in valid_actions:
                                is_threat = state.is_king_threated(bx,by,mx,my,"+")
                                if is_threat:
                                    print("is_threat: ", is_threat)
                                    print("Invalid move!(King would be under threat!)")
                                    break
                                else:                                    
                                    print("is_threat: ", is_threat)
                                    state = state.move(bx,by,mx,my,"+3")
                                    is_check = state.is_king_threated(-1,-1,-1,-1,"-")                                 
                                    print("is_check: ", is_check)
                                    isMoved = True
                                    break
                            else:
                                print("Invalid action!")            
                        #if player is moved, break the loop and make moved false again
                        if isMoved:
                            isMoved = False
                            break
                        break
                    else:
                        print("Invalid input!")'''
            elif a == "+4":
                while True:
                    available_rooks = []
                    rook_states = state.piece_positions("+4")
                    rook_actions = []
                    for i in range(0, len(rook_states)):
                        rook_actions.append(state.rook_actions(int(rook_states[i][1]),int(rook_states[i][3]),"+"))
                    #print(rook_actions)
                    for i in range(0, len(rook_actions)):
                        for j in range(0, len(rook_actions[i])):
                            is_threat = state.is_king_threated(int(rook_states[i][1]),int(rook_states[i][3]),int(rook_actions[i][j][1]), int(rook_actions[i][j][3]),"+")
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
                                        state = state.move(rx,ry,mx,my,"+4")
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
                '''while True:
                    print("Enter x and y coordinates to select a specific rook:")
                    print("Available rooks are: ")
                    valid_rooks = state.piece_positions("+4")
                    print(valid_rooks)
                    rx = int(input())
                    ry = int(input())
                    if(state.board[rx,ry] == "+4"):
                        #print("asd")
                        while True:
                            valid_actions = state.rook_actions(rx,ry,"+")

                            print("Select x and y coordinates to move rook located in ("+ str(rx) + "," + str(ry) + ")")
                            print("Available actions are: ")
                            print(valid_actions)
                            mx = int(input())
                            my = int(input())
                            action = "(" + str(mx) + "," + str(my) + ")"
                            if valid_actions == []:
                                print("There is no valid action for this rook. Choose another piece...")                              
                                i = i + 1
                                break
                            elif action in valid_actions:
                                is_threat = state.is_king_threated(rx,ry,mx,my,"+")
                                if is_threat:
                                    print("is_threat: ", is_threat)
                                    print("Invalid move!(King would be under threat!)")
                                    break
                                else:                                   
                                    print("is_threat: ", is_threat)
                                    state = state.move(rx,ry,mx,my,"+4")
                                    is_check = state.is_king_threated(-1,-1,-1,-1,"-")                                    
                                    print("is_check: ", is_check)
                                    isMoved = True
                                    break
                            else:
                                print("Invalid action!")            
                        #if player is moved, break the loop and make moved false again
                        if isMoved:
                            isMoved = False
                            break
                        break
                    else:
                        print("Invalid input!")'''
            elif a == "+5":
                while True:
                    available_queens = []
                    queen_states = state.piece_positions("+5")
                    queen_actions = []
                    for i in range(0, len(queen_states)):
                        queen_actions.append(state.bishop_actions(int(queen_states[i][1]),int(queen_states[i][3]),"+") + state.rook_actions(int(queen_states[i][1]),int(queen_states[i][3]),"+"))
                    #print(queen_actions)
                    for i in range(0, len(queen_actions)):
                        for j in range(0, len(queen_actions[i])):
                            is_threat = state.is_king_threated(int(queen_states[i][1]),int(queen_states[i][3]),int(queen_actions[i][j][1]), int(queen_actions[i][j][3]),"+")
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
                                        state = state.move(qx,qy,mx,my,"+5")
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
                '''while True:
                    print("Enter x and y coordinates to select a specific queen:")
                    print("Available queens are: ")
                    valid_queens = state.piece_positions("+5")
                    print(valid_queens)
                    qx = int(input())
                    qy = int(input())
                    if(state.board[qx,qy] == "+5"):
                        #print("asd")
                        while True:
                            valid_actions = state.bishop_actions(qx,qy,"+") + state.rook_actions(qx,qy,"+")

                            print("Select x and y coordinates to move queen located in ("+ str(qx) + "," + str(qy) + ")")
                            print("Available actions are: ")
                            print(valid_actions)
                            mx = int(input())
                            my = int(input())
                            action = "(" + str(mx) + "," + str(my) + ")"
                            if valid_actions == []:
                                print("There is no valid action for this queen. Choose another piece...")                              
                                i = i + 1
                                break
                            elif action in valid_actions:
                                is_threat = state.is_king_threated(qx,qy,mx,my,"+")
                                if is_threat:
                                    print("is_threat: ", is_threat)
                                    print("Invalid move!(King would be under threat!)")
                                    break
                                else:                                    
                                    print("is_threat: ", is_threat)
                                    state = state.move(qx,qy,mx,my,"+5")
                                    is_check = state.is_king_threated(-1,-1,-1,-1,"-")                                   
                                    print("is_check: ", is_check)
                                    isMoved = True
                                    break
                            else:
                                print("Invalid action!")            
                        #if player is moved, break the loop and make moved false again
                        if isMoved:
                            isMoved = False
                            break
                        break
                    else:
                        print("Invalid input!")'''
            
            elif a == "+6":
                while True:
                    available_kings = []
                    king_states = state.piece_positions("+6")
                    king_actions = []
                    for i in range(0, len(king_states)):
                        king_actions.append(state.king_actions(int(king_states[i][1]),int(king_states[i][3]),"+"))
                    #print(king_actions)
                    for i in range(0, len(king_actions)):
                        for j in range(0, len(king_actions[i])):
                            is_threat = state.is_king_threated(int(king_states[i][1]),int(king_states[i][3]),int(king_actions[i][j][1]), int(king_actions[i][j][3]),"+")
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
                                        state = state.move(kx,ky,mx,my,"+6")
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
                '''while True:
                    print("Enter x and y coordinates to select a specific king:")
                    print("Available kings are: ")
                    valid_queens = state.piece_positions("+6")
                    print(valid_queens)
                    kx = int(input())
                    ky = int(input())
                    if(state.board[kx,ky] == "+6"):
                        #print("asd")
                        while True:
                            valid_actions = state.king_actions(kx,ky,"+")

                            print("Select x and y coordinates to move king located in ("+ str(kx) + "," + str(ky) + ")")
                            print("Available actions are: ")
                            print(valid_actions)
                            mx = int(input())
                            my = int(input())
                            action = "(" + str(mx) + "," + str(my) + ")"
                            if valid_actions == []:
                                print("There is no valid action for this king. Choose another piece...")                              
                                i = i + 1
                                break
                            elif action in valid_actions:
                                is_threat = state.is_king_threated(kx,ky,mx,my,"+")
                                if is_threat:
                                    print("is_threat: ", is_threat)
                                    print("Invalid move!(King would be under threat!)")
                                    break
                                else:                             
                                    print("is_threat: ", is_threat)
                                    state = state.move(kx,ky,mx,my,"+6")
                                    is_check = state.is_king_threated(-1,-1,-1,-1,"-")                                    
                                    print("is_check: ", is_check)
                                    isMoved = True
                                    break
                            else:
                                print("Invalid action!")            
                        #if player is moved, break the loop and make moved false again
                        if isMoved:
                            isMoved = False
                            break
                        break
                    else:
                        print("Invalid input!")'''
            else:
                print("Invalid input. Please choose again!")
                iterator = iterator+1
                
            iterator = iterator+1
        else:
            print("---------------------")
            print("Black player's turn")
            print("Current state:")
            print(str(state))
            #Check if it is a checkmate
            pawns_list = is_unavailable("-1")
            knights_list = is_unavailable("-2")
            bishops_list = is_unavailable("-3")
            rooks_list = is_unavailable("-4")
            queens_list = is_unavailable("-5")
            kings_list = is_unavailable("-6")
            if pawns_list and knights_list and bishops_list and rooks_list and queens_list and kings_list:
                print("Checkmate! White wins.")
                break
            a = input("Enter a chess piece('-1'=pawn,'-2'=knight,'-3'=bishop,'-4'=rook,'-5'=queen,'-6'=king,'q'=quit):")
            if a == "q": break
            elif a == "-1":
                while True:
                    available_pawns = []
                    pawn_states = state.piece_positions("-1")
                    pawn_actions = []
                    for i in range(0, len(pawn_states)):
                        pawn_actions.append(state.pawn_actions(int(pawn_states[i][1]),int(pawn_states[i][3]),"-",False))
                    #print(pawn_actions)
                    for i in range(0, len(pawn_actions)):
                        for j in range(0, len(pawn_actions[i])):
                            is_threat = state.is_king_threated(int(pawn_states[i][1]),int(pawn_states[i][3]),int(pawn_actions[i][j][1]), int(pawn_actions[i][j][3]),"-")
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
                                        state = state.move(px,py,mx,my,"-1")
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
                    '''print("-----------------------------------------------------")        
                    print("Enter x and y coordinates to select a specific pawn:")
                    print("Available pawns are: ")
                    valid_pawns = state.piece_positions("-1")
                    print(valid_pawns)
                    px = int(input())
                    py = int(input())
                    if(state.board[px,py] == "-1"):
                        #print("asd")
                        while True:
                            valid_actions = state.pawn_actions(px,py,"-",False)
                            print("Select x and y coordinates to move pawn located in ("+ str(px) + "," + str(py) + ")")
                            print("Available actions are: ")
                            print(valid_actions)
                            mx = int(input())
                            my = int(input())
                            action = "(" + str(mx) + "," + str(my) + ")"
                            if valid_actions == []:
                                print("There is no valid action for this pawn. Choose another piece...")                               
                                i = i + 1
                                break
                            elif action in valid_actions:
                                is_threat = state.is_king_threated(px,py,mx,my,"-")
                                if is_threat:
                                    print("is_threat: ", is_threat)
                                    print("Invalid move!(King would be under threat!)")
                                    break
                                else:
                                    print("is_threat: ", is_threat)
                                    state = state.move(px,py,mx,my,"-1")
                                    is_check = state.is_king_threated(-1,-1,-1,-1,"+")                                    
                                    print("is_check: ", is_check)                                
                                    isMoved = True
                                    break
                            else:
                                print("Invalid action!")
                        #if player is moved, break the loop and make moved false again
                        if isMoved:
                            isMoved = False
                            break
                    else:
                        print("Invalid input!")'''
            elif a == "-2":
                while True:
                    available_knights = []
                    knight_states = state.piece_positions("-2")
                    knight_actions = []
                    for i in range(0, len(knight_states)):
                        knight_actions.append(state.knight_actions(int(knight_states[i][1]),int(knight_states[i][3]),"-"))
                    #print(knight_actions)
                    for i in range(0, len(knight_actions)):
                        for j in range(0, len(knight_actions[i])):
                            is_threat = state.is_king_threated(int(knight_states[i][1]),int(knight_states[i][3]),int(knight_actions[i][j][1]), int(knight_actions[i][j][3]),"-")
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
                                        state = state.move(nx,ny,mx,my,"-2")
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
                '''while True:
                    print("Enter x and y coordinates to select a specific knight:")
                    print("Available knights are: ")
                    valid_knights = state.piece_positions("-2")
                    print(valid_knights)
                    nx = int(input())
                    ny = int(input())
                    if(state.board[nx,ny] == "-2"):
                        #print("asd")
                        while True:
                            valid_actions = state.knight_actions(nx,ny,"-")

                            print("Select x and y coordinates to move knight located in ("+ str(nx) + "," + str(ny) + ")")
                            print("Available actions are: ")
                            print(valid_actions)
                            mx = int(input())
                            my = int(input())
                            action = "(" + str(mx) + "," + str(my) + ")"
                            if valid_actions == []:
                                print("There is no valid action for this knight. Choose another piece...")                              
                                i = i + 1
                                break
                            elif action in valid_actions:
                                is_threat = state.is_king_threated(nx,ny,mx,my,"-")
                                if is_threat:
                                    print("is_threat: ", is_threat)
                                    print("Invalid move!(King would be under threat!)")
                                    break
                                else:
                                    print("is_threat: ", is_threat)
                                    state = state.move(nx,ny,mx,my,"-2")
                                    is_check = state.is_king_threated(-1,-1,-1,-1,"+")                                    
                                    print("is_check: ", is_check)
                                    isMoved = True
                                    break
                            else:
                                print("Invalid action!")            
                        #if player is moved, break the loop and make moved false again
                        if isMoved:
                            isMoved = False
                            break
                        break
                    else:
                        print("Invalid input!")'''
            elif a == "-3":
                while True:
                    available_bishops = []
                    bishop_states = state.piece_positions("-3")
                    bishop_actions = []
                    for i in range(0, len(bishop_states)):
                        bishop_actions.append(state.bishop_actions(int(bishop_states[i][1]),int(bishop_states[i][3]),"-"))
                    #print(bishop_actions)
                    for i in range(0, len(bishop_actions)):
                        for j in range(0, len(bishop_actions[i])):
                            is_threat = state.is_king_threated(int(bishop_states[i][1]),int(bishop_states[i][3]),int(bishop_actions[i][j][1]), int(bishop_actions[i][j][3]),"-")
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
                                        state = state.move(bx,by,mx,my,"-3")
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
                '''while True:
                    print("Enter x and y coordinates to select a specific bishop:")
                    print("Available bishops are: ")
                    valid_bishops = state.piece_positions("-3")
                    print(valid_bishops)
                    bx = int(input())
                    by = int(input())
                    if(state.board[bx,by] == "-3"):
                        #print("asd")
                        while True:
                            valid_actions = state.bishop_actions(bx,by,"-")

                            print("Select x and y coordinates to move bishop located in ("+ str(bx) + "," + str(by) + ")")
                            print("Available actions are: ")
                            print(valid_actions)
                            mx = int(input())
                            my = int(input())
                            action = "(" + str(mx) + "," + str(my) + ")"
                            if valid_actions == []:
                                print("There is no valid action for this bishop. Choose another piece...")                              
                                i = i + 1
                                break
                            elif action in valid_actions:
                                is_threat = state.is_king_threated(bx,by,mx,my,"-")
                                if is_threat:
                                    print("is_threat: ", is_threat)
                                    print("Invalid move!(King would be under threat!)")
                                    break
                                else:                                    
                                    print("is_threat: ", is_threat)
                                    state = state.move(bx,by,mx,my,"-3")
                                    is_check = state.is_king_threated(-1,-1,-1,-1,"+")                                 
                                    print("is_check: ", is_check)
                                    isMoved = True
                                    break
                            else:
                                print("Invalid action!")            
                        #if player is moved, break the loop and make moved false again
                        if isMoved:
                            isMoved = False
                            break
                        break
                    else:
                        print("Invalid input!")'''
            elif a == "-4":
                while True:
                    available_rooks = []
                    rook_states = state.piece_positions("-4")
                    rook_actions = []
                    for i in range(0, len(rook_states)):
                        rook_actions.append(state.rook_actions(int(rook_states[i][1]),int(rook_states[i][3]),"-"))
                    #print(rook_actions)
                    for i in range(0, len(rook_actions)):
                        for j in range(0, len(rook_actions[i])):
                            is_threat = state.is_king_threated(int(rook_states[i][1]),int(rook_states[i][3]),int(rook_actions[i][j][1]), int(rook_actions[i][j][3]),"-")
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
                                        state = state.move(rx,ry,mx,my,"-4")
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
                '''while True:
                    print("Enter x and y coordinates to select a specific rook:")
                    print("Available rooks are: ")
                    valid_rooks = state.piece_positions("-4")
                    print(valid_rooks)
                    rx = int(input())
                    ry = int(input())
                    if(state.board[rx,ry] == "-4"):
                        #print("asd")
                        while True:
                            valid_actions = state.rook_actions(rx,ry,"-")

                            print("Select x and y coordinates to move rook located in ("+ str(rx) + "," + str(ry) + ")")
                            print("Available actions are: ")
                            print(valid_actions)
                            mx = int(input())
                            my = int(input())
                            action = "(" + str(mx) + "," + str(my) + ")"
                            if valid_actions == []:
                                print("There is no valid action for this rook. Choose another piece...")                              
                                i = i + 1
                                break
                            elif action in valid_actions:
                                is_threat = state.is_king_threated(rx,ry,mx,my,"-")
                                if is_threat:
                                    print("is_threat: ", is_threat)
                                    print("Invalid move!(King would be under threat!)")
                                    break
                                else:                                   
                                    print("is_threat: ", is_threat)
                                    state = state.move(rx,ry,mx,my,"-4")
                                    is_check = state.is_king_threated(-1,-1,-1,-1,"+")                                    
                                    print("is_check: ", is_check)
                                    isMoved = True
                                    break
                            else:
                                print("Invalid action!")            
                        #if player is moved, break the loop and make moved false again
                        if isMoved:
                            isMoved = False
                            break
                        break
                    else:
                        print("Invalid input!")'''
            elif a == "-5":
                while True:
                    available_queens = []
                    queen_states = state.piece_positions("-5")
                    queen_actions = []
                    for i in range(0, len(queen_states)):
                        queen_actions.append(state.bishop_actions(int(queen_states[i][1]),int(queen_states[i][3]),"-") + state.rook_actions(int(queen_states[i][1]),int(queen_states[i][3]),"-"))
                    #print(queen_actions)
                    for i in range(0, len(queen_actions)):
                        for j in range(0, len(queen_actions[i])):
                            is_threat = state.is_king_threated(int(queen_states[i][1]),int(queen_states[i][3]),int(queen_actions[i][j][1]), int(queen_actions[i][j][3]),"-")
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
                                        state = state.move(qx,qy,mx,my,"-5")
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
                '''while True:
                    print("Enter x and y coordinates to select a specific queen:")
                    print("Available queens are: ")
                    valid_queens = state.piece_positions("-5")
                    print(valid_queens)
                    qx = int(input())
                    qy = int(input())
                    if(state.board[qx,qy] == "-5"):
                        #print("asd")
                        while True:
                            valid_actions = state.bishop_actions(qx,qy,"-") + state.rook_actions(qx,qy,"-")

                            print("Select x and y coordinates to move queen located in ("+ str(qx) + "," + str(qy) + ")")
                            print("Available actions are: ")
                            print(valid_actions)
                            mx = int(input())
                            my = int(input())
                            action = "(" + str(mx) + "," + str(my) + ")"
                            if valid_actions == []:
                                print("There is no valid action for this queen. Choose another piece...")                              
                                i = i + 1
                                break
                            elif action in valid_actions:
                                is_threat = state.is_king_threated(qx,qy,mx,my,"-")
                                if is_threat:
                                    print("is_threat: ", is_threat)
                                    print("Invalid move!(King would be under threat!)")
                                    break
                                else:                                    
                                    print("is_threat: ", is_threat)
                                    state = state.move(qx,qy,mx,my,"-5")
                                    is_check = state.is_king_threated(-1,-1,-1,-1,"+")                                   
                                    print("is_check: ", is_check)
                                    isMoved = True
                                    break
                            else:
                                print("Invalid action!")            
                        #if player is moved, break the loop and make moved false again
                        if isMoved:
                            isMoved = False
                            break
                        break
                    else:
                        print("Invalid input!")'''
            
            elif a == "-6":
                while True:
                    available_kings = []
                    king_states = state.piece_positions("-6")
                    king_actions = []
                    for i in range(0, len(king_states)):
                        king_actions.append(state.king_actions(int(king_states[i][1]),int(king_states[i][3]),"-"))
                    #print(king_actions)
                    for i in range(0, len(king_actions)):
                        for j in range(0, len(king_actions[i])):
                            is_threat = state.is_king_threated(int(king_states[i][1]),int(king_states[i][3]),int(king_actions[i][j][1]), int(king_actions[i][j][3]),"-")
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
                                        state = state.move(kx,ky,mx,my,"-6")
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
                '''while True:
                    print("Enter x and y coordinates to select a specific king:")
                    print("Available kings are: ")
                    valid_queens = state.piece_positions("-6")
                    print(valid_queens)
                    kx = int(input())
                    ky = int(input())
                    if(state.board[kx,ky] == "-6"):
                        #print("asd")
                        while True:
                            valid_actions = state.king_actions(kx,ky,"-")

                            print("Select x and y coordinates to move king located in ("+ str(kx) + "," + str(ky) + ")")
                            print("Available actions are: ")
                            print(valid_actions)
                            mx = int(input())
                            my = int(input())
                            action = "(" + str(mx) + "," + str(my) + ")"
                            if valid_actions == []:
                                print("There is no valid action for this king. Choose another piece...")                              
                                i = i + 1
                                break
                            elif action in valid_actions:
                                is_threat = state.is_king_threated(kx,ky,mx,my,"-")
                                if is_threat:
                                    print("is_threat: ", is_threat)
                                    print("Invalid move!(King would be under threat!)")
                                    break
                                else:                             
                                    print("is_threat: ", is_threat)
                                    state = state.move(kx,ky,mx,my,"-6")
                                    is_check = state.is_king_threated(-1,-1,-1,-1,"+")                                    
                                    print("is_check: ", is_check)
                                    isMoved = True
                                    break
                            else:
                                print("Invalid action!")            
                        #if player is moved, break the loop and make moved false again
                        if isMoved:
                            isMoved = False
                            break
                        break
                    else:
                        print("Invalid input!")'''
            else:
                print("Invalid input. Please choose again!")
                iterator = iterator+1
                
            iterator = iterator+1