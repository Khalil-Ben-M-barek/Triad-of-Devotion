import pygame
import sys
import random

white = (255, 255, 255)
blue = (0, 0, 150)
gray = (100, 100, 100)
yellow = (255, 255, 0)
orange = (255, 165, 0)
green = (0, 255, 0)
red = (255, 0, 0)

menu_rect = (50, 420, 440, 150) #x, y, width, and height
battle_menu = [["Attack", "Magic", "Protect Stance"], ["Synergy Ability", "Potential Breach"]]

class SynergyAbility:
    def __init__(self, name, description, partner, perk_type, damage):
        self.name = name
        self.description = description
        self.synergy_partner = partner
        self.perk_type = perk_type
        self.damage = damage
        self.synergy_bars_required = 3

# trying to incoorporate OOP elements
# to implement: synergy bars gained after entering a protect partner stance and blocking a full attack against that partner (both gain a bar). if blocking is missed, the character with the stance takes the full damage too. the protect stance can only be entered once before each enemy turn. if the enemy attacks anyone other than the protected (including the initiator), the protective stance fisles and the system returns to normal

class Characters:
    def __init__(self, name, hp, mp, x, y, image_path, is_enemy = False):
        self.name = name
        self.hp, self.max_hp = hp, hp
        self.mp, self.max_mp = mp, mp
        self.base_x, self.base_y = x, y
        self.x, self.y = x, y
        self.is_enemy = is_enemy
        self.potential_value = 0
        self.max_potential_value = 100
        self.abilities = []
        self.synergy_abilities = []
        self.zero_mp_cost = False
        self.potential_level = 1
        self.synergy_bars = 0
        self.max_synergy_bars = 5
        self.is_protecting_target = None
        self.chi_level = 0
        self.cooldowns = {}
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 200))
        self.is_attacking = False
        self.attack_timer = 0

    def take_damage(self, amount, party):
        protector = None
        for p in party:
            if p.is_protecting_target == self:
                protector = p
                break
        if protector:
            block_success = random.choice([True, False]) #Test blocking. blocking implimentation later
            if block_success:
                protector.synergy_bars = min(protector.max_synergy_bars, protector.synergy_bars + 1)
                self.synergy_bars = min(self.max_synergy_bars, self.synergy_bars + 1)
                protector.is_protecting_target = None
                return
            else:
                self.hp = max(0, self.hp - amount)
                protector.hp = max(0, protector.hp - amount)

        self.hp = max(0, self.hp - amount)

        if not self.is_enemy:
            potential_gain = (amount / self.max_hp) * 170
            self.potential_value = min(self.max_potential_value, self.potential_value + potential_gain) # To not exceed the max

def draw_individual_menus(virtual_screen, small_font, party, active_hero_index):
    for i, hero in enumerate(party):
        box_width, box_height = 200, 80
        box_x = 580
        box_y = 340 + (i * 75)
        color = (0, 180, 200) if i == active_hero_index else white
        pygame.draw.rect(virtual_screen, (15, 25, 35), (box_x, box_y, box_width, box_height))
        pygame.draw.rect(virtual_screen, color, (box_x, box_y, box_width, box_height), 2)

        name_surface = small_font.render(hero.name, True, color)
        hp_surface = small_font.render(f"HP: {hero.hp}/{hero.max_hp}", True, white)
        mp_surface = small_font.render(f"MP: {hero.mp}/{hero.max_mp}", True, white)

        virtual_screen.blit(name_surface, (box_x + 10, box_y + 5))
        virtual_screen.blit(hp_surface, (box_x + 10, box_y + 20))
        virtual_screen.blit(mp_surface, (box_x + 10, box_y + 35))

        hp_bar_x, hp_bar_y, hp_bar_width = box_x + 105, box_y + 25, 80
        pygame.draw.rect(virtual_screen, (80, 80, 80), (hp_bar_x, hp_bar_y, hp_bar_width, 10))
        
        hp_ratio = hero.hp / max(1, hero.max_hp)
        hp_color = green if hp_ratio > 0.4 else yellow if hp_ratio > 0.15 else red
        pygame.draw.rect(virtual_screen, hp_color, (hp_bar_x, hp_bar_y, hp_bar_width * hp_ratio, 10))
        pygame.draw.rect(virtual_screen, white, (hp_bar_x, hp_bar_y, hp_bar_width, 10), 1)


        for synergy_bar_number in range(hero.max_synergy_bars):
            synergy_bar_x = box_x + 10 + (synergy_bar_number * 10)
            synergy_bar_y = box_y + 55
            if synergy_bar_number < hero.synergy_bars:
                synergy_bar_color = (0, 200, 255)
            else:
                synergy_bar_color = (50, 50, 50)
            pygame.draw.rect(virtual_screen, synergy_bar_color, (synergy_bar_x, synergy_bar_y, 5, 12))
            
        potential_x, potential_y = box_x + 90, box_y + 55
        potential_is_full = hero.potential_value >= hero.max_potential_value
        potential_text = "POTENTIAL BREACH" if potential_is_full else "POTENTIAL"
        potential_color = orange if hero.potential_value >= hero.max_potential_value else white
        potential_fill_width = (hero.potential_value / hero.max_potential_value) * 100
        pygame.draw.rect(virtual_screen, (80, 80, 80), (potential_x, potential_y, 100, 15))
        pygame.draw.rect(virtual_screen, potential_color, (potential_x, potential_y, potential_fill_width, 15))
        pygame.draw.rect(virtual_screen, white, (potential_x, potential_y, 100, 15), 1) # Border
        virtual_screen.blit(small_font.render(potential_text, True, potential_color), (potential_x, potential_y - 20))

