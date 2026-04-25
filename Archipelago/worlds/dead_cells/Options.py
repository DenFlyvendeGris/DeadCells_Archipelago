"""
Dead Cells APWorld — options.py

All player-configurable YAML options are defined here.
Each class maps to one option in the player's YAML file.
The dataclass DeadCellsOptions collects them all and is
assigned to the World via options_dataclass.
"""

from dataclasses import dataclass
from Options import Choice, DefaultOnToggle, Range, Toggle, PerGameCommonOptions


# ── Goal ──────────────────────────────────────────────────────────────────────

class Goal(Choice):
    """Determines the victory condition for this randomizer run.

    - **hand_of_the_king**: Defeat the Hand of the King. Accessible to all
      players with no DLC required. This is the default goal.
    - **the_collector**: Defeat the Collector, the true final boss. Requires
      the Rise of the Giant DLC to be enabled. The player must first defeat the
      Hand of the King to unlock the Cavern, defeat the Giant, traverse the
      Astrolab, and fight the Hand of the King a second time before the
      Collector is revealed.
    - **target_bsc**: Reach and activate a target number of Boss Stem Cells,
      set by the ``target_bsc_level`` option. Useful for shorter runs.
    """
    display_name = "Goal"
    rich_text_doc = True
    option_hand_of_the_king = 0
    option_the_collector = 1
    option_target_bsc = 2
    default = 0


class TargetBSCLevel(Range):
    """The number of Boss Stem Cells required to complete the run.

    Only relevant when ``goal`` is set to ``target_bsc``.
    Boss Stem Cells are items in the multiworld pool and must be received
    before the goal is considered complete.
    """
    display_name = "Target BSC level"
    range_start = 1
    range_end = 5
    default = 3


# ── DLC toggles ───────────────────────────────────────────────────────────────

class DLCRiseOfTheGiant(Toggle):
    """Include Rise of the Giant DLC content.

    Adds the Cavern, Guardian's Haven, and Astrolab biomes, the Giant boss,
    and all associated blueprints and locations.
    Required if ``goal`` is set to ``the_collector``.
    """
    display_name = "DLC: Rise of the Giant"


class DLCTheBadSeed(Toggle):
    """Include The Bad Seed DLC content.

    Adds the Dilapidated Arboretum, Morass of the Banished, and Nest biomes,
    the Mama Tick boss, and all associated blueprints and locations.
    """
    display_name = "DLC: The Bad Seed"


class DLCFatalFalls(Toggle):
    """Include Fatal Falls DLC content.

    Adds the Fractured Shrines, Undying Shores, and Mausoleum biomes,
    the Scarecrow boss, and all associated blueprints and locations.
    """
    display_name = "DLC: Fatal Falls"


class DLCQueenAndTheSea(Toggle):
    """Include The Queen and the Sea DLC content.

    Adds the Infested Shipwreck, Lighthouse, and related biomes,
    the Servants and the Queen boss fight, and all associated blueprints
    and locations.
    """
    display_name = "DLC: The Queen and the Sea"


# ── Item pool options ─────────────────────────────────────────────────────────

class ScrollShuffle(DefaultOnToggle):
    """Shuffle scrolls into the multiworld item pool.

    When enabled, Power Scrolls, Dual Scrolls, and Cursed Scrolls are
    added to the item pool and may be received from any player's world.
    When disabled, scrolls remain as vanilla in-run drops and are not
    randomized.
    """
    display_name = "Scroll shuffle"


class BSCShuffle(DefaultOnToggle):
    """Shuffle Boss Stem Cells into the multiworld item pool.

    When enabled, all five Boss Stem Cell upgrades are items in the pool.
    They may need to be received from other players before higher
    difficulty tiers and certain BSC-locked doors become accessible.
    When disabled, BSC upgrades unlock through vanilla means.
    """
    display_name = "BSC shuffle"


class TrapPercentage(Range):
    """Percentage of filler item slots replaced with trap items.

    Traps include Curse Traps and Malaise Traps, which apply negative
    effects to the player when received. Set to 0 to disable traps entirely.
    """
    display_name = "Trap percentage"
    range_start = 0
    range_end = 50
    default = 10


class StartingWeapon(Choice):
    """Determines the weapon the player starts each run with.

    - **any**: A random weapon is chosen from whichever blueprints
      have been received so far.
    - **rusty_sword**: The player always starts with the base Rusty Sword,
      regardless of received blueprints.
    """
    display_name = "Starting weapon"
    rich_text_doc = True
    option_any = 0
    option_rusty_sword = 1
    default = 0


class BlueprintCount(Choice):
    """Controls how many weapon and skill blueprints are included in the pool.

    - **all**: Every blueprint in the game (subject to DLC toggles) is
      placed into the item pool. Results in a large pool with many locations.
    - **subset**: A curated subset of blueprints is included, keeping the
      pool manageable. Outfit blueprints are excluded; weapons, skills,
      shields, and key mutations are included.
    """
    display_name = "Blueprint count"
    rich_text_doc = True
    option_all = 0
    option_subset = 1
    default = 1


# ── Dataclass ─────────────────────────────────────────────────────────────────

@dataclass
class DeadCellsOptions(PerGameCommonOptions):
    # Goal
    goal: Goal
    target_bsc_level: TargetBSCLevel

    # DLC
    dlc_rise_of_the_giant: DLCRiseOfTheGiant
    dlc_the_bad_seed: DLCTheBadSeed
    dlc_fatal_falls: DLCFatalFalls
    dlc_queen_and_the_sea: DLCQueenAndTheSea

    # Item pool
    scroll_shuffle: ScrollShuffle
    bsc_shuffle: BSCShuffle
    trap_percentage: TrapPercentage
    starting_weapon: StartingWeapon
    blueprint_count: BlueprintCount