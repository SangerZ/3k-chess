import pygame
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Three Kingdoms Chess")
    
    game = Game(screen)
    game.start()

    pygame.quit()

if __name__ == "__main__":
    main()