import piece
import asyncio
import pygame
import board

pygame.init()
screen = pygame.display.set_mode(flags=pygame.RESIZABLE)
clock = pygame.time.Clock()


def reset(): ...


async def main():
    delta = 0.0
    running = True
    reset()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                piece.input(event)
        screen.fill((0, 0, 0))
        piece.tick(delta)
        board.draw(screen)
        pygame.display.flip()
        # screen.fli
        delta = clock.tick(60)
        await asyncio.sleep(0)


asyncio.run(main())
