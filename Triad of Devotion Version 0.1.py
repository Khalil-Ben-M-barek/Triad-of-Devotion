import pygame
import sys

white = (255,255,255)
blue = (0,0,150)
gray = (100,100,100)
yellow = (255,255,0)
menu_rect = (100,420,500,150) #x, y, width, and height
menu_grid = [["Basic Attack", "Ability", "Magic"], ["Synergy Ability", "Potential Breach", ""]]

def draw_battle_menu(surface, font, col, row):
    pygame.draw.rect(surface, blue, menu_rect)
    pygame.draw.rect(surface, white, menu_rect, 2)

    for c in range(2):
        for r in range(3):
            text = menu_grid[c][r]
            if text == "":
                continue

            tx = menu_rect[0] + 60 + (c * 260)
            ty = menu_rect[1] + 15 + (r * 32)
            text_color = white

            if text in ["Synergy Ability", "Potential Breach"]:
                text_color = gray
            if c == col and r == row:
                text_color = yellow
            
            img = font.render(text, True, text_color)
            surface.blit(img, (tx, ty))
            if c == col and r == row:
                pointer_x = (tx - 35)
                pointer_y = (ty + 10)
                pygame.draw.polygon(surface, white, [(pointer_x, pointer_y), (pointer_x + 15, pointer_y + 7), (pointer_x, pointer_y + 14)])

def main():
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 22)

    ethan_img = pygame.image.load("ethan.png").convert_alpha()
    boss_img = pygame.image.load("boss.png").convert_alpha()
    
    ethan_img = pygame.transform.scale(ethan_img, (150, 200))

    ethan_base_x, ethan_base_y = 550, 250
    boss_base_x, boss_base_y = 150, 50

    ethan_x, ethan_y = ethan_base_x, ethan_base_y
    boss_x, boss_y = boss_base_x, boss_base_y

    is_attacking = False
    attack_timer = 0

    cur_col = 0
    cur_row = 0

    pygame.mixer.init()

    music = pygame.mixer.Sound("battle_theme.mp3")
    music.play()

    is_runniung = True
    while is_runniung:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_runniung = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    cur_row = (cur_row - 1) % 3
                if event.key == pygame.K_DOWN:
                    cur_row = (cur_row + 1) % 3
                if event.key == pygame.K_RIGHT:
                    cur_col = (cur_col + 1) % 2
                if event.key == pygame.K_LEFT:
                    cur_col = (cur_col - 1) % 2
                if event.key == pygame.K_SPACE:
                    cur_selection = menu_grid[cur_col][cur_row]
                    if cur_selection in ["Synergy Ability", "Potential Breach"]:
                        print("You can't use that yet!")
                    else:
                        print(f"You chose: {cur_selection}")
                        is_attacking = True
                        attack_timer = 40
        if is_attacking:
            if attack_timer > 25: # first phase of the animation
                ethan_x -= 20
                ethan_y -= 10
            elif attack_timer > 15: # second phase of the animation
                pass
            elif attack_timer > 0:
                ethan_x += 20
                ethan_y += 10

            attack_timer -= 1 # countdown timer

            if attack_timer <= 0:
                is_attacking == False
                ethan_x, ethan_y = ethan_base_x, ethan_base_y

        screen.fill((30,30,30))
        draw_battle_menu(screen, font, cur_col, cur_row)
        screen.blit(ethan_img, (ethan_x, ethan_y))
        screen.blit(boss_img, (boss_x, boss_y))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

