import math
import unittest

import numpy as np

import lexicographic as lex
from errors import NoSuccessorError


class LexicographicTest(unittest.TestCase):

    def test_rank(self):
        self.assertEqual(lex.perm_lex_rank(3, [1, 2, 3]), 0)
        self.assertEqual(lex.perm_lex_rank(3, [1, 3, 2]), 1)
        self.assertEqual(lex.perm_lex_rank(3, [2, 1, 3]), 2)
        self.assertEqual(lex.perm_lex_rank(3, [2, 3, 1]), 3)
        self.assertEqual(lex.perm_lex_rank(3, [3, 1, 2]), 4)
        self.assertEqual(lex.perm_lex_rank(3, [3, 2, 1]), 5)

    def test_unrank(self) -> None:
        assert np.array_equal(lex.perm_lex_unrank(3, 0), [1, 2, 3])
        assert np.array_equal(lex.perm_lex_unrank(3, 1), [1, 3, 2])
        assert np.array_equal(lex.perm_lex_unrank(3, 2), [2, 1, 3])
        assert np.array_equal(lex.perm_lex_unrank(3, 3), [2, 3, 1])
        assert np.array_equal(lex.perm_lex_unrank(3, 4), [3, 1, 2])
        assert np.array_equal(lex.perm_lex_unrank(3, 5), [3, 2, 1])

    def test_successor(self):
        for n in range(1, 10):
            perm = np.arange(1, n + 1).tolist()
            i = 1
            while True:
                try:
                    perm = lex.perm_lex_successor(n, perm)
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
                    perm = lex.perm_lex_successor(n, perm)
                    i += 1
                    assert lex.perm_lex_rank(n, perm) == i
                except NoSuccessorError:
                    assert i == math.factorial(n) - 1
                    break

    def test_rank_unrank(self):
        for n in range(1, 8):
            perm = np.arange(1, n + 1).tolist()
            i = 0
            while True:
                try:
                    perm = lex.perm_lex_successor(n, perm)
                    unranked = lex.perm_lex_unrank(n, lex.perm_lex_rank(n, perm))
                    i += 1
                    assert np.array_equal(perm, unranked)
                except NoSuccessorError:
                    assert i == math.factorial(n) - 1
                    break
