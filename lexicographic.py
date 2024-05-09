import math

import numpy as np

from errors import NoSuccessorError


def perm_lex_successor(n: int, perm: list[int]) -> list[int]:
    """
    Find the lexicographically next permutation of a sequence of integers.

    :param n: Number of integers in the permutation
    :param perm: Permutation of integers 1 to n in list form
    :return: Lexicographically next permutation in list form
    :raises NoSuccessorError: If the input permutation is the last one in lexicographic order
    """
    successor = perm.copy()

    # Find the smallest index i such that pi[i] < pi[i+1]
    i = n - 2
    while i >= 0 and perm[i + 1] < perm[i]:
        i -= 1
    # if i = 0, then pi=[n, n-1, ..., 1], which has no successor
    if i < 0:
        raise NoSuccessorError('No successor')
    # Find the largest index j such that pi[j] > pi[i]
    j = n - 1
    while perm[j] < perm[i]:
        j -= 1
    # Swap pi[i] and pi[j]
    successor[j] = perm[i]
    successor[i] = perm[j]

    # Reverse the order of the elements after index i
    successor_tail = successor[i + 1:]
    successor[i + 1:] = successor_tail[::-1]

    return successor


def perm_lex_rank(n: int, perm: list[int]) -> int:
    """
    Find the lexicographic rank of a permutation of integers.

    :param n: Number of integers in the permutation
    :param perm: Permutation of integers 1 to n in list form
    :return: Lexicographic rank of the permutation
    """
    rank = 0
    rho = perm.copy()
    for j in range(n):
        rank = rank + (rho[j] - 1) * math.factorial(n - j - 1)
        for i in range(j + 1, n):
            if rho[i] > rho[j]:
                rho[i] = rho[i] - 1

    return rank


def perm_lex_unrank(n: int, rank: int) -> list[int]:
    """
    Find the permutation of integers with a given lexicographic rank.
    :param n: Number of integers in the permutation
    :param rank: Lexicographic rank of the permutation
    :return: Permutation of integers 1 to n in list form
    """
    perm = np.zeros(n, dtype=int)
    perm[n - 1] = 1
    for j in range(n - 1):
        numerator = (rank % math.factorial(j + 2))
        denominator = math.factorial(j + 1)
        d = numerator / denominator
        rank = rank - d * math.factorial(j + 1)
        perm[n - j - 2] = d + 1
        for i in range(n - j - 1, n):
            if perm[i] > d:
                perm[i] = perm[i] + 1
    return perm.tolist()



N = 8
permutation = np.arange(1, N + 1)
while True:
    try:
        ranked = perm_lex_rank(N, permutation)
        unranked = perm_lex_unrank(N, ranked)
        print(ranked, unranked, permutation)
        assert np.array_equal(unranked, permutation)
        permutation = perm_lex_successor(N, permutation)
    except NoSuccessorError:
        print("finished")
        break
