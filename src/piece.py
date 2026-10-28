from copy import copy
import board
from srs import srs
import pygame
from helper import vec2


class Piece:
    def __init__(self):
        self.idx = 0
        self.pos = vec2(3, 0)
        self.rot = 0

    def can_exist(self):
        for offset in srs["pieces"][self.idx][self.rot]:
            if not board.safe_pos(self.pos + vec2(offset)):
                return False
        return True


GRAVITY_TIME = 500

gravity_timer = 0
p = Piece()


def input(event: pygame.Event):
    global gravity_timer

    if event.type == pygame.KEYDOWN:
        match event.key:
            case pygame.K_a:
                try_move(vec2(-1, 0))
            case pygame.K_d:
                try_move(vec2(1, 0))
            case pygame.K_w:
                try_move(vec2(0, 1))
                gravity_timer = 0.0
            case pygame.K_LEFT:
                try_rotate((p.rot + 3) % 4)
            case pygame.K_RIGHT:
                try_rotate((p.rot + 1) % 4)


def tick(delta: float):
    global gravity_timer

    gravity_timer += delta
    if gravity_timer > GRAVITY_TIME:
        try_move(vec2(0, 1))
        gravity_timer = 0


def try_move(vec: vec2):
    global p

    test = copy(p)
    test.pos = p.pos + vec
    if test.can_exist():
        p = test


def try_rotate(new_rot: int):
    global p

    test = copy(p)
    test.rot = new_rot
    if test.can_exist():
        p = test