def get_unique_abilities(hero):
    abilities = ["Basic Attack"]
    if hero.name == "Ethan":
        abilities += ["Counter"]

    elif hero.name == "Elena":
        abilities += ["Charge"]
        if hero.chi_level == 1:
            abilities.append("Brute Force")
        if hero.chi_level == 2:
            abilities.append("Heavy Barrage")

    elif hero.name == "Evelyn":
        abilities += ["Twin Cast", "Twin Cast"]
    
    abilities.append("Back")
    return abilities

def draw_battle_menu(virtual_screen, font, col, row, cur_menu, sub_row, enemy, protect_options, hero, current_options):

    pygame.draw.rect(virtual_screen, blue, menu_rect)
    pygame.draw.rect(virtual_screen, white, menu_rect, 2)

    pygame.draw.rect(virtual_screen, gray, (enemy.base_x - 20, enemy.base_y - 20, 150, 15)) # HP bar
    pygame.draw.rect(virtual_screen, green, (enemy.base_x - 20, enemy.base_y - 20, (enemy.hp / enemy.hp) * 150, 15))
    virtual_screen.blit(font.render(f"HP: {enemy.hp}/{enemy.max_hp}", True, white), (enemy.base_x - 20, enemy.base_y - 50))

    if cur_menu == "MAIN BATTLE MENU":
        for c in range(2):
            for r in range(len(battle_menu[c])):
                text = battle_menu[c][r]

                tx = menu_rect[0] + 60 + (c * 200)
                ty = menu_rect[1] + 15 + (r * 32)
                
                text_color = white
                if text == "Potential Breach" and hero.potential_value < hero.max_potential_value:
                    text_color = gray
                elif text == "Synergy Ability":
                    text_color = gray
                if c == col and r == row:
                    text_color = yellow
                
                virtual_screen.blit(font.render(text, True, text_color), (tx, ty))

                if c == col and r == row:
                    pointer_x = (tx - 35)
                    pointer_y = (ty + 10)
                    pygame.draw.polygon(virtual_screen, white, [(pointer_x, pointer_y), (pointer_x + 15, pointer_y + 7), (pointer_x, pointer_y + 14)])

    elif cur_menu == "ATTACK SUBMENU" or cur_menu == "PROTECT SUBMENU":
        options = current_options if cur_menu  == "ATTACK SUBMENU" else protect_options
        for i, text in enumerate(options):
            tx = menu_rect[0] + 60
            ty = menu_rect[1] + 15 + (i * 32)
            text_color = yellow if i == sub_row else white
            virtual_screen.blit(font.render(text, True, text_color), (tx, ty))
            if i == sub_row:
                pygame.draw.polygon(virtual_screen, white, [(tx - 35, ty + 10), (tx - 20, ty + 17), (tx - 35, ty + 24)])

