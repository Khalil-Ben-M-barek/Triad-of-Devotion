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
battle_menu = [["Attack", "Magic", "Protect Stance"], ["Synergy Abilities", "Potential Breach"]]
protect_used_this_turn = False
current_hover_text = ""
scroll_x = 440


DESCRIPTIONS = {
    "Potential Breach": (
        "A powerful attack available when a character's Potential gauge is full. " 
        "The Potential gauge increases when the character takes damage. "
        "Certain synergy abilities level up a character's Potential attack, "
        "either significantly increasing the damage or adding special effects. "
        "When filled, the character can spend the Potential gauge and a potential level "
        "(if greater than 1) to perform a powerful attack."
    ),
    "Synergy Abilities": (
        "Powerful attacks tied to the number of bars in a character's menu. " 
        "Synergy bars are gained by successfully performing a Protect Stance. " 
        "When enough synergy bars are collected, Synergy Abilities become available. "
        "The attacks involve a partner and grant special perks."
    ), 
    "Basic Attack": "A normal physical strike. No cooldown. Uses no MP. ",

    "Counter": ( 
        "Ethan enters a stance that automatically blocks the next attack that targets him that turn. " 
        "When Ethan successfully blocks with Counter, he immediately COUNTERS, dealing damage equal to two of his basic attacks. " 
        "Has a cooldown of 3 turns." 
    ),         
    "Charge": (
        "Charges Elena's 'Chi' by 1 level (max 2). Can't be used back-to-back. " 
        "Charged levels unlock two special attacks: Brute Force (requires 1 Chi) and Heavy Barrage (requires 2 Chi). " 
        "When using a charged attack, one Chi level is consumed." 
    ),          
    "Brute Force": (
        "Unlocked once Elena has at least 1 Chi. " 
        "Consumes 1 Chi level. Deals more than double the damage of the Basic Attack." 
    ),
    "Heavy Barrage": (
        "Unlocked once Elena has 2 Chi levels. " 
        "Consumes 1 Chi level. Deals more than double the damage of Brute Force." 
    ),   
    "Twin Cast": (
        "The next spell cast by any ally will be duplicated, with the duplicate costing " 
        "0 MP but only dealing half the damage of the first. Cooldown: 3 turns." 
    ),
    "Twin Cast": (
        "Increases the damage of Evelyn's basic attacks for 3 turns. " 
        "This only applies to Evelyn's basic attacks. Has a cooldown of 3 turns." 
    ),
    "Protect Stance": (
        "Any ally can enter this stance and choose one other ally to protect and gain synergy bars with. " 
        "If the next enemy attack is directed at the protected target and the normal block command is successful, "
        "the damage is nullified for that attack and both the protector and the protected gain 1 synergy bar. " 
        "If the block fails, both take half the attack damage. " 
        "If the enemy attacks anyone other than the protected target (including the protector), the Protect Stance fails. " 
        "Only one hero may initiate this stance per party rotation (until all three heroes have acted)."  
    ), 
    "Flurry Slash": "Ethan's Level 1 Potential Breach. Ethan's weakest Potential Breach.",

    "Heavenly Descent": "Ethan's Level 2 Potential Breach. Deals significant damage.",

    "Final Blow": "Ethan's Level 3 Potential. Ethan's most powerful attack.",
    
    "Spinning Kick": "Elena's Level 1 Potential Breach. Elena's weakest Potential Breach.",

    "Tidal Onslaught": "Elena's Level 2 Potential Breach. Deals significant damage.",

    "Celestial Tempest": "Elena's Level 3 Potential Breach. Elena's most powerful attack.",

    "Soothing Gale": "Evelyn's level 1 Potential Breach. Restores half the maximum HP of the entire party.",
    
    "Potential Impart": "Evelyn's level 2 Potential Breach. Completely fills the other two allies' Potential gauges.",

    "full restore": "Evelyn's level 3 Potential Breach. Fully restores the HP and MP of the entire party.",

    "Vicious Dash": "For Ethan and Elena. Requires 3 Synergy bars. Deals moderate damage and revives the potential level of the characters who performed it.",

    "Explosive Impact": "For Ethan and Evelyn. Requires 3 Synergy bars. Deals moderate damage and grants unpotentialed MP for the next spell of each character who performed it.",

    "Synchro Blast": "For Elena and Evelyn. Requires 4 Synergy bars. Deals moderate damage and grants both a potential level increase for each character who performed it and 0 MP cost MP for each of their next spell castings.",

    "Back": "Return to the previous menu.",

    "Magic": "Cast spells using equipped enabler. Each spell consumes a specific amount of MP.",

    "Manipulate": "Choose who the enemy targets for their next attack. Costs 8 MP.",

    "Potential Seize": "Absorb the entire Potential Gauge of a chosen ally. Costs 17 MP.",

    "Revive": "Revives a fallen ally with a small portion of their health restored. Costs 8 MP.",

    "Rebirth": "Revives a fallen ally and fully restore their HP. Costs 18 MP.",

    "Healing": "Recovers a moderate amount of HP. Costs 9 MP.",

    "Strike": "Deals 600 magic damage. Costs 20 MP."
    
}
         
