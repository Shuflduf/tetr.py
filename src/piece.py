from enum import Enum
from bag import next_from_next
from copy import copy
import board
from srs import srs
import pygame
from helper import vec2


class Piece:
    def __init__(self, idx: int, pos: vec2, rot: int):
        self.idx = idx
        self.pos = pos
        self.rot = rot

    def can_exist(self):
        for offset in srs["pieces"][self.idx][self.rot]:
            if not board.safe_pos(self.pos + vec2(offset)):
                return False
        return True


class MovingDir(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2


START_POS = vec2(3, 0)
GRAVITY_TIME = 500
DAS_TIME = 168
ARR_TIME = 33
SDF_TIME = 100

gravity_timer = 0
das_timer = 0
sdf_timer = 0
ghost_offset = 0
p = Piece(next_from_next(), START_POS, 0)
inputs = {"left": False, "right": False, "moving": MovingDir.NONE}


def input(event: pygame.Event):
    global gravity_timer, das_timer

    if event.type == pygame.KEYDOWN:
        match event.key:
            case pygame.K_a:
                try_move(vec2(-1, 0))
                inputs["left"] = True
                inputs["moving"] = MovingDir.LEFT
                das_timer = 0
            case pygame.K_d:
                try_move(vec2(1, 0))
                inputs["right"] = True
                inputs["moving"] = MovingDir.RIGHT
                das_timer = 0
            case pygame.K_w:
                if try_move(vec2(0, 1)):
                    gravity_timer = 0.0
            case pygame.K_LEFT:
                try_rotate((p.rot + 3) % 4)
            case pygame.K_RIGHT:
                try_rotate((p.rot + 1) % 4)
            case pygame.K_s:
                while try_move(vec2(0, 1)):
                    pass
                place_piece()
    elif event.type == pygame.KEYUP:
        match event.key:
            case pygame.K_a:
                inputs["left"] = False
                if inputs["right"]:
                    inputs["moving"] = MovingDir.RIGHT
                    try_move(vec2(1, 0))
                else:
                    inputs["moving"] = MovingDir.NONE
            case pygame.K_d:
                inputs["right"] = False
                if inputs["left"]:
                    inputs["moving"] = MovingDir.LEFT
                    try_move(vec2(-1, 0))
                else:
                    inputs["moving"] = MovingDir.NONE


def tick(delta: float):
    global gravity_timer, das_timer

    gravity_timer += delta
    if gravity_timer > GRAVITY_TIME:
        moved = try_move(vec2(0, 1))
        if not moved:
            place_piece()
        gravity_timer = 0

    if inputs["moving"] != MovingDir.NONE:
        das_timer += delta
        if das_timer > DAS_TIME:
            match inputs["moving"]:
                case MovingDir.LEFT:
                    try_move(vec2(-1, 0))
                case MovingDir.RIGHT:
                    try_move(vec2(1, 0))
            das_timer -= ARR_TIME


def try_move(vec: vec2) -> bool:
    global p

    test = copy(p)
    test.pos = p.pos + vec
    moved = test.can_exist()
    if moved:
        p = test
        recalc_ghost()
    return moved


def try_rotate(new_rot: int):
    global p

    test = copy(p)
    test.rot = new_rot
    if test.can_exist():
        p = test
        recalc_ghost()


def place_piece():
    global p

    board.place(p)
    p = Piece(next_from_next(), START_POS, 0)
    recalc_ghost()


def recalc_ghost():
    global ghost_offset

    ghost_offset = -1
    test = copy(p)
    while test.can_exist():
        test.pos += vec2(0, 1)
        ghost_offset += 1


recalc_ghost()