def main():
    pygame.init()
    internal_res = (800, 600)
    display_res = (1280, 720)
    
    window = pygame.display.set_mode(display_res, pygame.RESIZABLE)
    virtual_screen = pygame.Surface(internal_res)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 22)
    small_font = pygame.font.SysFont("Arial", 16)
    
    pygame.mixer.init()
    music = pygame.mixer.Sound("battle_theme.mp3")
    music.play(-1)
    cursor_sound = pygame.mixer.Sound("cursor.mp3")
    confirm_sound = pygame.mixer.Sound("confirm.mp3")

    protect_options = []
    party = [
        Characters("Ethan", 1000, 50, 550, 250, "ethan.png"), 
        Characters("Elena", 1000, 50, 400, 250, "elena.png"), 
        Characters("Evelyn", 1000, 50, 650, 100, "evelyn.png")
    ]

    enemy = Characters("boss", 6000, 0, 150, 50, "boss.png", is_enemy=True)
    active_hero_index = 0

    is_attacking = False
    attack_timer = 0
    enemy_is_attacking = False
    enemy_attack_timer = 0

    cur_menu = "MAIN BATTLE MENU"
    cur_col, cur_row, sub_row = 0, 0, 0 

    current_options = []
    is_runniung = True
    while is_runniung:
        virtual_screen.fill((30, 30, 30))
        hero = party[active_hero_index]

        virtual_screen.blit(enemy.image, (enemy.x, enemy.y))
        for p in party:
            virtual_screen.blit(p.image, (p.x, p.y))

        draw_individual_menus(virtual_screen, small_font, party, active_hero_index)
        draw_battle_menu(virtual_screen, font, cur_col, cur_row, cur_menu, sub_row, enemy, protect_options, hero, current_options)

        protect_options = [p.name for p in party if p != hero] + ["Back"]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_runniung = False

            if event.type == pygame.VIDEORESIZE:
                display_res = (event.w, event.h)
                window = pygame.display.set_mode(display_res, pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN:
                if cur_menu == "MAIN BATTLE MENU":

                    if event.key == pygame.K_UP:
                        cur_row = (cur_row - 1) % len(battle_menu[cur_col])
                        cursor_sound.play()
                    if event.key == pygame.K_DOWN:
                        cur_row = (cur_row + 1) % len(battle_menu[cur_col])
                        cursor_sound.play()
                    if event.key == pygame.K_RIGHT:
                        cur_col = (cur_col + 1) % 2
                        cursor_sound.play()
                    if event.key == pygame.K_LEFT:
                        cur_col = (cur_col - 1) % 2
                        cursor_sound.play()
                    if event.key == pygame.K_SPACE and not is_attacking and not enemy_is_attacking:
                        confirm_sound.play()
                        if battle_menu[cur_col][cur_row] == "Attack":
                            current_options = get_unique_abilities(hero)
                            cur_menu = "ATTACK SUBMENU"
                        elif battle_menu[cur_col][cur_row] == "Protect Stance":
                            cur_menu = "PROTECT SUBMENU"
                     
                elif cur_menu == "PROTECT SUBMENU":
                    if event.key == pygame.K_UP:
                        sub_row = (sub_row - 1) % len(protect_options)
                        cursor_sound.play()
                    if event.key == pygame.K_DOWN:
                        sub_row = (sub_row + 1) % len(protect_options)
                        cursor_sound.play()
                    if event.key == pygame.K_SPACE and not is_attacking and not enemy_is_attacking:
                        confirm_sound.play()
                        choice = protect_options[sub_row]
                        if choice == "Back":
                                cur_menu = "MAIN BATTLE MENU"
                        else:
                            for p in party:
                                if choice == p.name:
                                    hero.is_protecting_target = p
                                    break
                            active_hero_index = (active_hero_index + 1) % len(party)
                            cur_menu = "MAIN BATTLE MENU"


                elif cur_menu == "ATTACK SUBMENU":
                    if event.key == pygame.K_UP:
                        sub_row = (sub_row - 1) % len(current_options)
                        cursor_sound.play()
                    if event.key == pygame.K_DOWN:
                        sub_row = (sub_row + 1) % len(current_options)
                        cursor_sound.play()
                    if event.key == pygame.K_SPACE and not is_attacking and not enemy_is_attacking:
                        confirm_sound.play()
                        if current_options[sub_row] == "Back":
                            cur_menu = "MAIN BATTLE MENU"
                        else:
                            is_attacking = True
                            attack_timer = 40
                            cur_menu = "MAIN BATTLE MENU"


        if is_attacking:
            if attack_timer > 25: # first phase of the animation
                hero.x -= 20
                hero.y -= 10
            elif attack_timer > 15: # second phase of the animation
                pass
            elif attack_timer > 0:
                hero.x += 20
                hero.y += 10

            attack_timer -= 1 # countdown timer

            if attack_timer == 0:
                is_attacking = False
                hero.x, hero.y = hero.base_x, hero.base_y
                enemy.take_damage(random.randint(100, 150), party )

                enemy_is_attacking = True
                enemy_attack_timer = 40
                
        if enemy_is_attacking:
            if enemy_attack_timer > 25: # first phase of the animation
                enemy.x += 20
                enemy.y += 10
            elif enemy_attack_timer > 15: # second phase of the animation
                pass
            elif enemy_attack_timer > 0:
                enemy.x -= 20
                enemy.y -= 10

            enemy_attack_timer -= 1 # countdown timer

            if enemy_attack_timer == 0:
                enemy_is_attacking = False
                enemy.x, enemy.y = enemy.base_x, enemy.base_y
                target_hero = random.choice(party)
                target_hero.take_damage(random.randint(100,150), party)
                for p in party:
                    p.is_protecting_target = None

                active_hero_index = (active_hero_index + 1) % len(party)

        scaled_surface = pygame.transform.smoothscale(virtual_screen, display_res)
        window.blit(scaled_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

