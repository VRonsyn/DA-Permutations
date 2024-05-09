import math
import unittest

import numpy as np

import trotter_johnson as tj
from errors import NoSuccessorError


class TrotterJohnsonTest(unittest.TestCase):

    def test_rank(self):
        self.assertEqual(tj.trotter_johnson_rank(3, [1, 2, 3]), 0)
        self.assertEqual(tj.trotter_johnson_rank(3, [1, 3, 2]), 1)
        self.assertEqual(tj.trotter_johnson_rank(3, [3, 1, 2]), 2)
        self.assertEqual(tj.trotter_johnson_rank(3, [3, 2, 1]), 3)
        self.assertEqual(tj.trotter_johnson_rank(3, [2, 3, 1]), 4)
        self.assertEqual(tj.trotter_johnson_rank(3, [2, 1, 3]), 5)

    def test_unrank(self):
        assert np.array_equal(tj.trotter_johnson_unrank(3, 0), [1, 2, 3])
        assert np.array_equal(tj.trotter_johnson_unrank(3, 1), [1, 3, 2])
        assert np.array_equal(tj.trotter_johnson_unrank(3, 2), [3, 1, 2])
        assert np.array_equal(tj.trotter_johnson_unrank(3, 3), [3, 2, 1])
        assert np.array_equal(tj.trotter_johnson_unrank(3, 4), [2, 3, 1])
        assert np.array_equal(tj.trotter_johnson_unrank(3, 5), [2, 1, 3])

    def test_successor(self):
        for n in range(1, 8):
            perm = np.arange(1, n + 1).tolist()
            i = 1
            while True:
                try:
                    perm = tj.trotter_johnson_successor(n, perm)
                    i += 1
                except NoSuccessorError:
                    assert i == math.factorial(n)
                    break

    def test_successor_rank(self):
        for n in range(1, 8):
            perm = np.arange(1, n + 1).tolist()
            i = 0
            while True:
                try:
                    perm = tj.trotter_johnson_successor(n, perm)
                    i += 1
                    assert tj.trotter_johnson_rank(n, perm) == i
                except NoSuccessorError:
                    assert i == math.factorial(n) - 1
                    break

    def test_rank_unrank(self):
        for n in range(1, 8):
            perm = np.arange(1, n + 1).tolist()
            i = 0
            while True:
                try:
                    perm = tj.trotter_johnson_successor(n, perm)
                    unranked = tj.trotter_johnson_unrank(n, tj.trotter_johnson_rank(n, perm))
                    i += 1
                    assert np.array_equal(perm, unranked)
                except NoSuccessorError:
                    assert i == math.factorial(n) - 1
                    break