POTENTIAL_MOVES = {
    "Ethan": {1: "Flurry Slash", 2: "Heavenly Descent", 3: "Final Blow"},
    "Elena": {1: "Spinning Kick", 2: "Tidal Onslaught", 3: "Celestial Tempest"},
    "Evelyn": {1: "Soothing Gale", 2: "Potential Impart", 3: "full restore"}
}

ENABLER_STATS = {
    "Manipulate": 8,
    "Potential Seize": 17,
    "Revive": 8,
    "Rebirth": 18,
    "Healing": 9,
    "Strike": 20
}

# The synergy logic needs to be revamped to fix hero being both hero and partner
# The synergy ability option should be inaccessible and grayed out when none of the hero's requirements are met
# The synergy ability option isn't being grayed out correctly 

class SynergyAbility:
    def __init__(self, name, partner, bars_required, perk_type, damage):
        self.name = name
        self.synergy_partner = partner
        self.perk_type = perk_type # Can be "POTENTIAL_LEVEL_UP", "ZERO_MP_COST", or "BOTH"
        self.damage = damage
        self.synergy_bars_required = bars_required

SYNERGY_MOVES = [
    SynergyAbility("Vicious Dash", "Elena", 3, "POTENTIAL_LEVEL_UP", 400),
    SynergyAbility("Explosive Impact", "Evelyn", 3, "ZERO_MP_COST", 400),
    SynergyAbility("Synchro Blast", "Evelyn", 4, "BOTH", 500)
]

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
        self.forced_target = None
        self.chi_level = 0
        self.cooldowns = {"Counter": 0, "Twin Cast": 0, "Charge": 0}
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 200))
        self.is_attacking = False
        self.attack_timer = 0
        self.last_attack_blocked = False
        self.failed_block_attempt = False

        if name == "Ethan": self.enabler = ["Potential Seize", "Strike"]
        elif name == "Elena": self.enabler = ["Manipulate", "Revive"]
        elif name == "Evelyn": self.enabler = ["Rebirth", "Healing"]
        else: self.enabler = []

    def heal(self, amount):
        if self.hp > 0:
            self.hp = min(self.max_hp, self.hp + amount)

    def take_damage(self, amount, party, attacker=None):
        if not self.is_enemy and self.cooldowns["Counter"] > 0:
            return # Damage is nullified

        protector = None
        for p in party:
            if p.is_protecting_target == self:
                protector = p
                break
        if protector:
            block_success = attacker.last_attack_blocked if attacker else False
            if block_success:
                protector.synergy_bars = min(protector.max_synergy_bars, protector.synergy_bars + 1)
                self.synergy_bars = min(self.max_synergy_bars, self.synergy_bars + 1)
                protector.is_protecting_target = None
                return
            else:
                self.hp = max(0, self.hp - amount // 2)
                protector.hp = max(0, protector.hp - amount // 2)
                protector.is_protecting_target = None
                return

        if attacker and attacker.last_attack_blocked:
            amount = 0
            
        if attacker and attacker.is_enemy and attacker.forced_target:
            new_target = attacker.forced_target
            attacker.forced_target = None
            if new_target != self:
                new_target.take_damage(amount, party, attacker)
                return

        self.hp = max(0, self.hp - amount)

        if not self.is_enemy:
            potential_gain = (amount / self.max_hp) * 170
            self.potential_value = min(self.max_potential_value, self.potential_value + potential_gain) # To not exceed the max

def get_potential_options(hero):
    if hero.name in POTENTIAL_MOVES:
        level = hero.potential_level
        return [POTENTIAL_MOVES[hero.name][level], "Back"]
    return ["Back"]

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
            
        potential_x, potential_y = box_x + 75, box_y + 55
        potential_is_full = hero.potential_value >= hero.max_potential_value
        potential_text = "POTENTIAL BREACH" if potential_is_full else "Potential"
        potential_color = orange if hero.potential_value >= hero.max_potential_value else white
        potential_fill_width = (hero.potential_value / hero.max_potential_value) * 100
        pygame.draw.rect(virtual_screen, (80, 80, 80), (potential_x, potential_y, 100, 15))
        pygame.draw.rect(virtual_screen, potential_color, (potential_x, potential_y, potential_fill_width, 15))
        pygame.draw.rect(virtual_screen, white, (potential_x, potential_y, 100, 15), 1) # Border
        virtual_screen.blit(small_font.render(potential_text, True, potential_color), (potential_x, potential_y - 20))

        for lvl in range(3):
            potential_bar_color = yellow if hero.potential_level > lvl else (50, 50, 50)
            pygame.draw.rect(virtual_screen, potential_bar_color, (potential_x + 105 + (lvl * 6), potential_y, 3, 15))




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

def draw_battle_menu(virtual_screen, font, col, row, cur_menu, sub_row, enemy, protect_options, hero, attack_options, potential_options, magic_options, synergy_options, party):
    global current_hover_text, scroll_x

    pygame.draw.rect(virtual_screen, blue, menu_rect)
    pygame.draw.rect(virtual_screen, white, menu_rect, 2)

    pygame.draw.rect(virtual_screen, gray, (enemy.base_x - 20, enemy.base_y - 20, 150, 15)) # HP bar
    pygame.draw.rect(virtual_screen, green, (enemy.base_x - 20, enemy.base_y - 20, (enemy.hp / max(1, enemy.max_hp)) * 150, 15))
    virtual_screen.blit(font.render(f"HP: {enemy.hp}/{enemy.max_hp}", True, white), (enemy.base_x - 20, enemy.base_y - 50))
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
                    if hero.synergy_bars < 3:
                        for p in party:
                            if p != hero and p.synergy_bars < 3:
                                text_color = gray
                elif text == "Protect Stance" and protect_used_this_turn:
                    text_color = gray
                if c == col and r == row and text_color != gray:
                    text_color = yellow
                
                virtual_screen.blit(font.render(text, True, text_color), (tx, ty))

                if c == col and r == row:
                    pointer_x = (tx - 35)
                    pointer_y = (ty + 10)
                    pygame.draw.polygon(virtual_screen, white, [(pointer_x, pointer_y), (pointer_x + 15, pointer_y + 7), (pointer_x, pointer_y + 14)])

    elif cur_menu in ["ATTACK SUBMENU", "PROTECT SUBMENU", "POTENTIAL SUBMENU", "MAGIC SUBMENU", "SYNERGY SUBMENU", "HEALING TARGET SUBMENU", "MANIPULATE TARGET SUBMENU", "SEIZE TARGET SUBMENU", "REVIVAL TARGET SUBMENU"]:
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
            options = [p.name for p in party if  0 < p.hp < p.max_hp] + ["Back"]
        elif cur_menu == "REVIVAL TARGET SUBMENU":
            options = [p.name for p in party if p.hp <= 0] + ["Back"]
        elif cur_menu == "SEIZE TARGET SUBMENU":
            options = [p.name for p in party if p != hero and p.potential_value > 0] + ["Back"]
        elif cur_menu == "MANIPULATE TARGET SUBMENU":
            options = [p.name for p in party] + ["Back"]

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
                if hero.mp < cost:
                    text_color = gray
                
            if cur_menu == "SYNERGY SUBMENU" and text != "Back":
                for m in SYNERGY_MOVES:
                    if text == m.name:
                        for p in party:
                            if p.name == m.synergy_partner and (hero.synergy_bars < m.synergy_bars_required or p.synergy_bars < m.synergy_bars_required):
                                text_color = gray

            if i == sub_row and text_color != gray:
                text_color = yellow
            display_name = text
            if cur_menu == "MAGIC SUBMENU" and text != "Back":
                display_name = f"{text} ({ENABLER_STATS[text]} MP)"

            virtual_screen.blit(font.render(display_name, True, text_color), (tx, ty))
            if i == sub_row and text_color != gray:
                pygame.draw.polygon(virtual_screen, white, [(tx - 35, ty + 10), (tx - 20, ty + 17), (tx - 35, ty + 24)])

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


def main():
    global scroll_x, protect_used_this_turn
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

    enemy = Characters("boss", 10000, 0, 150, 50, "boss.png", is_enemy=True)
    active_hero_index = 0
    target_hero = None

    is_attacking = False
    attack_timer = 0
    enemy_is_attacking = False
    enemy_attack_timer = 0

    cur_menu = "MAIN BATTLE MENU"
    cur_col, cur_row, sub_row = 0, 0, 0
    synergy_options = []
    attack_options = []
    is_running = True
    while is_running:
        virtual_screen.fill((30, 30, 30))
        hero = party[active_hero_index]

        virtual_screen.blit(enemy.image, (enemy.x, enemy.y))
        for p in party:
            virtual_screen.blit(p.image, (p.x, p.y))

        potential_options = get_potential_options(hero)
        magic_options = hero.enabler + ["Back"]
        protect_options = [p.name for p in party if p != hero] + ["Back"]

        draw_individual_menus(virtual_screen, small_font, party, active_hero_index)
        draw_battle_menu(virtual_screen, font, cur_col, cur_row, cur_menu, sub_row, enemy, protect_options, hero, attack_options, potential_options, magic_options, synergy_options, party)

        if active_hero_index == 0 and not is_attacking and not enemy_is_attacking:
            if protect_used_this_turn:
                protect_used_this_turn = False
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
                scroll_x = 200 # to reset scroll when any key is pressed

                if 15 < enemy_attack_timer < 25 and enemy_is_attacking:
                    key_pressed = pygame.key.name(event.key).lower()
                    target_initial = target_hero.name[0].lower()
                    if not enemy.failed_block_attempt and not enemy.last_attack_blocked:
                        if key_pressed == target_initial:
                            enemy.last_attack_blocked = True
                            confirm_sound.play()
                        else:
                            enemy.failed_block_attempt= True

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
                        sub_row = 0 
                        scroll_x = 200
                        if battle_menu[cur_col][cur_row] == "Attack":
                            attack_options = get_unique_abilities(hero)
                            cur_menu = "ATTACK SUBMENU"
                        if battle_menu[cur_col][cur_row] == "Magic":
                            cur_menu = "MAGIC SUBMENU"
                            sub_row = 0
                        elif battle_menu[cur_col][cur_row] == "Protect Stance":
                            if not protect_used_this_turn:
                                cur_menu = "PROTECT SUBMENU"
                        elif battle_menu[cur_col][cur_row] == "Potential Breach":
                            if hero.potential_value >= hero.max_potential_value:
                                cur_menu = "POTENTIAL SUBMENU"
                        elif battle_menu[cur_col][cur_row] == "Synergy Abilities":
                            synergy_options = []
                            for move in SYNERGY_MOVES:
                                if hero.name == "Ethan" and move.name in ["Vicious Dash", "Explosive Impact"]:
                                    synergy_options.append(move.name)
                                elif hero.name == "Elena" and move.name in ["Vicious Dash", "Synchro Blast"]:
                                    synergy_options.append(move.name)
                                elif hero.name == "Evelyn" and move.name in ["Explosive Impact", "Synchro Blast"]:
                                    synergy_options.append(move.name)

                            synergy_options.append("Back")
                            cur_menu = "SYNERGY SUBMENU"
                            sub_row = 0

                elif cur_menu == "SYNERGY SUBMENU":
                    if event.key == pygame.K_UP:
                        sub_row = (sub_row - 1) % len(synergy_options)
                        cursor_sound.play()
                    if event.key == pygame.K_DOWN:
                        sub_row = (sub_row + 1) % len(synergy_options)
                        cursor_sound.play()
                    if event.key == pygame.K_SPACE:
                        confirm_sound.play()
                        move_name = synergy_options[sub_row]
                        if move_name == "Back":
                            cur_menu = "MAIN BATTLE MENU"
                            cur_col, cur_row, sub_row = 0, 0, 0
                        else:
                            selected_move = None
                            for m in SYNERGY_MOVES:
                                if m.name in move_name:
                                    selected_move = m

                            partner = None
                            for p in party:
                                if p.name == selected_move.synergy_partner:
                                    partner = p

                            if(partner and hero.synergy_bars >= selected_move.synergy_bars_required and partner.synergy_bars >= selected_move.synergy_bars_required):
                                hero.synergy_bars -= selected_move.synergy_bars_required
                                partner.synergy_bars -= selected_move.synergy_bars_required
                                enemy.take_damage(selected_move.damage, party)
                                
                                partner_name = selected_move.synergy_partner
                                for p in [hero, partner]:   
                                    if selected_move.perk_type in ["POTENTIAL_LEVEL_UP", "BOTH"]:
                                        p.potential_level = min(3, p.potential_level + 1)
                                    if selected_move.perk_type in ["ZERO_MP_COST", "BOTH"]:
                                        p.zero_mp_cost = True
                                
                                is_attacking = True
                                attack_timer = 40
                                cur_menu = "MAIN BATTLE MENU"
                                cur_col, cur_row, sub_row = 0, 0, 0

                elif cur_menu == "POTENTIAL SUBMENU":
                    if event.key == pygame.K_UP:
                        sub_row = (sub_row - 1) % len(potential_options)
                        cursor_sound.play()
                    if event.key == pygame.K_DOWN:
                        sub_row = (sub_row + 1) % len(potential_options)
                        cursor_sound.play()
                    if event.key == pygame.K_SPACE:
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
                                    p.heal(500)
                                enemy_is_attacking = True
                                enemy_attack_timer = 40
                                cur_menu = "MAIN BATTLE MENU"
                                cur_col, cur_row, sub_row = 0, 0, 0
                            
                            elif current_potential_move == "Potential Impart":
                                for p in party: 
                                    if p != hero: p.potential_value = p.max_potential_value
                                enemy_is_attacking = True
                                enemy_attack_timer = 40
                                cur_menu = "MAIN BATTLE MENU"
                                cur_col, cur_row, sub_row = 0, 0, 0

                            elif current_potential_move == "full restore":
                                for p in party:
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
                        cursor_sound.play()
                    if event.key == pygame.K_DOWN:
                        sub_row = (sub_row + 1) % len(protect_options)
                        cursor_sound.play()
                    if event.key == pygame.K_SPACE and not is_attacking and not enemy_is_attacking:
                        confirm_sound.play()
                        choice = protect_options[sub_row]
                        if choice == "Back":
                                cur_menu = "MAIN BATTLE MENU"
                                cur_col, cur_row, sub_row = 0, 0, 0
                        else:
                            for p in party:
                                if choice == p.name:
                                    hero.is_protecting_target = p
                                    protect_used_this_turn = True
                                    break
                            enemy_is_attacking = True
                            enemy_attack_timer = 40
                            cur_menu = "MAIN BATTLE MENU"
                            cur_col, cur_row, sub_row = 0, 0, 0


                elif cur_menu == "ATTACK SUBMENU":
                    if event.key == pygame.K_UP:
                        sub_row = (sub_row - 1) % len(attack_options)
                        cursor_sound.play()
                    if event.key == pygame.K_DOWN:
                        sub_row = (sub_row + 1) % len(attack_options)
                        cursor_sound.play()
                    if event.key == pygame.K_SPACE and not is_attacking and not enemy_is_attacking:
                        confirm_sound.play()
                        if attack_options[sub_row] == "Back":
                            cur_menu = "MAIN BATTLE MENU"
                            cur_col, cur_row, sub_row = 0, 0, 0
                        elif attack_options[sub_row] == "Basic Attack":
                            enemy.take_damage(random.randint(100, 150), party)
                            is_attacking = True
                            attack_timer = 40
                            cur_menu = "MAIN BATTLE MENU"
                            cur_col, cur_row, sub_row = 0, 0, 0

                elif cur_menu == "MAGIC SUBMENU":
                    if event.key == pygame.K_UP:
                        sub_row = (sub_row - 1) % len(magic_options)
                        cursor_sound.play()
                    if event.key == pygame.K_DOWN:
                        sub_row = (sub_row + 1) % len(magic_options)
                        cursor_sound.play()
                    if event.key == pygame.K_SPACE:
                        spell = magic_options[sub_row]
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
                                cur_menu = "MAIN BATTLE MENU"
                                cur_col, cur_row, sub_row = 0, 0, 0
                                enemy_is_attacking = True
                                enemy_attack_timer = 40

                elif cur_menu == "HEALING TARGET SUBMENU":
                    alive_allies = [p for p in party if p.hp > 0]
                    target_options = [p.name for p in alive_allies] + ["Back"]
                    if event.key == pygame.K_UP:
                        sub_row = (sub_row - 1) % len(target_options)
                        cursor_sound.play()
                    elif event.key == pygame.K_DOWN:
                        sub_row = (sub_row + 1) % len(target_options)
                        cursor_sound.play()
                    if event.key == pygame.K_SPACE:
                        confirm_sound.play()
                        choice = target_options[sub_row]
                        if choice == "Back":
                            cur_menu = "MAGIC SUBMENU"
                            sub_row = 0
                        else:
                            target = alive_allies[sub_row]
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
                        cursor_sound.play()
                    elif event.key == pygame.K_DOWN:
                        sub_row = (sub_row + 1) % len(target_options)
                        cursor_sound.play()
                    if event.key == pygame.K_SPACE:
                        confirm_sound.play()
                        choice = target_options[sub_row]
                        if choice == "Back":
                            cur_menu = "MAGIC SUBMENU"
                            sub_row = 0
                        else:
                            target = dead_allies[sub_row]
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
                    target_options = [p.name for p in party] + ["Back"]
                    if event.key == pygame.K_UP:
                        sub_row = (sub_row - 1) % len(target_options)
                        cursor_sound.play()
                    elif event.key == pygame.K_DOWN:
                        sub_row = (sub_row + 1) % len(target_options)
                        cursor_sound.play()
                    if event.key == pygame.K_SPACE:
                        confirm_sound.play()
                        choice = target_options[sub_row]
                        if choice == "Back":
                            cur_menu = "MAGIC SUBMENU"
                            sub_row = 0
                        else:
                            for p in party:
                                if choice == p.name:
                                    enemy.forced_target = p
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
                        cursor_sound.play()
                    elif event.key == pygame.K_DOWN:
                        sub_row = (sub_row + 1) % len(target_options)
                        cursor_sound.play()
                    if event.key == pygame.K_SPACE:
                        confirm_sound.play()
                        if target_options[sub_row] == "Back":
                            cur_menu = "MAGIC SUBMENU"
                            sub_row = 0
                        else:
                            target = seize_targets[sub_row]
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
                enemy_is_attacking = True
                enemy_attack_timer = 40
                
        if enemy_is_attacking:
            if enemy_attack_timer == 40:
                enemy.last_attack_blocked = False
                enemy.failed_block_attempt = False
                living_heroes = [p for p in party if p.hp > 0]
                if living_heroes:
                    if enemy.forced_target and enemy.forced_target.hp > 0:
                        target_hero = enemy.forced_target
                        enemy.forced_target = None
                    else:
                        target_hero = random.choice(living_heroes)

            if enemy_attack_timer > 25: # First phase of the animation
                enemy.x += 20
                enemy.y += 10
            elif enemy_attack_timer > 15: # Second phase of the animation
                icon_font = pygame.font.SysFont("Arial", 40, bold=True)
                icon_surf = icon_font.render(f"! {target_hero.name[0]}", True, red)
                virtual_screen.blit(icon_surf, (target_hero.x + 60, target_hero.y - 50))
            elif enemy_attack_timer > 0:
                enemy.x -= 20
                enemy.y -= 10

            enemy_attack_timer -= 1

            if enemy_attack_timer == 0:
                enemy_is_attacking = False
                enemy.x, enemy.y = enemy.base_x, enemy.base_y
                target_hero.take_damage(random.randint(100,150), party, attacker=enemy)
                active_hero_index = (active_hero_index + 1) % len(party)

        scaled_surface = pygame.transform.smoothscale(virtual_screen, display_res)
        window.blit(scaled_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

