"""
This file is individualized for NetID faltay.
"""
import itertools as it
from chess_withMinimax_plusNN import MinimaxEngine as engine
import chess_withMinimax_plusNN as game_file
import torch as tr

def generate(selection="1", num_games=2, max_depth=3):

    data = []    
    for game in range(num_games):
        
        state = game_file.initial_state(selection)
        print(game)
        iterator = 0
        play = 0
        while play < 30:
            if iterator%2 == 0:
                #print("iterator: ", iterator)
                # print("---------------------")
                # print("White player's turn")
                # print("Current state:")
                # print(str(state))
                #Check if it is a checkmate
                pawns_list = game_file.is_unavailable("+1",selection, state)
                knights_list = game_file.is_unavailable("+2",selection, state)
                bishops_list = game_file.is_unavailable("+3",selection, state)
                rooks_list = game_file.is_unavailable("+4",selection, state)
                queens_list = game_file.is_unavailable("+5",selection, state)
                kings_list = game_file.is_unavailable("+6",selection, state)
                if pawns_list and knights_list and bishops_list and rooks_list and queens_list and kings_list:
                    print("Checkmate! Black wins.")
                    break
                
                piece = '+'
                AI = engine(max_depth)
                new_state, baseScore = AI.bestAction(state,selection,True,piece)
                state = new_state
                print("white: ", state)
                iterator += 1
                data.append((state, baseScore))
                play += 1
            else:
                #Check if it is a checkmate
                pawns_list = game_file.is_unavailable("-1",selection, state)
                knights_list = game_file.is_unavailable("-2",selection, state)
                bishops_list = game_file.is_unavailable("-3",selection, state)
                rooks_list = game_file.is_unavailable("-4",selection, state)
                queens_list = game_file.is_unavailable("-5",selection, state)
                kings_list = game_file.is_unavailable("-6",selection, state)
                if pawns_list and knights_list and bishops_list and rooks_list and queens_list and kings_list:
                    print("Checkmate! White wins.")
                    break
                
                piece = '-'
                AI = engine(max_depth)
                new_state, baseScore = AI.bestAction(state,selection,True,piece)
                state = new_state
                print("black :",state)

                iterator += 1

                data.append((state, abs(baseScore)))
                play += 1

    print(len(data))
    return data


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

def get_batch(selection="1", num_games=2, max_depth=1):

    state = game_file.initial_state(selection)
    
    training_data = generate(selection, num_games, max_depth)    
    input_arr = []
    output_arr = []
    for data in training_data:
        input_arr.append(encode(data[0]))
        output_arr.append(data[1])

    outputs = tr.tensor(output_arr,dtype=tr.float)
    outputs = tr.reshape(outputs,(len(training_data),1))
    
    inputs = tr.stack(input_arr,0)
    inputs = tr.tensor(inputs,dtype=tr.float)
    

    tr.reshape(inputs,(len(training_data),3,len(state.board),len(state.board[0])))
    return (inputs, outputs)

if __name__ == "__main__":
    
    max_depth = 3
    board = input("Choose a board size:('1'= 8x8, '2' = 8x7, '3' = 8x6, '4' = 8x5, '5' = 8x4, 'q' = quit)")
    selection, num_games = board, 25
    inputs, outputs = get_batch(selection, num_games=num_games, max_depth=max_depth)
    print(inputs[-1])
    print(outputs[-1])

    import pickle as pk
    with open("data%d.pkl" % int(selection), "wb") as f: pk.dump((inputs, outputs), f)

