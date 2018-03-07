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

    def simulate(self):
        for n in range(n_games):
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

class MultiSetOfGames:
    def __init__(self, ids, prob_head, n_games):
        self._ids = ids
        self._probHead = prob_head
        self._nGames = n_games

        self._gameRewards = [] # create an empty list where rewards will be stored
        self._sumStat_meanGameRewards = None
        self._meanRewards = []
        self._Losses = []
        self._sumStat_meanLosses = None
        self._meanLosses = []

    def simulate(self):
        for i in range(len(self._ids)):
            setofgames = SetOfGames(self._probHead,self._nGames)
            output = setofgames.simulate()
            self._gameRewards.append(setofgames.get_reward_list())
            self._meanRewards.append(setofgames.get_ave_reward())
        self._sumStat_meanGameRewards = \
            Stat.SummaryStat('', self._meanRewards)
    def get_SetOfGames_mean_rewards(self, games_index):
        return self._meanRewards[games_index]
    def get_SetOfGames_CI_mean_rewards(self, games_index,alpha):
        st = Stat.SummaryStat('',self._meanRewards[games_index])
        return st.get_t_CI(alpha)
    def get_all_mean_rewards(self):
        return self._meanRewards
    def get_overall_mean_rewards(self):
        return self._sumStat_meanGameRewards.get_mean()

    def get_overall_max_rewards(self):
        return max(self._meanRewards)
    def get_overall_min_rewards(self):
        return min(self._meanRewards)

    def get_SetOfGames_PI_rewards(self, game_index, alpha):
        st = Stat.SummaryStat('', self._meanRewards[game_index])
        return st.get_PI(alpha)
    def get_PI_mean_rewards(self, alpha):
        return self._sumStat_meanGameRewards.get_PI(alpha)

prob_head = 0.5
n_of_flips = 20
n_games = 10
Num_Sim_SetOfGames = 100
Alpha = 0.05

Gambler = MultiSetOfGames(ids=range(Num_Sim_SetOfGames), prob_head = [prob_head]* Num_Sim_SetOfGames,
                          n_games = [n_games]*Num_Sim_SetOfGames)
Gambler.simulate()
print("Data for Gambler:")
print("Projected mean reward ($) is", Gambler.get_overall_mean_rewards())
print("Project PI for mean reward is ", Gambler.get_PI_mean_rewards(Alpha))

print("I give up. I'm so tired, and if I can drop any of my HW sets, this will probably be it. I think we are allowed to drop 1 or 2 hw set grades"
      ". . . if not, we should be :). I'll be interested to see how to solve this (and I think I understand it in theory"
      " when the solution is released. For the record, I know my mean should not always"
      "be -70, but the output= line that is hashtagged out kept giving me an unresolved attribtion")
