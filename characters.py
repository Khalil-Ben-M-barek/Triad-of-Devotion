import pygame
import random
from constants import ENABLER_STATS

class Characters:
    def __init__(self, name, hp, mp, x, y, image_path, portrait_image_path=None, controlled_image_path=None, fainted_image_path=None, is_enemy=False):
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
        self.is_counter_active = False
        self.is_twin_cast_active = False
        self.is_controlled = False
        self.cooldowns = {"Counter": 0, "Twin Cast": 0, "Charge": 0}
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (300, 450))
            if is_enemy:
                self.image = pygame.transform.scale(self.image, (250, 250))
        except:
            self.image = pygame.Surface((100, 200))
            self.image.fill((80, 80, 120))

        self.original_image = self.image
        try:
            if controlled_image_path:
                self.controlled_image = pygame.image.load(controlled_image_path).convert_alpha()
                self.controlled_image = pygame.transform.scale(self.controlled_image, (300, 450))
            else:
                self.controlled_image = self.image.copy()
        except:
            self.controlled_image = pygame.Surface((100, 200))
            self.controlled_image.fill((200, 50, 50))

        try:
            if fainted_image_path:
                self.fainted_image = pygame.image.load(fainted_image_path).convert_alpha()
                self.fainted_image = pygame.transform.scale(self.fainted_image, (300, 450))
        except:
            self.fainted_image = pygame.Surface((200, 100))
            self.fainted_image.fill((80, 80, 120))

        try:
            if portrait_image_path:
                self.portrait_image = pygame.image.load(portrait_image_path).convert_alpha()
                self.portrait_image = pygame.transform.scale(self.portrait_image, (300, 450))
        except:
            self.portrait_image = pygame.Surface((100, 200))
            self.portrait_image.fill((80, 80, 120))

        self.is_attacking = False
        self.attack_timer = 0
        self.last_attack_blocked = False
        self.failed_block_attempt = False

        if name == "Ethan":
            self.enabler = ["Potential Seize", "Strike"]
        elif name == "Elena":
            self.enabler = ["Manipulate", "Revive"]
        elif name == "Evelyn":
            self.enabler = ["Rebirth", "Healing"]
        else:
            self.enabler = []

    def heal(self, amount):
        if self.hp > 0:
            self.hp = min(self.max_hp, self.hp + amount)

    def take_damage(self, amount, party, attacker=None):
        if not self.is_enemy and self.is_counter_active:
            self.is_counter_active = False
            if attacker and attacker.is_enemy:
                attacker.hp = max(0, attacker.hp - random.randint(200, 250))
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
                self.potential_value = min(self.max_potential_value, self.potential_value + ((amount // 2) / self.max_hp) * 170)
                protector.potential_value = min(protector.max_potential_value, protector.potential_value + ((amount // 2) / protector.max_hp) * 170)
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