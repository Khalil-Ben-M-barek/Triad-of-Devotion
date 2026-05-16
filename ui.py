import pygame
import constants
from constants import white, blue, gray, yellow, orange, green, red, menu_rect, battle_menu, DESCRIPTIONS, ENABLER_STATS
from abilities import SYNERGY_MOVES

def draw_individual_menus(virtual_screen, small_font, party, active_hero_index):
    for i, hero in enumerate(party):
        box_width, box_height = 200, 76
        box_x = 580
        box_y = 340 + (i * 78)
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
            
        potential_x, potential_y = box_x + 75, box_y + 55
        potential_is_full = hero.potential_value >= hero.max_potential_value
        potential_color = orange if hero.potential_value >= hero.max_potential_value else white
        potential_fill_width = (hero.potential_value / hero.max_potential_value) * 100
        pygame.draw.rect(virtual_screen, (80, 80, 80), (potential_x, potential_y, 100, 15))
        pygame.draw.rect(virtual_screen, potential_color, (potential_x, potential_y, potential_fill_width, 15))
        pygame.draw.rect(virtual_screen, white, (potential_x, potential_y, 100, 15), 1) # Border
        potential_text = "Potential Breach" if potential_is_full else "Potential"
        virtual_screen.blit(small_font.render(potential_text, True, potential_color), (potential_x, potential_y - 20))

        for lvl in range(3):
            potential_bar_color = yellow if hero.potential_level > lvl else (50, 50, 50)
            pygame.draw.rect(virtual_screen, potential_bar_color, (potential_x + 105 + (lvl * 6), potential_y, 3, 15))

