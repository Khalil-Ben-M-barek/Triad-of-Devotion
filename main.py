import pygame
import sys
from battle import run_battle
from constants import display_res, internal_res, protect_used_this_turn

# The game is beatable in as few as 65 enemy turns (my test run). Maybe try to beat my score (hint: The default ENABLER loadout is intentionally not the best, so I didn't use it)

def main():
    pygame.init()
    window = pygame.display.set_mode(display_res, pygame.RESIZABLE)
    virtual_screen = pygame.Surface(internal_res)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 22)
    small_font = pygame.font.SysFont("Arial", 16)
    pygame.display.set_caption("Triad of Devotion")
    pygame.display.set_icon(pygame.image.load("assets/images/icon.png"))
    run_battle(virtual_screen, window, display_res, font, small_font, clock, None, None)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()