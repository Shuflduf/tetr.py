from curses import update_lines_cols
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


I_PIECE_IDX = 4
START_POS = vec2(3, 0)
GRAVITY_TIME = 500
DAS_TIME = 168
ARR_TIME = 33
SDF_TIME = 100
LOCK_DELAY_TIME = 500
MAX_LOCK_DELAY_TIME = 2000

gravity_timer = 0
das_timer = 0
sdf_timer = 0
ghost_offset = 0
lock_delay_timer = 0
max_lock_delay_timer = 0
touched_ground: int | None = None
p = Piece(next_from_next(), START_POS, 0)
held: int | None = None
just_held = False
inputs = {"left": False, "right": False, "down": False, "moving": MovingDir.NONE}


def input(event: pygame.Event):
    global gravity_timer, das_timer, sdf_timer, held, just_held, p

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
                inputs["down"] = True
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
            case pygame.K_LSHIFT:
                if not just_held:
                    if held:
                        temp = p.idx
                        p = Piece(held, START_POS, 0)
                        recalc_ghost()
                        held = temp
                        just_held = True
                    else:
                        held = p.idx
                        p = Piece(next_from_next(), START_POS, 0)
                        recalc_ghost()
                        just_held = True

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
            case pygame.K_w:
                inputs["down"] = False
                sdf_timer = 0


def check_lock_delay(delta: float):
    global touched_ground, lock_delay_timer, max_lock_delay_timer

    temp = copy(p)
    temp.pos += vec2(0, 1)
    grounded = not temp.can_exist()
    if grounded:
        if touched_ground == None or p.pos.y > touched_ground:
            touched_ground = p.pos.y
            max_lock_delay_timer = 0
        lock_delay_timer += delta
        max_lock_delay_timer += delta
        if (
            lock_delay_timer > LOCK_DELAY_TIME
            or max_lock_delay_timer > MAX_LOCK_DELAY_TIME
        ):
            place_piece()
    else:
        lock_delay_timer = 0


def tick(delta: float):
    global gravity_timer, das_timer, sdf_timer

    gravity_timer += delta
    if gravity_timer > GRAVITY_TIME:
        try_move(vec2(0, 1))
        # if not moved:
        #     place_piece()
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

    if inputs["down"]:
        sdf_timer += delta
        if sdf_timer > SDF_TIME:
            sdf_timer = 0
            gravity_timer = 0
            try_move(vec2(0, 1))

    check_lock_delay(delta)


def try_move(vec: vec2) -> bool:
    global p, lock_delay_timer

    test = copy(p)
    test.pos = p.pos + vec
    moved = test.can_exist()
    if moved:
        p = test
        recalc_ghost()
        lock_delay_timer = 0
    return moved


def try_rotate(new_rot: int):
    global p, lock_delay_timer

    test = copy(p)
    test.rot = new_rot
    if test.can_exist():
        p = test
        recalc_ghost()
        lock_delay_timer = 0
    else:
        table = srs["kicks"] if p.idx != I_PIECE_IDX else srs["kicks_i"]
        for kick in table[kick_index(p.rot, new_rot)]:
            test.pos = p.pos + vec2(kick)
            if test.can_exist():
                p = test
                recalc_ghost()
                lock_delay_timer = 0
                return


def place_piece():
    global \
        p, \
        just_held, \
        touched_ground, \
        gravity_timer, \
        lock_delay_timer, \
        max_lock_delay_timer

    board.place(p)
    p = Piece(next_from_next(), START_POS, 0)
    recalc_ghost()
    just_held = False

    touched_ground = None
    gravity_timer = 0
    lock_delay_timer = 0
    max_lock_delay_timer = 0


def kick_index(old_rot: int, new_rot: int) -> int:
    if new_rot == (old_rot + 1) % 4:
        return old_rot * 2
    else:
        return (old_rot * 2 + 7) % 8


def recalc_ghost():
    global ghost_offset

    ghost_offset = -1
    test = copy(p)
    while test.can_exist():
        test.pos += vec2(0, 1)
        ghost_offset += 1


recalc_ghost()
