from typing import TypedDict
import json


class PieceTable(TypedDict):
    pieces: list[list[list[tuple[int, int]]]]
    kicks: list[list[tuple[int, int]]]
    kicks_i: list[list[tuple[int, int]]]


with open("srs.json") as t:
    srs: PieceTable = json.load(t)
