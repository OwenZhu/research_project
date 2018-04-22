# -*- coding: utf-8 -*-
# @Time    : 2018/3/5 下午1:53
# @Author  : Hanwei Zhu
# @Email   : hanweiz@student.unimelb.edu.au
# @File    : test_agent.py
# @Software: PyCharm Community Edition

import sys
import numpy as np
import agent
import constants as const
import matplotlib.pyplot as plt
import environment


def main(argv):
    # initialize

    env = environment.GameEnv()
    const.initialize(3, 2)
    scores = []

    players = []
    for player in range(const.N_AGENTS):
        players.append(agent.DqnAgent(name="DQN_" + str(player), learning_mode=False))

    resource_level = []
    for e in range(const.TEST_STEP):

        state = np.asarray([env.reset()])
        state = np.reshape(state, [1, const.STATE_SPACE])

        actions = [0] * const.N_AGENTS
        efforts = [const.INIT_EFFORT] * const.N_AGENTS
        score = 0

        for time in range(100):
            resource_level.append(env.common_resource_pool)
            for index, player in enumerate(players):
                action = player.choose_action(state)
                if action == 0:
                    efforts[index] += const.MIN_INCREMENT
                else:
                    efforts[index] -= const.MIN_INCREMENT
                if efforts[index] <= 0:
                    efforts[index] = 1
                actions[index] = action

            resource, rewards, done = env.step(efforts)
            score += sum(rewards)
            next_state = np.reshape([resource], [1, const.STATE_SPACE])
            state = next_state

            if done:
                break

        score /= const.N_AGENTS
        print("episode: {}/{}, score: {}, e: {:.2}"
              .format(e, const.TRAINING_EPISODES, score, players[0].epsilon))
        scores.append(score)

    plt.plot(resource_level)
    plt.interactive(False)
    plt.xlabel('Resource level')
    plt.ylabel('Time')
    plt.ylim(0, 100)
    plt.show()


if __name__ == '__main__':
    main(sys.argv)
