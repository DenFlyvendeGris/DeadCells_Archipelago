# Helper File

# rulesHelperFile.py  — Dead Cells APWorld access rules

# ── Rune helpers ──────────────────────────────────────────────────
def has_vine(state, player):
    return state.has("Vine Rune", player)

def has_teleport(state, player):
    return state.has("Teleportation Rune", player)

def has_ram(state, player):
    return state.has("Ram Rune", player)

def has_spider(state, player):
    return state.has("Spider Rune", player)

def has_homunculus(state, player):
    return state.has("Homunculus Rune", player)

# ── BSC helpers ───────────────────────────────────────────────────
def has_bsc(state, player, count):
    # Player needs `count` BSC items in their inventory
    return state.has("Boss Stem Cell", player, count)

# ── DLC helpers ───────────────────────────────────────────────────
def dlc_rotg(state, player):
    return state.has("DLC: Rise of the Giant", player)

def dlc_tbs(state, player):
    return state.has("DLC: The Bad Seed", player)

def dlc_ff(state, player):
    return state.has("DLC: Fatal Falls", player)

def dlc_qats(state, player):
    return state.has("DLC: Queen and the Sea", player)

# ── Stage 2 regions ───────────────────────────────────────────────
def can_reach_promenade(state, player):
    return True                                    # always accessible

def can_reach_toxic_sewers(state, player):
    return has_vine(state, player)                 # Vine Rune gates PQ → Toxic Sewers

def can_reach_arboretum(state, player):            # DLC: The Bad Seed
    return (has_teleport(state, player)
            and dlc_tbs(state, player))

# ── Stage 3 regions ───────────────────────────────────────────────
def can_reach_ramparts(state, player):
    # Free from Promenade — no rune needed
    # OR via Toxic Sewers — also no rune needed from there
    return (can_reach_promenade(state, player)
            or can_reach_toxic_sewers(state, player))

def can_reach_ossuary(state, player):
    # Promenade → Ossuary requires Teleportation Rune
    return (can_reach_promenade(state, player)
            and has_teleport(state, player))

def can_reach_ancient_sewers(state, player):
    # Toxic Sewers → Ancient Sewers requires Ram Rune
    return (can_reach_toxic_sewers(state, player)
            and has_ram(state, player))

def can_reach_morass(state, player):               # DLC: The Bad Seed
    return (can_reach_arboretum(state, player)
            and dlc_tbs(state, player))

# ── Boss 1 arenas ─────────────────────────────────────────────────
def can_reach_black_bridge(state, player):
    return can_reach_ramparts(state, player)

def can_reach_insufferable_crypt(state, player):
    # Accessible via Ossuary OR Ancient Sewers
    return (can_reach_ossuary(state, player)
            or can_reach_ancient_sewers(state, player))

def can_reach_nest(state, player):                 # DLC: The Bad Seed
    return (can_reach_morass(state, player)
            and dlc_tbs(state, player))

# ── Stage 4 regions ───────────────────────────────────────────────
def can_reach_stilt_village(state, player):
    return can_reach_black_bridge(state, player)

def can_reach_slumbering_sanctuary(state, player):
    # Insufferable Crypt → Slumbering Sanctuary requires Spider Rune
    return (can_reach_insufferable_crypt(state, player)
            and has_spider(state, player))

def can_reach_graveyard(state, player):
    # Stilt Village → Graveyard requires Spider Rune
    return (can_reach_stilt_village(state, player)
            and has_spider(state, player))

def can_reach_fractured_shrines(state, player):   # DLC: Fatal Falls
    return (can_reach_black_bridge(state, player)
            and dlc_ff(state, player))

# ── Stage 5 regions ───────────────────────────────────────────────
def can_reach_clock_tower(state, player):
    return (can_reach_stilt_village(state, player)
            or can_reach_slumbering_sanctuary(state, player)
            or can_reach_graveyard(state, player))

def can_reach_forgotten_sepulcher(state, player):
    # Requires Teleportation Rune to enter
    return (can_reach_clock_tower(state, player)
            and has_teleport(state, player))

def can_reach_cavern(state, player):               # DLC: Rise of the Giant
    return (has_homunculus(state, player)
            and dlc_rotg(state, player))

def can_reach_undying_shores(state, player):       # DLC: Queen and the Sea
    return (can_reach_black_bridge(state, player)
            and dlc_qats(state, player))

# ── Boss 2 arenas ─────────────────────────────────────────────────
def can_reach_clock_room(state, player):
    return can_reach_clock_tower(state, player)

def can_reach_guardians_haven(state, player):      # DLC: Rise of the Giant
    return (can_reach_cavern(state, player)
            and dlc_rotg(state, player))

def can_reach_mausoleum(state, player):            # DLC: The Bad Seed
    return (can_reach_fractured_shrines(state, player)
            and dlc_tbs(state, player))

# ── Stage 6 regions ───────────────────────────────────────────────
def can_reach_high_peak_castle(state, player):
    return can_reach_clock_room(state, player)

def can_reach_distillery(state, player):
    return can_reach_clock_room(state, player)

def can_reach_infested_shipwreck(state, player):   # DLC: Queen and the Sea
    return (can_reach_undying_shores(state, player)
            and dlc_qats(state, player))

# ── Final boss ────────────────────────────────────────────────────
def can_reach_throne_room(state, player):
    return (can_reach_high_peak_castle(state, player)
            or can_reach_distillery(state, player))

def can_reach_lighthouse(state, player):           # DLC: Queen and the Sea
    return can_reach_infested_shipwreck(state, player)

# ── True ending ───────────────────────────────────────────────────
def can_reach_astrolab(state, player):
    # Requires Homunculus Rune + RotG DLC + having reached Throne Room once
    return (can_reach_throne_room(state, player)
            and can_reach_guardians_haven(state, player)
            and has_homunculus(state, player)
            and dlc_rotg(state, player))

def can_reach_collector(state, player):
    return can_reach_astrolab(state, player)

# ── Goal completion rules ─────────────────────────────────────────
def goal_hand_of_the_king(state, player):
    return can_reach_throne_room(state, player)

def goal_the_collector(state, player):
    return can_reach_collector(state, player)

def goal_target_bsc(state, player, target_level):
    return has_bsc(state, player, target_level)