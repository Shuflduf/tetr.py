import bag
import piece
import asyncio
import pygame
import board

pygame.init()
screen = pygame.display.set_mode(flags=pygame.RESIZABLE)
clock = pygame.time.Clock()

CONTROLS: list[str] = [
    "A - LEFT",
    "D - RIGHT",
    "LEFT - CCW",
    "RIGHT - CW",
    "S - HARD",
    "W - SOFT",
    "SHIFT - HOLD",
]


def reset():
    bag.init()
    board.init()
    piece.init()


async def main():
    delta = 0.0
    running = True
    big_font = pygame.font.Font("PressStart2P-Regular.ttf", 40)
    small_font = pygame.font.Font("PressStart2P-Regular.ttf", 25)
    text = big_font.render("TETR.PY", False, pygame.Color("#FFFFFF"))
    text_rect = text.get_rect().move(20.0, 20.0)
    controls_texts: list[pygame.Surface] = []
    for c in CONTROLS:
        ct = small_font.render(c, False, pygame.Color("#4C4C4C"))
        controls_texts.append(ct)
    controls_texts.reverse()

    reset()
    pygame.font.init()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                piece.input(event)
        screen.fill((0, 0, 0))
        piece.tick(delta)
        board.draw(screen)
        screen.blit(text, text_rect)
        _, h = screen.get_size()
        for i, c in enumerate(controls_texts):
            screen.blit(
                c,
                c.get_rect()
                .move(0.0, h - c.get_rect().height - i * 30.0)
                .move(10.0, -10.0),
            )

        pygame.display.flip()
        # screen.fli
        delta = clock.tick(60)
        await asyncio.sleep(0)


asyncio.run(main())
