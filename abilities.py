from constants import POTENTIAL_MOVES

class SynergyAbility:
    def __init__(self, name, heroes, bars_required, perk_type, damage):
        self.name = name
        self.heroes = heroes
        self.perk_type = perk_type # Can be "POTENTIAL_LEVEL_UP", "ZERO_MP_COST", or "BOTH"
        self.damage = damage
        self.synergy_bars_required = bars_required

SYNERGY_MOVES = [
    SynergyAbility("Vicious Dash", ["Ethan", "Elena"], 3, "POTENTIAL_LEVEL_UP", 400),
    SynergyAbility("Explosive Impact", ["Ethan", "Evelyn"], 3, "ZERO_MP_COST", 400),
    SynergyAbility("Synchro Blast", ["Elena", "Evelyn"], 4, "BOTH", 500)
]

def get_potential_options(hero):
    if hero.name in POTENTIAL_MOVES:
        level = hero.potential_level
        return [POTENTIAL_MOVES[hero.name][level], "Back"]
    return ["Back"]

def get_unique_abilities(hero):
    abilities = ["Basic Attack"]
    if hero.name == "Ethan":
        abilities.append("Counter")

    elif hero.name == "Elena":
        abilities.append("Charge")
        if hero.chi_level == 1:
            abilities.append("Brute Force")
        if hero.chi_level == 2:
            abilities.append("Heavy Barrage")

    elif hero.name == "Evelyn":
        abilities.append("Twin Cast")
    
    abilities.append("Back")
    return abilities