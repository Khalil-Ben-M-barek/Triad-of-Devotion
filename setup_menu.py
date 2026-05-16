import pygame
from constants import white, gray, yellow, orange, green, blue, ENABLER_STATS, DESCRIPTIONS, BLOCK_KEYS
import sys

def run_setup_menu(virtual_screen, window, display_res, font, small_font, party, cursor_sound, confirm_sound, turn_order):
    is_equipping = True
    available_enabler = list(ENABLER_STATS.keys())
    hero_index = 0
    cursor_index = 0
    MAX_ENABLER_SLOTS = 2
    equipped_x, equipped_y = 200, 120
    slot_x, slot_y = 140, 160
    slot_w, slot_h = 110, 240
    list_x, list_y = 10, 410
    line_h = 28
    visible_count = 10
    desc_x, desc_y, desc_w, desc_h = 500, 440, 340, 120
    turn_cursor = 0
    active_panel = "ENABLER"  # Or "TURN ORDER"
    turn_first_selected = -1

    while is_equipping:
        virtual_screen.fill((0, 0, 50))
        hero = party[hero_index]
        title_text = font.render("SETUP MENU", True, yellow)
        instructions = small_font.render("LEFT/RIGHT: Change Hero | UP/DOWN: Navigate | SPACE: Select/Swap | TAB: Switch Panel | ENTER: Start Battle", True, white)
        virtual_screen.blit(title_text, (20, 20))
        virtual_screen.blit(instructions, (20, 50))
        hero_text = font.render(f"Hero: < {hero.name} >", True, (0, 255, 255))
        virtual_screen.blit(hero_text, (20, 100))
        virtual_screen.blit(hero.portrait_image, (240, 200))

        pygame.draw.rect(virtual_screen, (22 , 22, 40), (10, 140, 260, 90))
        pygame.draw.rect(virtual_screen, (180, 180, 180), (10, 140, 260, 90), 1)
        virtual_screen.blit(small_font.render("Equipped Enablers:", True, orange), (slot_x - 50, slot_y - 15))
        pygame.draw.line(virtual_screen, (180, 180, 180), (slot_x - 130, slot_y + 8), (slot_x + 128, slot_y + 8), 1)

        pygame.draw.rect(virtual_screen, (22,22,40), (8, 375, 281, 172))
        pygame.draw.rect(virtual_screen, (180, 180, 180), (8, 375, 281, 206), 1)
        virtual_screen.blit(small_font.render("Available Enablers:", True, orange), (slot_x - 50, slot_y + 220))
        virtual_screen.blit(small_font.render("MP:", True, orange), (slot_x + 117, slot_y + 220))
        pygame.draw.line(virtual_screen, (180, 180, 180), (slot_x - 131, slot_y + 249), (slot_x + 148, slot_y + 249), 1)

        for i in range(MAX_ENABLER_SLOTS):
            y = slot_y + (i * 30)
            text = hero.enabler[i] if i < len(hero.enabler) else "Empty"
            virtual_screen.blit(small_font.render(f"{i+1}. {text}", True, (220, 220, 220)), (slot_x - 50, y + 13))

        if len(available_enabler) == 0:
            cursor_index = 0
        else:
            cursor_index = max(0, min(cursor_index, len(available_enabler)-1))
        top_index = max(0, min(cursor_index - visible_count//2, max(0, len(available_enabler)-visible_count)))

        for index in range(top_index, min(len(available_enabler), top_index + visible_count)):
            enabler = available_enabler[index]
            y = list_y + (index - top_index) * line_h
            is_cursor = (index == cursor_index and active_panel == "ENABLER")

            owner = None
            for p in party:
                if enabler in p.enabler:
                    owner = p
            
            if owner is None:
                color = white
                status_text = "(Available)"
            elif owner == hero:
                color = (100, 255, 140)  # Equipped by this hero
                status_text = "(Equipped)"
            else:
                color = (160,160,160)  # Equipped by another hero
                status_text = f"(In use: {owner.name})"

            bg = (22,22,40) if not is_cursor else (40,40,80) # Most of the menu color
            pygame.draw.rect(virtual_screen, bg, (list_x, y, 278, line_h))
            info = ENABLER_STATS[enabler]
            name_text = small_font.render(enabler, True, color)
            info_text = small_font.render(f"{info}", True, white)
            virtual_screen.blit(name_text, (list_x + 8, y + 4))
            virtual_screen.blit(info_text, (list_x + 250, y + 4))
            if is_cursor:
                pygame.draw.polygon(virtual_screen, white, [(list_x - 15, y + 6), (list_x - 5, y + 14), (list_x - 15, y + 22)])
           
            eq_text = small_font.render(status_text, True, green)
            virtual_screen.blit(eq_text, (list_x + 150, y + 4))
        
        pygame.draw.rect(virtual_screen, (22,22,40), (desc_x, desc_y - 20, desc_w - 50, desc_h + 50))
        pygame.draw.rect(virtual_screen, (200,200,200), (desc_x, desc_y - 20, desc_w - 50, desc_h + 50), 1)

        if available_enabler:
            current_enabler = available_enabler[cursor_index]

            block_box_x, block_box_y = 500, 120
            block_box_w, block_box_h = 290, 220
            pygame.draw.rect(virtual_screen, (22, 22, 40), (block_box_x, block_box_y, block_box_w, block_box_h))
            pygame.draw.rect(virtual_screen, (0, 180, 200), (block_box_x, block_box_y, block_box_w, block_box_h), 2)

            header = font.render("BLOCK COMMANDS", True, yellow)
            virtual_screen.blit(header, (block_box_x + 10, block_box_y + 10))
            pygame.draw.line(virtual_screen, (0, 180, 200), (block_box_x + 10, block_box_y + 34), (block_box_x + block_box_w - 10, block_box_y + 34), 1)
            block_lines = [("When the enemy attacks, press the", white), ("corresponding key to block:", white), ("", white)]

            for hero_name, key in BLOCK_KEYS.items():
                block_lines.append((f"  {hero_name}: [ {key.upper()} ]", (0, 255, 200)))

            block_lines += [("", white), ("Blocking also frees an ally under enemy control.", (255, 200, 80))]

            for i, (line, color) in enumerate(block_lines):
                virtual_screen.blit(small_font.render(line, True, color), (block_box_x + 10, block_box_y + 44 + i * 20))

            desc = DESCRIPTIONS[current_enabler]
            words = desc.split()
            lines = []
            cur_line = ""
            max_chars_per_line = 42
            for w in words:
                if len(cur_line) + len(w) + 1 <= max_chars_per_line:
                    cur_line = (cur_line + " " + w).strip()
                else:
                    lines.append(cur_line)
                    cur_line = w
            if cur_line:
                lines.append(cur_line)
            virtual_screen.blit(small_font.render(f"{current_enabler}:", True, white), (desc_x + 8, desc_y + 8))
            for i, ln in enumerate(lines[:6]): # Limit just in case
                virtual_screen.blit(small_font.render(ln, True, (220,220,220)), (desc_x + 8, desc_y + 36 + i*18))

        turn_box_x, turn_box_y = 292, 120
        turn_box_w, turn_box_h = 185, 110
        pygame.draw.rect(virtual_screen, (22, 22, 40), (turn_box_x, turn_box_y, turn_box_w, turn_box_h))
        pygame.draw.rect(virtual_screen, (180, 100, 255), (turn_box_x, turn_box_y, turn_box_w, turn_box_h), 2)
        virtual_screen.blit(small_font.render("Turn Order", True, (180, 100, 255)), (turn_box_x + 8, turn_box_y + 6))
        pygame.draw.line(virtual_screen, (180, 100, 255), (turn_box_x + 8, turn_box_y + 24), (turn_box_x + turn_box_w - 8, turn_box_y + 24), 1)

        for i, p in enumerate(turn_order):
            row_y = turn_box_y + 32 + i * 22
            row_color = yellow if i == turn_cursor and active_panel == "TURN ORDER" else (gray if i == turn_first_selected else white)
            virtual_screen.blit(small_font.render(f"{i+1}. {p.name}", True, row_color), (turn_box_x + 20, row_y))
            if i == turn_cursor and active_panel == "TURN ORDER":
                pygame.draw.polygon(virtual_screen, yellow, [(turn_box_x + 8, row_y + 4), (turn_box_x + 16, row_y + 8), (turn_box_x + 8, row_y + 12)])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                display_res = (event.w, event.h)
                window = pygame.display.set_mode(display_res, pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    active_panel = "TURN ORDER" if active_panel == "ENABLER" else "ENABLER"
                    cursor_index = 0
                    turn_cursor = 0
                    turn_first_selected = -1
                    if cursor_sound:
                        cursor_sound.play()
                if event.key == pygame.K_LEFT:
                    hero_index = (hero_index - 1) % len(party)
                    cursor_index = 0
                    if cursor_sound:
                        cursor_sound.play()
                elif event.key == pygame.K_RIGHT:
                    hero_index = (hero_index + 1) % len(party)
                    cursor_index = 0
                    if cursor_sound:
                        cursor_sound.play()
                elif event.key == pygame.K_UP:
                    if active_panel == "ENABLER":
                        cursor_index = (cursor_index - 1) % len(available_enabler)
                    else:
                        turn_cursor = (turn_cursor - 1) % len(turn_order)
                    if cursor_sound:
                        cursor_sound.play()
                elif event.key == pygame.K_DOWN:
                    if active_panel == "ENABLER":
                        cursor_index = (cursor_index + 1) % len(available_enabler)
                    else:
                        turn_cursor = (turn_cursor + 1) % len(turn_order)
                    if cursor_sound:
                        cursor_sound.play()
                elif event.key == pygame.K_SPACE:
                    if confirm_sound:
                        confirm_sound.play()
                    if active_panel == "ENABLER":
                        selected_enabler = available_enabler[cursor_index]
                        if selected_enabler in hero.enabler:
                            hero.enabler.remove(selected_enabler)
                        elif len(hero.enabler) < MAX_ENABLER_SLOTS:
                            for p in party:
                                if selected_enabler in p.enabler:
                                    p.enabler.remove(selected_enabler)
                            hero.enabler.append(selected_enabler)
                    else:
                        if turn_first_selected == -1:
                            turn_first_selected = turn_cursor
                        elif turn_first_selected == turn_cursor:
                            turn_first_selected = -1  # Deselect
                        else:
                            turn_order[turn_first_selected], turn_order[turn_cursor] = turn_order[turn_cursor], turn_order[turn_first_selected]
                            turn_first_selected = -1
                elif event.key == pygame.K_RETURN:
                    is_equipping = False
                    if confirm_sound:
                        confirm_sound.play()
                    return display_res

        scaled_surface = pygame.transform.scale(virtual_screen, display_res)
        window.blit(scaled_surface, (0, 0))
        pygame.display.flip()