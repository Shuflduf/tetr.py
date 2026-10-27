import json
from piece import Piece
import asyncio
import pygame
import board

pygame.init()
screen = pygame.display.set_mode(flags=pygame.RESIZABLE)
clock = pygame.time.Clock()


def reset(): ...


async def main():

    running = True
    reset()
    Piece()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        # screen.size
        board.draw(screen)
        pygame.display.flip()
        # screen.fli
        clock.tick(60)
        await asyncio.sleep(0)


asyncio.run(main())
