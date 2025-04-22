class Train_Agent:
    def __init__(self, environment, agent, human_player):
        self.env = environment
        self.agent = agent
        self.human = human_player
        self.stats = {'wins': 0, 'losses': 0, 'draws': 0}
        # Store agent's last move for learning from human wins
        self.agent_last_state = []
        self.agent_last_action = []
    
    

    def train_against_human(self, episodes):

        for i in range(episodes):
            self.env.reset()
            #game starts
            while not self.env.is_over():
                #human makes a move
                a,b = map(int,input('Make User Move: ').split())
                self.human.get_move(a,b)
                #check if human won
                if self.env.winlose_conditions() and self.env.winner == 1:
                    self.stats['losses'] += 1
                    agent_last_action = self.agent_last_action[-1] if self.agent_last_action else None
                    agent_last_state = self.agent_last_state[-1] if self.agent_last_state else None
                    if agent_last_action and agent_last_state:
                        self.agent.update_q_value(agent_last_state, agent_last_action)
                    print("User wins!")
                    self.env.visualize()
                    break
                #check if game is draw
                elif self.env.draw():
                    self.stats['draws'] += 1
                    agent_last_action = self.agent_last_action[-1] if self.agent_last_action else None
                    agent_last_state = self.agent_last_state[-1] if self.agent_last_state else None
                    if agent_last_action and agent_last_state:
                        self.agent.update_q_value(agent_last_state, agent_last_action)
                    print("Game is a draw!")
                    self.env.visualize()
                    break
                #agent makes a move
                valid_actions = self.env.get_valid_actions()
                current_state_agent_is_in = self.env.get_state()
                if valid_actions:
                    best_action_for_agent = self.agent.choose_action(current_state_agent_is_in, valid_actions)
                self.agent_last_action.append(tuple(best_action_for_agent))
                self.agent_last_state.append(tuple(current_state_agent_is_in))
                self.agent.agent_move(best_action_for_agent)
                #check if agent won
                if self.env.winlose_conditions() and self.env.winner == -1:
                    self.stats['wins'] += 1
                    agent_last_action = self.agent_last_action[-1] if self.agent_last_action else None
                    agent_last_state = self.agent_last_state[-1] if self.agent_last_state else None
                    if agent_last_action and agent_last_state:
                        self.agent.update_q_value(agent_last_state, agent_last_action)
                    print("Agent wins!")
                    self.env.visualize()
                    break
                #check if game is draw
                elif self.env.draw():
                    self.stats['draws'] += 1
                    agent_last_action = self.agent_last_action[-1] if self.agent_last_action else None
                    agent_last_state = self.agent_last_state[-1] if self.agent_last_state else None
                    if agent_last_action and agent_last_state:
                        self.agent.update_q_value(agent_last_state, agent_last_action)
                    print("Game is a draw!")
                    self.env.visualize()
                    break
                #print the board before the next move
                self.env.visualize()
                self.env.switch()



