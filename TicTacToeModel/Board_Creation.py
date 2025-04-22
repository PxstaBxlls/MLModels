import numpy as np


#Environment Class - For the state,valid actions,win/lose/draw conditions 
class TicTacToeEnv:               
    def __init__(self): 
        self.board = np.zeros((3,3), dtype = int)
        self.over = False               #whether the game is over or not
        self.winner = 0              #if there is any winner or not
        self.current_player = 1        #1 is for player 1 and -1 is for player 2

    def reset(self):
        self.board = np.zeros((3,3), dtype = int)
        self.over = False
        self.winner = 0
        self.current_player = 1
        return
    
    def get_state(self):                 #returning the current state of the board in a tuple format
        return tuple(int(x) for x in self.board.flatten())
    
    def get_valid_actions(self):                #checking how many valid actions are left in the board
        if self.over:
            return []
        else:
            actions = []
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == 0:
                        actions.append([i,j])
            return actions
    
    def winlose_conditions(self):     #all the winninn or the losing conditions
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != 0:
                self.winner = self.board[i][0]
                self.over = True
                return True
        for j in range(3):
            if self.board[0][j] == self.board[1][j] == self.board[2][j] != 0:
                self.winner = self.board[0][j]
                self.over = True
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            self.winner = self.board[0][0]
            self.over = True
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            self.winner = self.board[0][2]
            self.over = True
            return True
        return False
   
    #if the game is draw
    def draw(self):             #
        if np.all(self.board != 0) and not self.winlose_conditions():
            self.over = True
            return True
        return False

    def switch(self):
        self.current_player = -self.current_player
        
    def visualize(self):                #visualizing the board
        symbols = {0: ' ', 1: 'X', -1: 'O'}
        print("-------------")
        for i in range(3):
            row = []
            for j in range(3):
                row.append(symbols[self.board[i][j]])
            print(f"| {row[0]} | {row[1]} | {row[2]} |")
            print("-------------")

    def is_over(self):            #checking if the game is over or not
        return self.over
        

#The human agent that takes input from user and makes a move in the Tic Tac toe environmemt
class user:
    def __init__(self,environment):
        self.environment = environment
    
    def get_move(self,i,j):
        if [i,j] in self.environment.get_valid_actions():
            self.environment.board[i][j] = 1
        else:
            print("Invalid move! Try again.")
            a,b = map(int,input('Make User Move: ').split())
            self.get_move(a,b)
