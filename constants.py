white = (255, 255, 255)
blue = (0, 0, 150)
gray = (100, 100, 100)
yellow = (255, 255, 0)
orange = (255, 165, 0)
green = (0, 255, 0)
red = (255, 0, 0)

menu_rect = (50, 420, 440, 150) # x, y, width, and height
battle_menu = [["Attack", "Magic", "Protect Stance"], ["Synergy Abilities", "Potential Breach"]]
protect_used_this_turn = False
internal_res = (800, 600)
display_res = (1280, 720)

BLOCK_KEYS = {
    "Elena": "l",
    "Ethan": "o",
    "Evelyn": "v"
}

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
    "Basic Attack": "A normal physical strike. No cooldown. ",

    "Counter": (
        "Ethan enters a stance that automatically blocks the next attack that targets him in an entire party rotation. "
        "When Ethan successfully blocks with Counter, he immediately counters, dealing more than double the damage of the Basic Attack. "
        "Ethan cannot be protected in this stance. Has a cooldown of 3 turns."
    ),
    "Charge": (
        "Charges Elena's 'Chi' by 1 level (max 2). Can't be used back-to-back. "
        "Charged levels unlock two special attacks: Brute Force (requires 1 Chi) and Heavy Barrage (requires 2 Chi). "
        "When using a charged attack, one Chi level is consumed."
    ),
    "Brute Force": (
        "Unlocked once Elena's Chi level is 1. "
        "Consumes 1 Chi level. Deals more than double the damage of the Basic Attack."
    ),
    "Heavy Barrage": (
        "Unlocked once Elena's Chi level is 2. "
        "Consumes 1 Chi level. Deals more than double the damage of Brute Force."
    ),
    "Twin Cast": (
        "The next spell cast by any ally will be duplicated, with the duplicate costing "
        "0 MP but only dealing half the damage of the first. Cooldown: 3 turns."
    ),
    "Protect Stance": (
        "Any ally can enter this stance and choose one other ally to protect and gain synergy bars with. "
        "If an attack is directed at the protected target and the normal block command is successful, "
        "the damage is nullified for that attack and both the protector and the protected gain 1 synergy bar. "
        "If the block fails, both take half the attack damage. The stance ends at the end of each party rotation. "
        "Only one hero may initiate this stance per party rotation."
    ),
    "Flurry Slash": "Ethan's Level 1 Potential Breach. Ethan's weakest Potential Breach.",

    "Heavenly Descent": "Ethan's Level 2 Potential Breach. Deals significant damage.",

    "Final Blow": "Ethan's Level 3 Potential. Ethan's most powerful attack.",

    "Spinning Kick": "Elena's Level 1 Potential Breach. Elena's weakest Potential Breach.",

    "Tidal Onslaught": "Elena's Level 2 Potential Breach. Deals significant damage.",

    "Celestial Tempest": "Elena's Level 3 Potential Breach. Elena's most powerful attack.",

    "Soothing Gale": "Evelyn's level 1 Potential Breach. Restores half the maximum HP of the entire party.",
    
    "Potential Impart": "Evelyn's level 2 Potential Breach. Completely fills the other two allies' Potential gauges.",

    "Full Restore": "Evelyn's level 3 Potential Breach. Fully restores the HP and MP of the entire party.",

    "Vicious Dash": "For Ethan and Elena. Requires 3 Synergy bars. Deals moderate damage and raises the potential level of the characters who performed it.",

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
    "Evelyn": {1: "Soothing Gale", 2: "Potential Impart", 3: "Full Restore"}
}

ENABLER_STATS = {
    "Manipulate": 8,
    "Potential Seize": 17,
    "Revive": 8,
    "Rebirth": 18,
    "Healing": 9,
    "Strike": 20
}