import pygame
import random
import constants
from characters import Characters
from constants import white, blue, gray, yellow, orange, green, red, BLOCK_KEYS, ENABLER_STATS, protect_used_this_turn, battle_menu
from abilities import SYNERGY_MOVES, get_potential_options, get_unique_abilities
from ui import draw_individual_menus, draw_battle_menu
from setup_menu import run_setup_menu

def reset_battle(party, enemy):
    for hero in party:
        hero.hp = hero.max_hp
        hero.mp = hero.max_mp
        hero.potential_value = 0
        hero.potential_level = 1
        hero.synergy_bars = 0
        hero.zero_mp_cost = False
        hero.chi_level = 0
        hero.is_protecting_target = None
        hero.is_counter_active = False
        hero.is_twin_cast_active = False
        hero.cooldowns = {"Counter": 0, "Twin Cast": 0, "Charge": 0}

    enemy.hp = enemy.max_hp
    enemy.forced_target = None
    constants.protect_used_this_turn = False

def run_battle(virtual_screen, window, display_res, font, small_font, clock, cursor_sound, confirm_sound):
    party = [
        Characters("Evelyn", 1000, 50, 550, 100, "assets/images/evelyn.png", "assets/images/evelyn_portrait.png", "assets/images/evelyn_controlled.png", "assets/images/fainted_evelyn.png"),
        Characters("Ethan", 1000, 50, 450, 150, "assets/images/ethan.png", "assets/images/ethan_portrait.png", "assets/images/ethan_controlled.png", "assets/images/fainted_ethan.png"), 
        Characters("Elena", 1000, 50, 400, 250, "assets/images/elena.png", "assets/images/elena_portrait.png", "assets/images/elena_controlled.png", "assets/images/fainted_elena.png")
    ]

    turn_order = list(party)
    default_turn_order = list(party)
    enemy = Characters("Void", 10000, 0, 70, 50, image_path="assets/images/void.png", is_enemy=True)
    active_hero_index = 0
    target_hero = None

    is_attacking = False
    attack_timer = 0
    enemy_is_attacking = False
    enemy_attack_timer = 0
    enemy_turn_count = 0
    MAX_ENEMY_TURNS = 80
    enemy_turns_remaining = MAX_ENEMY_TURNS

    cur_menu = "MAIN BATTLE MENU"
    cur_col, cur_row, sub_row = 0, 0, 0
    synergy_options = []
    attack_options = []
    protect_options = []
    synergy_partner = None
    scroll_x = 440

    pygame.mixer.init()
    try:
        cursor_sound = pygame.mixer.Sound("assets/audio/cursor.wav")
    except:
        cursor_sound = None
    try:
        confirm_sound = pygame.mixer.Sound("assets/audio/confirm.wav")
    except:
        confirm_sound = None

    display_res = run_setup_menu(virtual_screen, window, display_res, font, small_font, party, cursor_sound, confirm_sound, turn_order)
    party[:] = turn_order
    try:
        music = pygame.mixer.Sound("assets/audio/collision_of_destinies.mp3")
        music.play(-1)
    except:
        music = None

    is_running = True
    while is_running:
        virtual_screen.fill((30, 30, 30))

        if enemy.hp <= 0:
            print("Enemy turns before reset:", enemy_turn_count)
            enemy_turn_count = 0
            enemy_turns_remaining = MAX_ENEMY_TURNS
            if music:
                music.stop()
            pygame.time.delay(1000)
            turn_order[:] = default_turn_order
            display_res = run_setup_menu(virtual_screen, window, display_res, font, small_font, party, cursor_sound, confirm_sound, turn_order)
            reset_battle(party, enemy)
            if music:
                music.play(-1)
            active_hero_index = 0
            cur_menu = "MAIN BATTLE MENU"
            cur_col, cur_row, sub_row = 0, 0, 0
            continue
        
        if all(hero.hp <= 0 for hero in party):
            enemy_turn_count = 0
            enemy_turns_remaining = MAX_ENEMY_TURNS
            if music:
                music.stop()
            pygame.time.delay(1000)
            turn_order[:] = default_turn_order
            display_res = run_setup_menu(virtual_screen, window, display_res, font, small_font, party, cursor_sound, confirm_sound, turn_order)
            reset_battle(party, enemy)
            if music:
                music.play(-1)
            active_hero_index = 0
            cur_menu = "MAIN BATTLE MENU"
            cur_col, cur_row, sub_row = 0, 0, 0
            continue

        controlled_hero = None
        for p in party:
            if p.is_controlled:
                controlled_hero = p
                break

        living_uncontrolled_heroes = [p for p in party if p.hp > 0 and not p.is_controlled]
        if controlled_hero and len(living_uncontrolled_heroes) == 0:
            controlled_hero.is_controlled = False
            controlled_hero.image = controlled_hero.original_image
            controlled_hero.x, controlled_hero.y = controlled_hero.base_x, controlled_hero.base_y
            controlled_hero = None
        if party[active_hero_index].hp <= 0 or party[active_hero_index].is_controlled:
            if active_hero_index == 0 and constants.protect_used_this_turn  and not is_attacking and not enemy_is_attacking:
                constants.protect_used_this_turn = False
                for p in party:
                    p.is_protecting_target = None

            active_hero_index = (active_hero_index + 1) % len(party)
            continue

        hero = party[active_hero_index]
        current_attacker = controlled_hero if controlled_hero else enemy
        virtual_screen.blit(enemy.image, (enemy.x, enemy.y))
        for p in default_turn_order:
            if p.hp <= 0:
                virtual_screen.blit(p.fainted_image, (p.x, p.y))
            else:
                virtual_screen.blit(p.image, (p.x, p.y))

        potential_options = get_potential_options(hero)
        magic_options = hero.enabler + ["Back"]
        protect_options = [p.name for p in party if p != hero and p.hp > 0 and not p.is_controlled] + ["Back"]

        draw_individual_menus(virtual_screen, small_font, party, active_hero_index)
        scroll_x = draw_battle_menu(virtual_screen, font, small_font, cur_col, cur_row, cur_menu, sub_row, enemy, protect_options, hero, attack_options, potential_options, magic_options, synergy_options, party, enemy_turns_remaining, scroll_x)

        if active_hero_index == 0 and not is_attacking and not enemy_is_attacking:
            if constants.protect_used_this_turn :
                constants.protect_used_this_turn = False
                for p in party:
                    p.is_protecting_target = None

        if party[active_hero_index].hp <= 0:
            active_hero_index = (active_hero_index + 1) % len(party)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.VIDEORESIZE:
                display_res = (event.w, event.h)
                window = pygame.display.set_mode(display_res, pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN:
                scroll_x = 200 # To reset scroll when any key is pressed

                if 15 < enemy_attack_timer < 25 and enemy_is_attacking:
                    key_pressed = pygame.key.name(event.key).lower()
                    expected_key = BLOCK_KEYS[target_hero.name]
                    if not current_attacker.failed_block_attempt and not current_attacker.last_attack_blocked:
                        if key_pressed == expected_key:
                            current_attacker.last_attack_blocked = True
                            enemy.last_attack_blocked = True
                            if confirm_sound:
                                confirm_sound.play()
                            if controlled_hero:
                                controlled_hero.is_controlled = False
                                controlled_hero.image = controlled_hero.original_image
                                controlled_hero.x, controlled_hero.y = controlled_hero.base_x, controlled_hero.base_y
                                for i, hero in enumerate(party):
                                    if hero == controlled_hero: 
                                        active_hero_index = i
                                        break
                                controlled_hero = None
                            cur_menu = "MAIN BATTLE MENU"
                            cur_col, cur_row, sub_row = 0, 0, 0
                        else:
                            current_attacker.failed_block_attempt= True

                if cur_menu == "MAIN BATTLE MENU":
                    if cur_col >= len(battle_menu):
                        cur_col = len(battle_menu) - 1
                    if cur_row >= len(battle_menu[cur_col]):
                        cur_row = len(battle_menu[cur_col]) - 1
                    if event.key == pygame.K_UP:
                        cur_row = (cur_row - 1) % len(battle_menu[cur_col])
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_DOWN:
                        cur_row = (cur_row + 1) % len(battle_menu[cur_col])
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_RIGHT:
                        cur_col = (cur_col + 1) % 2
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_LEFT:
                        cur_col = (cur_col - 1) % 2
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_SPACE and not is_attacking and not enemy_is_attacking:
                        if confirm_sound:
                            confirm_sound.play()
                        sub_row = 0 
                        scroll_x = 200
                        if battle_menu[cur_col][cur_row] == "Attack":
                            attack_options = get_unique_abilities(hero)
                            cur_menu = "ATTACK SUBMENU"
                        elif battle_menu[cur_col][cur_row] == "Magic":
                            cur_menu = "MAGIC SUBMENU"
                            sub_row = 0
                        elif battle_menu[cur_col][cur_row] == "Protect Stance":
                            if not constants.protect_used_this_turn :
                                cur_menu = "PROTECT SUBMENU"
                        elif battle_menu[cur_col][cur_row] == "Potential Breach":
                            if hero.potential_value >= hero.max_potential_value:
                                cur_menu = "POTENTIAL SUBMENU"
                        elif battle_menu[cur_col][cur_row] == "Synergy Abilities":
                            # If any move is available/satisfies the conditions
                            if any(m for m in SYNERGY_MOVES if hero.name in m.heroes and all(p.synergy_bars >= m.synergy_bars_required and not p.is_controlled for p in party if p.name in m.heroes)):
                                synergy_options = [move.name for move in SYNERGY_MOVES if hero.name in move.heroes]
                                synergy_options.append("Back")
                                cur_menu = "SYNERGY SUBMENU"
                                sub_row = 0

                elif cur_menu == "SYNERGY SUBMENU":
                    if event.key == pygame.K_UP:
                        sub_row = (sub_row - 1) % len(synergy_options)
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_DOWN:
                        sub_row = (sub_row + 1) % len(synergy_options)
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_SPACE:
                        if confirm_sound:
                            confirm_sound.play()
                        move_name = synergy_options[sub_row]
                        if move_name == "Back":
                            cur_menu = "MAIN BATTLE MENU"
                            cur_col, cur_row, sub_row = 0, 0, 0
                        else:
                            selected_move = None
                            for move in SYNERGY_MOVES:
                                if move.name == move_name:
                                    selected_move = move
                                    break

                            partner_name = selected_move.heroes[0] if selected_move.heroes[1] == hero.name else selected_move.heroes[1]
                            partner = None
                            for p in party:
                                if p.name == partner_name:
                                    partner = p
                                    break

                            if(partner and hero.synergy_bars >= selected_move.synergy_bars_required and partner.synergy_bars >= selected_move.synergy_bars_required):
                                hero.synergy_bars -= selected_move.synergy_bars_required
                                partner.synergy_bars -= selected_move.synergy_bars_required
                                enemy.take_damage(selected_move.damage, party)

                                for p in [hero, partner]:   
                                    if selected_move.perk_type in ["POTENTIAL_LEVEL_UP", "BOTH"]:
                                        p.potential_level = min(3, p.potential_level + 1)
                                    if selected_move.perk_type in ["ZERO_MP_COST", "BOTH"]:
                                        p.zero_mp_cost = True
                                
                                is_attacking = True
                                attack_timer = 40
                                cur_menu = "MAIN BATTLE MENU"
                                synergy_partner = partner
                                cur_col, cur_row, sub_row = 0, 0, 0

                elif cur_menu == "POTENTIAL SUBMENU":
                    if event.key == pygame.K_UP:
                        sub_row = (sub_row - 1) % len(potential_options)
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_DOWN:
                        sub_row = (sub_row + 1) % len(potential_options)
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_SPACE:
                        if confirm_sound:
                            confirm_sound.play()
                        if potential_options[sub_row] == "Back":
                            cur_menu = "MAIN BATTLE MENU"
                            cur_col, cur_row, sub_row = 0, 0, 0
                        else:
                            current_potential_move = potential_options[sub_row]
                            hero.potential_value = 0
                            hero.potential_level = max(1, hero.potential_level - 1)

                            if current_potential_move == "Soothing Gale":
                                for p in party:
                                    if p.hp > 0 and not p.is_controlled:
                                        p.heal(500)
                                enemy_is_attacking = True
                                enemy_attack_timer = 40
                                cur_menu = "MAIN BATTLE MENU"
                                cur_col, cur_row, sub_row = 0, 0, 0
                            
                            elif current_potential_move == "Potential Impart":
                                for p in party: 
                                    if p != hero and not p.is_controlled and p.hp > 0:
                                        p.potential_value = p.max_potential_value
                                enemy_is_attacking = True
                                enemy_attack_timer = 40
                                cur_menu = "MAIN BATTLE MENU"
                                cur_col, cur_row, sub_row = 0, 0, 0

                            elif current_potential_move == "Full Restore":
                                for p in party:
                                    if p.hp > 0 and not p.is_controlled:
                                        p.hp = p.max_hp
                                        p.mp = p.max_mp

                                enemy_is_attacking = True
                                enemy_attack_timer = 40
                                cur_menu = "MAIN BATTLE MENU"
                                cur_col, cur_row, sub_row = 0, 0, 0

                            else:
                                is_attacking = True
                                attack_timer = 40
                                
                                if current_potential_move == "Flurry Slash":
                                    enemy.take_damage(350, party)
                                elif current_potential_move == "Heavenly Descent":
                                    enemy.take_damage(800, party)
                                elif current_potential_move == "Final Blow":
                                    enemy.take_damage(1800, party)
                                
                                elif current_potential_move == "Spinning Kick":
                                    enemy.take_damage(350, party)
                                elif current_potential_move == "Tidal Onslaught":
                                    enemy.take_damage(800, party)
                                elif current_potential_move == "Celestial Tempest":
                                    enemy.take_damage(1800, party)
                                
                                cur_menu = "MAIN BATTLE MENU"
                                cur_col, cur_row, sub_row = 0, 0, 0

                elif cur_menu == "PROTECT SUBMENU":
                    if event.key == pygame.K_UP:
                        sub_row = (sub_row - 1) % len(protect_options)
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_DOWN:
                        sub_row = (sub_row + 1) % len(protect_options)
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_SPACE and not is_attacking and not enemy_is_attacking:
                        if confirm_sound:
                            confirm_sound.play()
                        choice = protect_options[sub_row]
                        if choice == "Back":
                                cur_menu = "MAIN BATTLE MENU"
                                cur_col, cur_row, sub_row = 0, 0, 0
                        else:
                            for p in party:
                                if choice == p.name:
                                    hero.is_protecting_target = p
                                    constants.protect_used_this_turn = True
                                    break
                            enemy_is_attacking = True
                            enemy_attack_timer = 40
                            cur_menu = "MAIN BATTLE MENU"
                            cur_col, cur_row, sub_row = 0, 0, 0


                elif cur_menu == "ATTACK SUBMENU":
                    if event.key == pygame.K_UP:
                        sub_row = (sub_row - 1) % len(attack_options)
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_DOWN:
                        sub_row = (sub_row + 1) % len(attack_options)
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_SPACE and not is_attacking and not enemy_is_attacking:
                        if confirm_sound:
                            confirm_sound.play()
                        if attack_options[sub_row] == "Back":
                            cur_menu = "MAIN BATTLE MENU"
                            cur_col, cur_row, sub_row = 0, 0, 0

                        elif attack_options[sub_row] == "Basic Attack":
                            enemy.take_damage(random.randint(50, 100), party)
                            is_attacking = True
                            attack_timer = 40
                            cur_menu = "MAIN BATTLE MENU"
                            cur_col, cur_row, sub_row = 0, 0, 0

                        elif attack_options[sub_row] == "Counter":
                            if hero.cooldowns["Counter"] <= 0:
                                hero.cooldowns["Counter"] = 4
                                hero.is_counter_active = True
                                enemy_is_attacking = True
                                enemy_attack_timer = 40
                                cur_menu = "MAIN BATTLE MENU"
                                cur_col, cur_row, sub_row = 0, 0, 0

                        elif attack_options[sub_row] == "Charge":
                            if hero.chi_level > 2 or hero.cooldowns["Charge"] <= 0:
                                hero.chi_level += 1
                                hero.cooldowns["Charge"] = 2
                                enemy_is_attacking = True
                                enemy_attack_timer = 40
                                cur_menu = "MAIN BATTLE MENU"
                                cur_col, cur_row, sub_row = 0, 0, 0
                        elif attack_options[sub_row] == "Brute Force":
                            enemy.take_damage(random.randint(150, 200), party)
                            hero.chi_level -= 1
                            is_attacking = True
                            attack_timer = 40
                            cur_menu = "MAIN BATTLE MENU"
                            cur_col, cur_row, sub_row = 0, 0, 0
                        elif attack_options[sub_row] == "Heavy Barrage":
                            enemy.take_damage(random.randint(350, 400), party)
                            hero.chi_level -= 1
                            is_attacking = True
                            attack_timer = 40
                            cur_menu = "MAIN BATTLE MENU"
                            cur_col, cur_row, sub_row = 0, 0, 0

                        elif attack_options[sub_row] == "Twin Cast":
                            if hero.cooldowns["Twin Cast"] <= 0:
                                cur_menu = "TWIN CAST SUBMENU"
                                sub_row = 0

                elif cur_menu == "TWIN CAST SUBMENU":
                    alive_allies = [p for p in party if p.hp > 0 and not p.is_controlled]
                    target_options = [p.name for p in alive_allies] + ["Back"]
                    if event.key == pygame.K_UP:
                        sub_row = (sub_row - 1) % len(target_options)
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_DOWN:
                        sub_row = (sub_row + 1) % len(target_options)
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_SPACE:
                        if confirm_sound:
                            confirm_sound.play()
                        if sub_row >= len(target_options):
                            sub_row = 0
                        choice = target_options[sub_row]
                        if choice == "Back":
                            cur_menu = "ATTACK SUBMENU"
                            sub_row = 0
                        else:
                            target = None
                            for p in alive_allies:
                                if p.name == choice:
                                    target = p
                                    break
                            if target is not None:
                                target.is_twin_cast_active = True
                                hero.cooldowns["Twin Cast"] = 4
                                cur_menu = "MAIN BATTLE MENU"
                                cur_col, cur_row, sub_row = 0, 0, 0
                                enemy_is_attacking = True
                                enemy_attack_timer = 40

                elif cur_menu == "MAGIC SUBMENU":
                    if event.key == pygame.K_UP:
                        sub_row = (sub_row - 1) % len(magic_options)
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_DOWN:
                        sub_row = (sub_row + 1) % len(magic_options)
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_SPACE:
                        spell = magic_options[sub_row]
                        if confirm_sound:
                            confirm_sound.play()
                        if spell == "Back":
                            cur_menu = "MAIN BATTLE MENU"
                            cur_col, cur_row, sub_row = 0, 0, 0
                        elif hero.mp >= ENABLER_STATS[spell] or hero.zero_mp_cost:
                            if spell == "Potential Seize":
                                cur_menu = "SEIZE TARGET SUBMENU"
                            elif spell == "Healing":
                                cur_menu = "HEALING TARGET SUBMENU"
                            elif spell == "Revive" or spell == "Rebirth":
                                cur_menu = "REVIVAL TARGET SUBMENU"
                            elif spell == "Manipulate":
                                cur_menu = "MANIPULATE TARGET SUBMENU"
                            elif spell == "Strike":
                                enemy.take_damage(600, party)
                                if hero.is_twin_cast_active:
                                    enemy.take_damage(300, party)
                                    hero.is_twin_cast_active = False
                                if not hero.zero_mp_cost:
                                    hero.mp -= ENABLER_STATS["Strike"]
                                hero.zero_mp_cost = False
                                cur_menu = "MAIN BATTLE MENU"
                                cur_col, cur_row, sub_row = 0, 0, 0
                                enemy_is_attacking = True
                                enemy_attack_timer = 40

                elif cur_menu == "HEALING TARGET SUBMENU":
                    alive_allies = [p for p in party if p.hp > 0 and not p.is_controlled]
                    target_options = [p.name for p in alive_allies] + ["Back"]
                    if event.key == pygame.K_UP:
                        sub_row = (sub_row - 1) % len(target_options)
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_DOWN:
                        sub_row = (sub_row + 1) % len(target_options)
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_SPACE:
                        if confirm_sound:
                            confirm_sound.play()
                        if sub_row >= len(target_options):
                            sub_row = 0
                        choice = target_options[sub_row]
                        if choice == "Back":
                            cur_menu = "MAGIC SUBMENU"
                            sub_row = 0
                        else:
                            target = None
                            for p in alive_allies:
                                if p.name == choice:
                                    target = p
                                    break
                            if target is not None:
                                target.heal(random.randint(400, 600))
                                hero.mp -= 0 if hero.zero_mp_cost else ENABLER_STATS["Healing"]
                                hero.zero_mp_cost = False
                                cur_menu = "MAIN BATTLE MENU"
                                cur_col, cur_row, sub_row = 0, 0, 0
                                enemy_is_attacking = True
                                enemy_attack_timer = 40

                elif cur_menu == "REVIVAL TARGET SUBMENU":
                    dead_allies = [p for p in party if p.hp <= 0]
                    target_options = [p.name for p in dead_allies] + ["Back"]
                    if event.key == pygame.K_UP:
                        sub_row = (sub_row - 1) % len(target_options)
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_DOWN:
                        sub_row = (sub_row + 1) % len(target_options)
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_SPACE:
                        if confirm_sound:
                            confirm_sound.play()
                        if sub_row >= len(target_options):
                            sub_row = 0
                        choice = target_options[sub_row]
                        if choice == "Back":
                            cur_menu = "MAGIC SUBMENU"
                            sub_row = 0
                        else:
                            for p in dead_allies:
                                if p.name == choice:
                                    target = p
                                    break
                            if target is not None:
                                if spell == "Revive":
                                    target.hp = int(target.max_hp * 0.3)
                                elif spell == "Rebirth":
                                    target.hp = target.max_hp
                                if not hero.zero_mp_cost:
                                    if spell == "Revive":
                                        hero.mp -=  ENABLER_STATS["Revive"]
                                    elif spell == "Rebirth":
                                        hero.mp -=  ENABLER_STATS["Rebirth"]
                                hero.zero_mp_cost = False
                                cur_menu = "MAIN BATTLE MENU"
                                cur_col, cur_row, sub_row = 0, 0, 0
                                enemy_is_attacking = True
                                enemy_attack_timer = 40

                elif cur_menu == "MANIPULATE TARGET SUBMENU":
                    alive_allies = [p for p in party if p.hp > 0 and not p.is_controlled]
                    target_options = [p.name for p in alive_allies] + ["Back"]
                    if event.key == pygame.K_UP:
                        sub_row = (sub_row - 1) % len(target_options)
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_DOWN:
                        sub_row = (sub_row + 1) % len(target_options)
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_SPACE:
                        if confirm_sound:
                            confirm_sound.play()
                        if sub_row >= len(target_options):
                            sub_row = 0
                        choice = target_options[sub_row]
                        if choice == "Back":
                            cur_menu = "MAGIC SUBMENU"
                            sub_row = 0
                        else:
                            target = None
                            for p in alive_allies:
                                if p.name == choice:
                                    target = p
                                    break
                            if target is not None:
                                enemy.forced_target = target
                                if not hero.zero_mp_cost:
                                    hero.mp -= ENABLER_STATS["Manipulate"]
                                hero.zero_mp_cost = False
                                cur_menu = "MAIN BATTLE MENU"
                                cur_col, cur_row, sub_row = 0, 0, 0
                                enemy_is_attacking = True
                                enemy_attack_timer = 40


                elif cur_menu == "SEIZE TARGET SUBMENU":
                    seize_targets = [p for p in party if p != hero and p.potential_value > 0]
                    target_options = [p.name for p in seize_targets] + ["Back"]
                    if event.key == pygame.K_UP:
                        sub_row = (sub_row - 1) % len(target_options)
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_DOWN:
                        sub_row = (sub_row + 1) % len(target_options)
                        if cursor_sound:
                            cursor_sound.play()
                    elif event.key == pygame.K_SPACE:
                        if confirm_sound:
                            confirm_sound.play()
                        if sub_row >= len(target_options):
                            sub_row = 0
                        choice = target_options[sub_row]
                        if target_options[sub_row] == "Back":
                            cur_menu = "MAGIC SUBMENU"
                            sub_row = 0
                        else:
                            target = None
                            for p in seize_targets:
                                if p.name == choice:
                                    target = p
                                    break
                            if target is not None:
                                hero.potential_value = min(hero.max_potential_value, hero.potential_value + target.potential_value)
                                target.potential_value = 0
                                if not hero.zero_mp_cost:
                                    hero.mp -= ENABLER_STATS["Potential Seize"]
                                hero.zero_mp_cost = False
                                cur_menu = "MAIN BATTLE MENU"
                                cur_col, cur_row, sub_row = 0, 0, 0
                                enemy_is_attacking = True
                                enemy_attack_timer = 40

                            
        if is_attacking:
            if attack_timer > 25: # First phase of the animation
                hero.x += (enemy.base_x - hero.base_x) // 15
                hero.y += (enemy.base_y - hero.base_y) // 15
                if synergy_partner:
                    synergy_partner.x += (enemy.base_x - synergy_partner.base_x) // 15
                    synergy_partner.y += (enemy.base_y - synergy_partner.base_y) // 15
            elif attack_timer > 15: # Second phase of the animation
                pass
            elif attack_timer > 0:
                hero.x -= (enemy.base_x - hero.base_x) // 15
                hero.y -= (enemy.base_y - hero.base_y) // 15
                if synergy_partner:
                    synergy_partner.x -= (enemy.base_x - synergy_partner.base_x) // 15
                    synergy_partner.y -= (enemy.base_y - synergy_partner.base_y) // 15

            attack_timer -= 1 # Countdown timer

            if attack_timer == 0:
                is_attacking = False
                hero.x, hero.y = hero.base_x, hero.base_y
                if synergy_partner:
                    synergy_partner.x, synergy_partner.y = synergy_partner.base_x, synergy_partner.base_y
                    synergy_partner = None
                enemy_is_attacking = True
                enemy_attack_timer = 40
                
        if enemy_is_attacking:
            if enemy_attack_timer == 40:
                current_attacker.last_attack_blocked = False
                current_attacker.failed_block_attempt = False
                if not controlled_hero and len(living_uncontrolled_heroes) > 1 and random.randint(1, 10) == 1:
                    target = random.choice(living_uncontrolled_heroes)
                    target.is_controlled = True
                    target.is_protecting_target = None
                    target.original_image = target.image
                    target.image = target.controlled_image
                    target.x, target.y = enemy.x + 180, enemy.y + 50

                    for p in party:
                        if p.is_protecting_target == target:
                            p.is_protecting_target = None

                    enemy_is_attacking = False
                    enemy_attack_timer = 0
                    enemy_turn_count += 1
                    enemy_turns_remaining -= 1
                    active_hero_index = (active_hero_index + 1) % len(party)
                    if party[active_hero_index].hp <= 0 or party[active_hero_index].is_controlled:
                        active_hero_index = (active_hero_index + 1) % len(party)
                    cur_menu = "MAIN BATTLE MENU"
                    cur_col, cur_row, sub_row = 0, 0, 0
                    continue

                if living_uncontrolled_heroes:
                    if enemy.forced_target and enemy.forced_target.hp > 0 and not enemy.forced_target.is_controlled:
                        target_hero = enemy.forced_target
                        enemy.forced_target = None
                    else:
                        target_hero = random.choice(living_uncontrolled_heroes)

            protector = None
            for p in party:
                if p.is_protecting_target == target_hero and p.hp > 0:
                    protector = p
                    break

            if enemy_attack_timer > 25: # First phase of the animation
                if controlled_hero:
                    current_attacker.x += (target_hero.base_x - enemy.x - 120) // 15
                    current_attacker.y += (target_hero.base_y - enemy.y + 15) // 15
                else:
                    current_attacker.x += (target_hero.base_x - current_attacker.base_x) // 15
                    current_attacker.y += (target_hero.base_y - current_attacker.base_y) // 15
                if protector:
                    protector.x += (target_hero.base_x - protector.base_x - 40) // 10
                    protector.y += (target_hero.base_y - protector.base_y - 40) // 10
            elif enemy_attack_timer > 15: # Second phase of the animation
                icon_font = pygame.font.SysFont("Arial", 40, bold=True)
                expected_key_display = BLOCK_KEYS[target_hero.name].upper()
                icon_surf = icon_font.render(f"! {expected_key_display}", True, red)
                virtual_screen.blit(icon_surf, (target_hero.x + 120, target_hero.y + 20))
            elif enemy_attack_timer > 0:
                if controlled_hero:
                    current_attacker.x -= (target_hero.base_x - enemy.x - 120) // 15
                    current_attacker.y -= (target_hero.base_y - enemy.y + 15) // 15
                else:
                    current_attacker.x -= (target_hero.base_x - current_attacker.base_x) // 15
                    current_attacker.y -= (target_hero.base_y - current_attacker.base_y) // 15
                if protector:
                    protector.x -= (target_hero.base_x - protector.base_x - 40) // 10
                    protector.y -= (target_hero.base_y - protector.base_y - 40) // 10

            enemy_attack_timer -= 1

            if enemy_attack_timer == 0:
                enemy_is_attacking = False
                if protector:
                    protector.x, protector.y = protector.base_x, protector.base_y
                target_hero.take_damage(random.randint(100,150), party, attacker=current_attacker)
                if controlled_hero:
                    controlled_hero.x, controlled_hero.y = enemy.x + 180, enemy.y + 50
                else:
                    enemy.x, enemy.y = enemy.base_x, enemy.base_y
                enemy_turn_count += 1
                enemy_turns_remaining -= 1
                if enemy_turns_remaining <= 0:
                    for p in party:
                        p.hp = 0
                active_hero_index = (active_hero_index + 1) % len(party)
                for move_key in hero.cooldowns:
                    if hero.cooldowns[move_key] > 0:
                        hero.cooldowns[move_key] -= 1

        scaled_surface = pygame.transform.smoothscale(virtual_screen, display_res)
        window.blit(scaled_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)