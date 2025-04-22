from Board_Creation import TicTacToeEnv, user
from rl_agent import Q_Agent


episodes = 10000
env = TicTacToeEnv()
for i in range(episodes):
    env.reset()
    agent = Q_Agent(env, alpha=0.1, gamma=0.9, epsilon=0.1)
    human = user(env)
    while not env.is_over():
        #human makes a move
        a,b = map(int,input('Make User Move: ').split())
        human.get_move(a,b)
        if env.winlose_conditions() and env.winner != 2:
            print("Game Over and the result is:" , env.winner)
            env.visualize()
            break
        elif env.draw():
            print("Game Over and the result is: Draw")
            env.visualize()
            break
        env.switch()
        rem_valid_actions = env.get_valid_actions()
        if rem_valid_actions:
            #agent makes a move
            agent_action = agent.choose_action(env.get_state(),rem_valid_actions)
            env.board[agent_action[0]][agent_action[1]] = env.current_player
            agent.update_q_value(env.get_state(),agent_action)
            



