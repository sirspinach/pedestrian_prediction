from unittest import TestCase
import numpy as np
from numpy import testing as t

from ..mdp import GridWorldMDP
from .hardmax import *

Actions = GridWorldMDP.Actions
ni = -np.inf

class TestBackwardsValueIter(TestCase):
    def test_simple(self):
        g = GridWorldMDP(3, 1, {(2,0): -9}, default_reward=-1)
        t.assert_allclose([0, -1, -10], backwards_value_iter(g, 0))
        t.assert_allclose([-1, 0, -9], backwards_value_iter(g, 1))
        t.assert_allclose([-2, -1, 0], backwards_value_iter(g, 2))
    def test_2d(self):
        g = GridWorldMDP(3, 3, {(2,0): -3, (1,1): -4}, default_reward=-1,
                euclidean_rewards=False)
        expected = [-3, -2, -2,
                    -2, -4, -1,
                    -4, -1, 0]
        t.assert_allclose(expected, backwards_value_iter(g, g.coor_to_state(2,2)))

class TestForwardsValueIter(TestCase):
    def test_simple(self):
        g = GridWorldMDP(3, 1, {(2,0): -9}, default_reward=-1,
                euclidean_rewards=False)
        t.assert_allclose([0, -1, -2], forwards_value_iter(g, 0))
        t.assert_allclose([-1, 0, -1], forwards_value_iter(g, 1))
        t.assert_allclose([-10, -9, 0], forwards_value_iter(g, 2))
    def test_2d(self):
        g = GridWorldMDP(3, 3, {(2,0): -3, (1,1): -4}, default_reward=-1,
                euclidean_rewards=False)
        expected = [-3, -2, -2,
                    -2, -1, -1,
                    -2, -1, 0]

        t.assert_allclose(expected, forwards_value_iter(g, g.coor_to_state(2,2)))

class TestQValues(TestCase):
    def test_simple(self):
        g = GridWorldMDP(3, 1, {(2,0): -9}, default_reward=-1)
        Q = np.empty([g.S, g.A], dtype=float)

        # V = [0, -1, -2]
        Q.fill(-np.inf)
        Q[0][Actions.ABSORB] = 0
        Q[1][Actions.LEFT] = -1
        Q[1][Actions.RIGHT] = -11
        Q[2][Actions.LEFT] = -2
        t.assert_allclose(Q, q_values(g, 0))

        # V = [-1, 0, -1]
        Q.fill(-np.inf)
        Q[0][Actions.RIGHT] = -1
        Q[1][Actions.ABSORB] = 0
        Q[2][Actions.LEFT] = -1
        t.assert_allclose(Q, q_values(g, 1))

        # V = [-10, -9, 0]
        Q.fill(-np.inf)
        Q[0][Actions.RIGHT] = -10
        Q[1][Actions.LEFT] = -11
        Q[1][Actions.RIGHT] = -9
        Q[2][Actions.ABSORB] = 0
        t.assert_allclose(Q, q_values(g, 2))

class TestActionProbabilities(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g = GridWorldMDP(5,5)

    def test_one_choice(self):
        q_cached = np.array([[1, ni, ni], [ni, 1, ni], [ni, ni, 1]])
        P = action_probabilities(self.g, 3, q_cached=q_cached)
        t.assert_allclose(P, [[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    def test_uniform(self):
        q_cached = np.zeros([3,3])
        P = action_probabilities(self.g, 3, q_cached=q_cached)
        t.assert_allclose(P, np.ones([3,3])/3)

class TestTrajProb(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g = GridWorldMDP(5,5)

    def test_empty(self):
        t.assert_equal(trajectory_probability(self.g, 2, [], beta=1), 1)
        t.assert_equal(trajectory_probability(self.g, 2, [], beta=2), 1)
        t.assert_equal(trajectory_probability(self.g, 2, [], beta=3), 1)

    def test_one_traj(self):
        fake_prob = np.zeros([self.g.S, self.g.A])
        traj = [(0,0), (1,1), (2, 2)]
        fake_prob[0, 0] = 0.5
        fake_prob[1, 1] = 0.5
        fake_prob[2, 2] = 0.5
        t.assert_equal(trajectory_probability(self.g, 2, traj=traj,
                    cached_act_probs=fake_prob), 0.125)