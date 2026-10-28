import piece
from srs import srs
from helper import vec2
from pygame.locals import Rect, Color
import pygame


cols, rows = 10, 20
colours = [
    Color("#ff3030"),
    Color("#ff8330"),
    Color("#ffd130"),
    Color("#60ec3f"),
    Color("#3fd2ec"),
    Color("#3f53ec"),
    Color("#ff4fe0"),
]
board_colour = Color("#262626")

tiles: list[list[int | None]] = [[None for _ in range(rows)] for _ in range(cols)]
size, x, y = 0.0, 0.0, 0.0


def draw(surface: pygame.Surface):
    global size, x, y
    w, h = surface.get_size()
    size = min(h / (rows + 1), w / (cols + 2))
    x = (w - size * cols) / 2
    y = (h - size * (rows + 1)) / 2
    draw_outline(surface)
    draw_piece(surface)


def draw_tile(surface: pygame.Surface, colour: pygame.Color, pos: vec2):
    pygame.draw.rect(
        surface, colour, Rect(x + size * pos.x, y + size * pos.y, size + 1, size + 1)
    )


def draw_outline(surface: pygame.Surface):
    pygame.draw.rect(surface, board_colour, Rect(x - size, y, size, size * (rows + 1)))
    pygame.draw.rect(
        surface, board_colour, Rect(x + (size * cols), y, size, size * (rows + 1))
    )
    pygame.draw.rect(
        surface,
        board_colour,
        Rect(x - size, y + (size * rows), size * (cols + 1), size),
    )


def draw_piece(surface: pygame.Surface):
    for pos in srs["pieces"][piece.p.idx][piece.p.rot]:
        draw_tile(surface, colours[piece.p.idx], piece.p.pos + vec2(pos))


def safe_pos(pos: vec2) -> bool:
    if pos.x < 0 or pos.x > cols - 1 or pos.y < 0 or pos.y > rows - 1:
        return False

    return tiles[pos.x][pos.y] == None
