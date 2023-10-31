# Fibonacci sequence

from functools import lru_cache

""" Memoization of cache approach
@lru_cache
def fib_rec(n):
    if n<=1:
        return 1
    return fib_rec(n -1) + fib_rec(n-2)
"""

# 1 2 3
"""
def fib_rec(n):
    fib_0 = 1
    fib_1 = 1

    for i in range(n -1):
        
        fib_0 ,fib_1 = fib_1, fib_0 + fib_1
        print(fib_0, fib_1)
        # print(fib_0, "+", fib_1 , " = " , fib_1)
        # temp = fib_1
        # fib_0 = fib_1
        # fib_1 = temp + fib_1

    
    return fib_1
"""

#1 1 
def fib(n):
    fib_1 = 1
    yield fib_1
    fib_2 = 1
    yield fib_2

    # if n<=1:
    #     yield 1
    
    for _ in range(n-2):
        result = fib_1 + fib_2 
        fib_1 = fib_2
        fib_2 = result 
        yield  result

def square_gen(n):
    for i in range(n):
        yield i ** 2
    
from collections import namedtuple

Card = namedtuple("Card", "rank suit")
SUITS = ("Spades", "Hearts", "Diamonds", "Clubs")
RANKS = tuple(range(2,11)) + tuple("JQKA")
def card_gen():

    for i in range(len(SUITS) * len(RANKS)):
        suit_index = i // len(RANKS)
        rank_index = i % len(RANKS)
        print(suit_index, rank_index)
        suit = SUITS[suit_index]
        rank = RANKS[rank_index]
        yield Card(rank=rank, suit=suit)
    

if __name__ == "__main__":

    # print(fib_rec(5))
    import time
    start = time.perf_counter()


    # gen = fib(7)
    # print([i for i in gen])

    # sq_gen = square_gen(5)
    # for each in sq_gen:
        # print(each)

    ca = card_gen()
    for each in ca:
        print(each)
    end = time.perf_counter()
    print(end- start)