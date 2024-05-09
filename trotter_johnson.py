import math

import numpy as np

from errors import NoSuccessorError
from util import is_even


def trotter_johnson_rank(n: int, perm: list[int]) -> int:
    """
    Find the Trotter-Johnson rank of a permutation of integers.

    :param n: Number of integers in the permutation.
    :param perm: Permutation of integers 1 to n in list form.
    :return: Trotter-Johnson rank of the permutation.
    """
    rank = 0
    for j in range(2, n + 1):
        k = 1
        i = 0
        while perm[i] != j:
            if perm[i] < j:
                k += 1
            i += 1
        # Different cases described in the Trotter-Johnson algorithm depending on whether
        # the current rank is even or odd
        if is_even(rank):
            rank = j * rank + j - k
        else:
            rank = j * rank + k - 1
    return rank


def trotter_johnson_unrank(n: int, rank: int) -> list[int]:
    """
    Find the permutation of integers with a given Trotter-Johnson rank.

    :param n: Number of integers in the permutation.
    :param rank: Trotter-Johnson rank of the permutation.
    :return: Permutation of integers 1 to n in list form.
    """
    perm = np.zeros(n, dtype=int)
    perm[0] = 1
    r2 = 0
    for j in range(1, n):
        r1 = math.floor((rank * math.factorial(j + 1)) / math.factorial(n))
        k = r1 - (j + 1) * r2
        shift_start = j
        if is_even(r2):
            shift_end = j - k
        else:
            shift_end = k
        for i in range(shift_start, shift_end, -1):
            perm[i] = perm[i - 1]
        perm[shift_end] = j + 1
        r2 = r1
    return perm.tolist()


def perm_parity(n: int, perm: list[int]) -> int:
    """
    Find the parity of a permutation of integers.

    :param n: Amount of integers in the permutation.
    :param perm: Permutation of integers 1 to n in list form.
    :return: Parity of the permutation.
    """
    a = np.zeros(n, dtype=int)

    c = 0
    for j in range(1, n + 1):
        if a[j - 1] == 0:
            c += 1
            a[j - 1] = 1
            i = j
            while perm[i - 1] != j:
                i = perm[i - 1]
                a[i - 1] = 1
    return (n - c) % 2


def trotter_johnson_successor(n: int, perm: list[int]) -> list[int]:
    """
    Find the Trotter-Johnson next permutation of a sequence of integers.

    :param n: Number of integers in the permutation.
    :param perm: Permutation of integers 1 to n in list form.
    :return: Trotter-Johnson next permutation in list form.
    :raises NoSuccessorError: If the input permutation is the last one in Trotter-Johnson order.
    """
    assert len(perm) == n
    st = 0
    successor = perm.copy()
    rho = perm.copy()
    done = False
    m = n
    while m > 1 and not done:
        d = 0
        while rho[d] != m:
            d += 1
        for i in range(d, m - 1):
            rho[i] = rho[i + 1]
        par = perm_parity(m - 1, rho)
        if par == 1:
            if d == m - 1:
                # Case 4
                m -= 1
            else:
                # Case 2
                successor[st + d] = perm[st + d + 1]
                successor[st + d + 1] = perm[st + d]
                done = True
        else:
            if d == 0:
                # Case 3
                m -= 1
                st += 1
            else:
                # Case 1
                successor[st + d] = perm[st + d - 1]
                successor[st + d - 1] = perm[st + d]
                done = True
    if m == 1:
        raise NoSuccessorError("No successor")
    return successor
