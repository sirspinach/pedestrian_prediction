from __future__ import division
from unittest import TestCase
import numpy as np
from numpy import testing as t

from ...mdp import GridWorldMDP
from .state import *

class TestInferFromStart(TestCase):

    def test_base_case(self):
        mdp = GridWorldMDP(3, 3, euclidean_rewards=True)
        D = np.zeros(9)
        D[0] = 1
        t.assert_allclose(D, infer_from_start(mdp, 0, 3, T=0,
            verbose_return=False))

    def test_uniform_easy(self):
        mdp = GridWorldMDP(3, 3)
        p = uniform = np.ones([mdp.S, mdp.A]) / mdp.A
        # p = {s: uniform for s in range(mdp.S)}

        D = D0 = np.zeros(9)
        D[0] = 1
        t.assert_allclose(D, infer_from_start(mdp, 0, 3, T=0,
            verbose_return=False, cached_action_probs=p))

        D = D1 = np.zeros(9)
        D[0] = 1
        D[mdp.coor_to_state(0,0)] = 1 / mdp.A
        D[mdp.coor_to_state(0,1)] = 1 / mdp.A
        D[mdp.coor_to_state(1,0)] = 1 / mdp.A
        D[mdp.coor_to_state(1,1)] = 1 / mdp.A
        t.assert_allclose(D, infer_from_start(mdp, 0, 3, T=1,
            verbose_return=False, cached_action_probs=p))

        D = D2 = np.zeros(9)
        D[0] = 1
        q = 1 / mdp.A / mdp.A
        D[mdp.coor_to_state(0,0)] = 4*q
        D[mdp.coor_to_state(0,1)] = 4*q
        D[mdp.coor_to_state(1,0)] = 4*q
        D[mdp.coor_to_state(1,1)] = 4*q
        D[mdp.coor_to_state(2,2)] = 1*q
        D[mdp.coor_to_state(0,2)] = 2*q
        D[mdp.coor_to_state(1,2)] = 2*q
        D[mdp.coor_to_state(2,0)] = 2*q
        D[mdp.coor_to_state(2,1)] = 2*q
        t.assert_allclose(D, infer_from_start(mdp, 0, 3, T=2,
            verbose_return=False, cached_action_probs=p))

        t.assert_allclose([D0, D1, D2], infer_from_start(mdp, 0, 3, T=2,
            cached_action_probs=p, verbose_return=True)[0])

    def test_infer_multidest_no_crash(self):
        mdp = GridWorldMDP(3, 3)
        p = uniform = np.ones([mdp.S, mdp.A]) / mdp.A

        D = D1 = np.zeros(9)
        D[0] = 1
        D[mdp.coor_to_state(0,0)] = 1 / mdp.A
        D[mdp.coor_to_state(0,1)] = 1 / mdp.A
        D[mdp.coor_to_state(1,0)] = 1 / mdp.A
        D[mdp.coor_to_state(1,1)] = 1 / mdp.A
        traj = [(4,4)]
        infer(mdp, traj, [0, 1], T=1, verbose_return=False, cached_action_probs=p)