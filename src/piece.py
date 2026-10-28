from bag import next_from_bag, next_from_next
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


START_POS = vec2(3, 0)
GRAVITY_TIME = 500

gravity_timer = 0
p = Piece(next_from_next(), START_POS, 0)


def input(event: pygame.Event):
    global gravity_timer

    if event.type == pygame.KEYDOWN:
        match event.key:
            case pygame.K_a:
                try_move(vec2(-1, 0))
            case pygame.K_d:
                try_move(vec2(1, 0))
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


def tick(delta: float):
    global gravity_timer

    gravity_timer += delta
    if gravity_timer > GRAVITY_TIME:
        moved = try_move(vec2(0, 1))
        if not moved:
            place_piece()
        gravity_timer = 0


def try_move(vec: vec2) -> bool:
    global p

    test = copy(p)
    test.pos = p.pos + vec
    moved = test.can_exist()
    if moved:
        p = test
    return moved


def try_rotate(new_rot: int):
    global p

    test = copy(p)
    test.rot = new_rot
    if test.can_exist():
        p = test


def place_piece():
    global p

    board.place(p)
    p = Piece(next_from_next(), START_POS, 0)
