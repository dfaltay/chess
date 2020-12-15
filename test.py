import chess_withMinimax_plusNN as game_file
import torch as tr
import chess_net as ch
import chess_data as cd
import numpy as np

def test(selection="1"):

    net = ch.ChessNet1(selection)
    net.load_state_dict(tr.load("model%d.pth" % int(selection)))

    state = game_file.initial_state(selection)
    iterator = 0
    play = 0
    
    while play < 20:
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
            print("XXXXXXXX")
            with tr.no_grad():
                x = tr.stack(tuple(map(cd.encode, [child for child in game_file.getPossibleMoves(selection, state, piece)])))
                y = net(x)
                probs = tr.softmax(y.flatten(), dim=0)
                a = np.random.choice(len(probs), p=probs.detach().numpy())
                new_state = game_file.getPossibleMoves(selection, state, piece)[a]
                
        
            state = new_state
            print("white: ", state)
            iterator += 1
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
            
            print("YYYYYYYYY")
            with tr.no_grad():
                x = tr.stack(tuple(map(cd.encode, [child for child in game_file.getPossibleMoves(selection, state, piece)])))
                print("Y1")
                y = net(x)
                print("Y2")
                probs = tr.softmax(y.flatten(), dim=0)
                a = np.random.choice(len(probs), p=probs.detach().numpy())
                new_state = game_file.getPossibleMoves(selection, state, piece)[a]
            
            state = new_state
            print("black :",state)

            iterator += 1
            play += 1
    
    return print("Game Over")


if __name__ == "__main__":
    
    selection = "1"
    test(selection)