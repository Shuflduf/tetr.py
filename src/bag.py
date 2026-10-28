from copy import copy
from random import shuffle

NEXT_COUNT = 2
STARTING_BAG = [0, 1, 2, 3, 4, 5, 6]

bag: list[int] = []
next: list[int] = []


def fresh_bag():
    global bag
    bag = copy(STARTING_BAG)
    shuffle(bag)


def next_from_bag() -> int:
    n = bag.pop()
    if len(bag) == 0:
        fresh_bag()
    return n


def next_from_next() -> int:
    n = next.pop()
    next.insert(0, next_from_bag())
    return n


fresh_bag()
for _ in range(NEXT_COUNT):
    next.append(next_from_bag())
