import numpy as np
import scr.FigureSupport as figureLibrary
import scr.SamplePathClass as PathCls
import scr.StatisticalClasses as Stat

class Game(object):
    def __init__(self, id, prob_head):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)
        self._probHead = prob_head  # probability of flipping a head
        self._countWins = 0  # number of wins, set to 0 to begin

    def simulate(self, n_of_flips):

        count_tails = 0  # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:  # if the series is ..., T, T, H
                    self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

    def get_reward(self):
        # calculate the reward from playing a single game
        return 100*self._countWins - 250


class SetOfGames:
    def __init__(self, prob_head, n_games):
        self._gameRewards = [] # create an empty list where rewards will be stored
        self._sumStat_gameRewards = None
        self._Losses = []
        self._sumStat_Losses = None
        # simulate the games
        for n in range(n_games):
            # create a new game
            game = Game(id=n, prob_head=prob_head)
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())

    def get_ave_reward(self):
        """ returns the average reward from all games"""
        re = Stat.SummaryStat('',self._gameRewards)
        return re.get_mean()
            #sum(self._gameRewards) / len(self._gameRewards)

    def get_reward_list(self):
        """ returns all the rewards from all game to later be used for creation of histogram """
        return self._gameRewards

    def get_CI_ave_reward(self, alpha):
        st = Stat.SummaryStat('',self._gameRewards)
        return st.get_t_CI(alpha)

    def get_max(self):
        """ returns maximum reward"""
        return max(self._gameRewards)

    def get_min(self):
        """ returns minimum reward"""
        return min(self._gameRewards)

    def get_probability_loss(self):
        """ returns the probability of a loss """
        count_loss = 0
        for value in self._gameRewards:
            if value < 0:
                self._Losses.append(1)
            else:
                self._Losses.append(0)
        pl = Stat.SummaryStat('',self._Losses)
        return pl.get_mean()

    def get_CI_probability_loss(self, alpha):
        cil = Stat.SummaryStat('',self._Losses)
        return cil.get_t_CI(alpha)

# Calculate expected reward of 3000 games
print("Data for a casino owner who gets to play this game many times (approximated by 3000)")
trial = SetOfGames(prob_head=0.5, n_games=1000)
print("The average expected reward is:", trial.get_ave_reward())
print("In our trial, the maximum reward is:", trial.get_max())
print("In our trial, the minimum reward is:", trial.get_min())
print("The probability of a single game yielding a loss is:", trial.get_probability_loss())
print('95% CI of average reward', trial.get_CI_ave_reward(0.05))
print('95% CI of probability loss', trial.get_CI_probability_loss(0.05))