def draw_battle_menu(virtual_screen, font, small_font, col, row, cur_menu, sub_row, enemy, protect_options, hero, attack_options, potential_options, magic_options, synergy_options, party, enemy_turns_remaining, scroll_x):
    current_hover_text = ""

    pygame.draw.rect(virtual_screen, blue, menu_rect)
    pygame.draw.rect(virtual_screen, white, menu_rect, 2)

    pygame.draw.rect(virtual_screen, gray, (enemy.base_x + 50, enemy.base_y - 20, 150, 15)) # HP bar
    pygame.draw.rect(virtual_screen, green, (enemy.base_x + 50, enemy.base_y - 20, (enemy.hp / max(1, enemy.max_hp)) * 150, 15))
    virtual_screen.blit(small_font.render(f"HP: {enemy.hp}/{enemy.max_hp}", True, white), (enemy.base_x + 50, enemy.base_y - 37))
    virtual_screen.blit(small_font.render(f"{enemy.name}", True, red), (enemy.base_x + 110, enemy.base_y -50))
    turn_font = pygame.font.SysFont("Arial", 28, bold=True)
    turn_text = turn_font.render(f"Turns Remaining: {enemy_turns_remaining}", True, red)
    virtual_screen.blit(turn_text, (300, 20))
    current_hover_text = ""
    active_y = menu_rect[1] + 15
    options = []

    if cur_menu == "MAIN BATTLE MENU":
        if row >= len(battle_menu[col]):
            row = len(battle_menu[col]) - 1
            
        current_hover_text = battle_menu[col][row]
        active_y = menu_rect[1] + 15 + (row * 32)
        for c in range(2):
            for r in range(len(battle_menu[c])):
                text = battle_menu[c][r]

                tx = menu_rect[0] + 60 + (c * 200)
                ty = menu_rect[1] + 15 + (r * 32)

                text_color = white
                if text == "Potential Breach" and hero.potential_value < hero.max_potential_value:
                    text_color = gray
                elif text == "Synergy Abilities":
                    for move in SYNERGY_MOVES:
                        if move.heroes[0] == hero.name or move.heroes[1] == hero.name: # Checking for only the current hero's synergy abilities
                            partner_name = move.heroes[0] if move.heroes[1] == hero.name else move.heroes[1]
                            partner = None
                            for p in party:
                                if p.name == partner_name:
                                    partner = p
                                    break
                            if partner and partner.hp > 0 and not partner.is_controlled and hero.synergy_bars >= move.synergy_bars_required and partner.synergy_bars >= move.synergy_bars_required: # Found a valid move
                                text_color = white
                                break
                            else:
                                text_color = gray
                elif text == "Protect Stance" and constants.protect_used_this_turn:
                    text_color = gray
                    
                if c == col and r == row and text_color != gray:
                    text_color = yellow
                
                virtual_screen.blit(font.render(text, True, text_color), (tx, ty))

                if c == col and r == row:
                    pointer_x = (tx - 35)
                    pointer_y = (ty + 10)
                    pygame.draw.polygon(virtual_screen, white, [(pointer_x, pointer_y), (pointer_x + 15, pointer_y + 7), (pointer_x, pointer_y + 14)])

    elif cur_menu in ["ATTACK SUBMENU", "PROTECT SUBMENU", "POTENTIAL SUBMENU", "MAGIC SUBMENU", "SYNERGY SUBMENU", "HEALING TARGET SUBMENU", "MANIPULATE TARGET SUBMENU", "SEIZE TARGET SUBMENU", "REVIVAL TARGET SUBMENU", "TWIN CAST SUBMENU"]:
        if cur_menu == "ATTACK SUBMENU":
            options = attack_options
        elif cur_menu == "PROTECT SUBMENU":
            options = protect_options
        elif cur_menu == "MAGIC SUBMENU":
            options = magic_options
        elif cur_menu == "POTENTIAL SUBMENU":
            options = potential_options
        elif cur_menu == "SYNERGY SUBMENU":
            options = synergy_options
        elif cur_menu == "HEALING TARGET SUBMENU":
            options = [p.name for p in party if 0 < p.hp < p.max_hp and not p.is_controlled] + ["Back"]
        elif cur_menu == "REVIVAL TARGET SUBMENU":
            options = [p.name for p in party if p.hp <= 0] + ["Back"]
        elif cur_menu == "SEIZE TARGET SUBMENU":
            options = [p.name for p in party if p != hero and p.hp > 0 and p.potential_value > 0 and not p.is_controlled] + ["Back"]
        elif cur_menu == "MANIPULATE TARGET SUBMENU":
            options = [p.name for p in party if p.hp > 0 and not p.is_controlled] + ["Back"]
        elif cur_menu == "TWIN CAST SUBMENU":
            options = [p.name for p in party if p.hp > 0 and not p.is_controlled] + ["Back"]
        if sub_row >= len(options):
            sub_row = 0

        current_hover_text = options[sub_row]
        active_y = menu_rect[1] + 15 + (sub_row * 32)
        for i, text in enumerate(options):
            tx = menu_rect[0] + 60
            ty = menu_rect[1] + 15 + (i * 32)
            text_color = white
            if cur_menu == "MAGIC SUBMENU" and text != "Back":
                cost = ENABLER_STATS[text]
                if hero.mp < cost and not hero.zero_mp_cost:
                    text_color = gray

            elif cur_menu == "ATTACK SUBMENU":
                if text == "Counter" and hero.cooldowns["Counter"] > 0:
                    text_color = gray
                if text == "Charge" and (hero.chi_level >= 2 or hero.cooldowns["Charge"] > 0):
                    text_color = gray
                if text == "Twin Cast" and hero.cooldowns["Twin Cast"] > 0:
                    text_color = gray

            elif cur_menu == "SYNERGY SUBMENU" and text != "Back":
                for move in SYNERGY_MOVES:
                    if text == move.name:
                        partner_name = move.heroes[0] if move.heroes[1] == hero.name else move.heroes[1]
                        partner = None
                        for p in party:
                            if p.name == partner_name:
                                partner = p
                                break
                        if not partner or partner.hp <= 0 or hero.synergy_bars < move.synergy_bars_required or partner.synergy_bars < move.synergy_bars_required:
                            text_color = gray

            if i == sub_row and text_color != gray:
                text_color = yellow
            display_name = text
            if cur_menu == "MAGIC SUBMENU" and text != "Back":
                display_name = f"{text} ({ENABLER_STATS[text]} MP)"

            virtual_screen.blit(font.render(display_name, True, text_color), (tx, ty))
            if i == sub_row:
                pygame.draw.polygon(virtual_screen, white, [(tx - 35, ty + 10), (tx - 20, ty + 17), (tx - 35, ty + 24)])

    box_width = 200
    scroll_rect = pygame.Rect(menu_rect[0] + 230, active_y, box_width, 25)
    
    if current_hover_text in DESCRIPTIONS:
        pygame.draw.rect(virtual_screen, blue, scroll_rect)
        pygame.draw.rect(virtual_screen, white, scroll_rect, 1)

        description_text = DESCRIPTIONS[current_hover_text]
        text_surface = font.render(description_text, True, yellow)

        clip_surface = pygame.Surface((box_width - 10, 21))
        clip_surface.fill(blue)
        clip_surface.blit(text_surface, (scroll_x, 0))
        virtual_screen.blit(clip_surface, (scroll_rect.x + 5, scroll_rect.y + 2))

        scroll_x -= 2 # Scroll speed
        if (scroll_x + text_surface.get_width()) < 0:
            scroll_x = box_width
    return scroll_x