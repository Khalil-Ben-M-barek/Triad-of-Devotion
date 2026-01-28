import pygame
import sys
import random

white = (255, 255, 255)
blue = (0, 0, 150)
gray = (100, 100, 100)
yellow = (255, 255, 0)
orange = (255, 165, 0)
green = (0, 255, 0)

menu_rect = (100,420,500,150) #x, y, width, and height
battle_menu = [["Attack", "Magic"], ["Synergy Ability", "Potential Breach"]]
attack_submenu = ["Basic Attack", "Counter", "Back"]

ethan_hp, ethan_max_hp = 1000, 1000
boss_hp, boss_max_hp = 6000, 6000
potential_val, potential_max = 0, 100

def take_damage(amount, target = "ethan"):
    global ethan_hp, potential_val, boss_hp
    if target == "ethan":
        ethan_hp -= amount
        potential_gain = (amount / ethan_max_hp) * 170
        potential_val = min(potential_max, potential_val + potential_gain) # To not exceed the max
        print(f"Ethan took {amount} damage! \n Potential gauge increased")

    elif target == "boss":
        boss_hp -= amount

def draw_potential_bar(surface, x, y):
    pygame.draw.rect(surface, gray, (x, y, 150, 20))
    fill_width = (potential_val / potential_max) * 150
    bar_color = orange if potential_val >= potential_max else white
    pygame.draw.rect(surface, bar_color, (x, y, fill_width, 20))
    pygame.draw.rect(surface, white, (x, y, 150, 20), 1) # Border

def draw_battle_menu(surface, font, col, row, cur_menu, sub_row):
    global boss_hp, boss_max_hp, boss_base_x, boss_base_y
    pygame.draw.rect(surface, blue, menu_rect)
    pygame.draw.rect(surface, white, menu_rect, 2)
    pygame.draw.rect(surface, gray, (620, 480, 150, 15)) # HP bar
    pygame.draw.rect(surface, green, (620, 480, (ethan_hp / ethan_max_hp) * 150, 15))
    surface.blit(font.render(f"HP: {ethan_hp}/{ethan_max_hp}", True, white), (620, 460))

    pygame.draw.rect(surface, gray, (boss_base_x - 20, boss_base_y - 20, 150, 15)) # HP bar
    pygame.draw.rect(surface, green, (boss_base_x - 20, boss_base_y - 20, (boss_hp / boss_max_hp) * 150, 15))
    surface.blit(font.render(f"HP: {boss_hp}/{boss_max_hp}", True, white), (boss_base_x - 20, boss_base_y - 50))

    if cur_menu == "MAIN BATTLE MENU":
        for c in range(2):
            for r in range(2):
                text = battle_menu[c][r]

                tx = menu_rect[0] + 60 + (c * 260)
                ty = menu_rect[1] + 15 + (r * 32)
                
                text_color = white
                if text == "Potential Breach" and potential_val < potential_max:
                    text_color = gray
                elif text == "Synergy Ability":
                    text_color = gray
                if c == col and r == row:
                    text_color = yellow
                
                img = font.render(text, True, text_color)
                surface.blit(img, (tx, ty))
                if c == col and r == row:
                    pointer_x = (tx - 35)
                    pointer_y = (ty + 10)
                    pygame.draw.polygon(surface, white, [(pointer_x, pointer_y), (pointer_x + 15, pointer_y + 7), (pointer_x, pointer_y + 14)])

    elif cur_menu == "ATTACK SUBMENU":
        for i, text in enumerate(attack_submenu):
            tx = menu_rect[0] + 60
            ty = menu_rect[1] + 15 + (i * 32)
            text_color = yellow if i == sub_row else white
            surface.blit(font.render(text, True, text_color), (tx, ty))
            if i == sub_row:
                pygame.draw.polygon(surface, white, [(tx - 35, ty + 10), (tx - 20, ty + 17), (tx - 35, ty + 24)])

def main():
    global potential_val # To allow updating
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 22)

    ethan_img = pygame.image.load("ethan.png").convert_alpha()
    boss_img = pygame.image.load("boss.png").convert_alpha()
    
    ethan_img = pygame.transform.scale(ethan_img, (150, 200))

    
    global boss_base_x, boss_base_y
    ethan_base_x, ethan_base_y = 550, 250
    boss_base_x, boss_base_y = 150, 50

    ethan_x, ethan_y = ethan_base_x, ethan_base_y
    boss_x, boss_y = boss_base_x, boss_base_y

    is_attacking = False
    attack_timer = 0
    enemy_is_attacking = False
    enemy_attack_timer = 0

    cur_menu = "MAIN BATTLE MENU"
    cur_col, cur_row, sub_row = 0, 0, 0

    pygame.mixer.init()

    music = pygame.mixer.Sound("battle_theme.mp3")
    music.play()

    is_runniung = True
    while is_runniung:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_runniung = False

            if event.type == pygame.KEYDOWN:
                if cur_menu == "MAIN BATTLE MENU":

                    if event.key == pygame.K_UP:
                        cur_row = (cur_row - 1) % 2
                    if event.key == pygame.K_DOWN:
                        cur_row = (cur_row + 1) % 2
                    if event.key == pygame.K_RIGHT:
                        cur_col = (cur_col + 1) % 2
                    if event.key == pygame.K_LEFT:
                        cur_col = (cur_col - 1) % 2
                    if event.key == pygame.K_SPACE and not is_attacking and not enemy_is_attacking:
                        if battle_menu[cur_col][cur_row] == "Attack":
                            cur_menu = "ATTACK SUBMENU"
                     
                        
                elif cur_menu == "ATTACK SUBMENU":
                    if event.key == pygame.K_UP:
                        sub_row = (sub_row - 1) % len(attack_submenu)
                    if event.key == pygame.K_DOWN:
                        sub_row = (sub_row + 1) % len(attack_submenu)
                    if event.key == pygame.K_SPACE and not is_attacking and not enemy_is_attacking:
                        if attack_submenu[sub_row] == "Back":
                            cur_menu = "MAIN BATTLE MENU"
                        else:
                            is_attacking = True
                            attack_timer = 40
                            cur_menu = "MAIN BATTLE MENU"


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

            if attack_timer == 0:
                is_attacking = False
                ethan_x, ethan_y = ethan_base_x, ethan_base_y

                enemy_is_attacking = True
                enemy_attack_timer = 40
                take_damage(random.randint(100, 150), "boss")
        if enemy_is_attacking:
            if enemy_attack_timer > 25: # first phase of the animation
                boss_x += 20
                boss_y += 10
            elif enemy_attack_timer > 15: # second phase of the animation
                pass
            elif enemy_attack_timer > 0:
                boss_x -= 20
                boss_y -= 10

            enemy_attack_timer -= 1 # countdown timer

            if enemy_attack_timer == 0:
                enemy_is_attacking = False
                boss_x, boss_y = boss_base_x, boss_base_y
        
                take_damage(random.randint(100,150), "ethan")


        screen.fill((30,30,30))
        draw_battle_menu(screen, font, cur_col, cur_row, cur_menu, sub_row)
        draw_potential_bar(screen, 420, 500)
        screen.blit(ethan_img, (ethan_x, ethan_y))
        screen.blit(boss_img, (boss_x, boss_y))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

