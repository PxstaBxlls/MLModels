from Board_Creation import TicTacToeEnv
import numpy as np
import random
class Q_Agent:
    def __init__(self,env,alpha,gamma,epsilon):     #alpha = learning rate, gamma = discount factor, epsilon = exploration rate
        self.environment = env
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.state_array = env.get_state()

    def give_reward(self,winner):
        if winner == 1:
            return -10
        elif winner == -1:
            return 10
        elif winner == 2:
            return -10
        else:
            return -0.5
        
    def get_q_value(self,state,action):         #returning the q value for any state action pair or initializing it to 0 if not discovered yet
        action = tuple(action)
        return self.q_table.get((state,action),0)
    

    def smart_explore(self, state, valid_actions):
        # Try to block opponent's winning move
        for action in valid_actions:
            hypothetical_state = self.simulate_user_move(state, action)
            # print(hypothetical_state)
            if self.check_user_win(hypothetical_state):
                return action  # Block this move immediately

        # Prefer center
        if [1, 1] in valid_actions:
            return [1, 1]

        # Prefer corners
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        corner_moves = [action for action in valid_actions if action in corners]
        if corner_moves:
            return random.choice(corner_moves)

        # Fallback: random move
        return random.choice(valid_actions)
    
    def simulate_user_move(self, state, action):
        # Make a deep copy of the board
        new_state = self.environment.board.copy()
        x, y = action
        new_state[x][y] = 1  # Assuming '1' is the human/player marker
        return new_state


    def check_user_win(self, state):
        # Check rows, columns, and diagonals for a win
        for i in range(3):
            if all(cell == 1 for cell in state[i]): return True
            if all(row[i] == 1 for row in state): return True
        if all(state[i][i] == 1 for i in range(3)): return True
        if all(state[i][2 - i] == 1 for i in range(3)): return True
        return False

    
    def choose_action(self,state,valid_actions):
        #--to heuristic logic to be deployed later
        # for actions in valid_actions: 
        #     hypothetical_state = self.simulate_user_move(state, actions)
        #     if self.check_user_win(hypothetical_state):
        #         return actions
        if np.random.rand() < self.epsilon:   #Exploration
            return self.smart_explore(state, valid_actions)
            ## return random.choice(valid_actions)  # Random action for exploration
        else:                                 #exploitation
            q_values = [self.get_q_value(state,action) for action in valid_actions]
            max_q_val = max(q_values)
            max_actions = [action for action in valid_actions if self.get_q_value(state,action) == max_q_val]
            agent_action =  max_actions[np.random.randint(len(max_actions))]
            return agent_action
    
    def update_q_value(self, old_state, action_taken_in_old_state):
        # Convert action to tuple for dictionary key
        action_taken = tuple(action_taken_in_old_state)
    
        # Get current Q-value
        current_q_value = self.get_q_value(old_state, action_taken_in_old_state)
    
        # Get next state
        new_state_after_best_action = self.environment.get_state()    #this is after the agent has taken action_taken
    
    # Calculate maximum Q-value for next state
        max_next_q = 0
        if not self.environment.over:
            valid_actions = self.environment.get_valid_actions()
            if valid_actions:
                next_q_values = [self.get_q_value(new_state_after_best_action, next_action) for next_action in valid_actions]
                if next_q_values:
                    max_next_q = max(next_q_values)
    
    # Calculate reward
        reward = self.give_reward(self.environment.winner)
    
    # Update Q-value
        new_q = current_q_value + self.alpha * (reward + (self.gamma * (max_next_q - current_q_value)))
    
    # Store in Q-table
        self.q_table[(old_state, action_taken_in_old_state)] = new_q

    def agent_move(self,best_action):   #agent move
        i,j = best_action
        self.environment.board[i][j] = -1
        self.environment.switch()
