"""
Dead Cells APWorld — __init__.py

Main world class. Archipelago loads this file automatically.
All generation logic is orchestrated from here; the heavy data
lives in items.py, locations.py, regions.py, rulesHelperFile.py, and options.py.
"""

from typing import Dict, Any, List

from BaseClasses import Item, ItemClassification, Region, Tutorial
from worlds.AutoWorld import World, WebWorld
from Options import OptionError
from .Options import DeadCellsOptions, Goal
from .Items import (
    ALL_ITEMS, RUNE_ITEMS, BSC_ITEMS, SCROLL_ITEMS,
    BLUEPRINT_ITEMS, DLC_BLUEPRINT_ITEMS, FILLER_ITEMS, TRAP_ITEMS,
    DeadCellsItemData,
)
from .Locations import ALL_LOCATIONS, DeadCellsLocationData
from .Rules import set_rules


# ── Item and Location classes ─────────────────────────────────────────────────

class DeadCellsItem(Item):
    game = "dead_cells"


class DeadCellsLocation:
    """Thin wrapper — actual BaseClasses.Location is created in create_regions."""
    pass


# ── WebWorld ──────────────────────────────────────────────────────────────────

class DeadCellsWebWorld(WebWorld):
    theme = "dirt"
    rich_text_options_doc = True
    tutorials = [
        Tutorial(
            tutorial_name="Setup Guide",
            description="A guide to setting up Dead Cells Archipelago.",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["YourNameHere"],
        )
    ]


# ── World ─────────────────────────────────────────────────────────────────────

class DeadCellsWorld(World):
    """Dead Cells is a roguelite action platformer by Motion Twin and Evil Empire.
    Fight through procedurally generated biomes, collect runes to unlock new
    paths, and face increasingly powerful bosses on your way to the Hand of
    the King — or beyond."""

    game = "Dead Cells"
    options_dataclass = DeadCellsOptions
    options: DeadCellsOptions

    web = DeadCellsWebWorld()

    item_name_to_id = {
        name: data.code
        for name, data in ALL_ITEMS.items()
        if data.code is not None
    }
    location_name_to_id = {
        name: data.code
        for name, data in ALL_LOCATIONS.items()
        if data.code is not None
    }

    # ── Validation ────────────────────────────────────────────────────────────

    def generate_early(self) -> None:
        """Validate option combinations before generation begins."""

        # The Collector goal requires Rise of the Giant DLC
        if (self.options.goal == Goal.option_the_collector
                and not self.options.dlc_rise_of_the_giant):
            raise OptionError(
                f"[Dead Cells] Player {self.player_name}: goal 'the_collector' "
                f"requires 'dlc_rise_of_the_giant' to be enabled."
            )

        # Nudge Vine Rune into early sphere so the player isn't locked out
        # of the entire second half of the map from the start.
        self.multiworld.local_early_items[self.player]["Vine Rune"] = 1

    # ── Regions ───────────────────────────────────────────────────────────────

    def create_regions(self) -> None:
        """Create all regions, connect them, and populate them with locations."""
        from BaseClasses import Location as APLocation

        # All region names we need
        region_names = [
            "Menu",
            "Prisoners' Quarters",
            "Promenade",
            "Toxic Sewers",
            "Prison Depths",
            "Corrupted Prison",
            "Ramparts",
            "Ossuary",
            "Ancient Sewers",
            "Black Bridge",
            "Insufferable Crypt",
            "Stilt Village",
            "Slumbering Sanctuary",
            "Graveyard",
            "Clock Tower",
            "Forgotten Sepulcher",
            "Clock Room",
            "High Peak Castle",
            "Derelict Distillery",
            "Throne Room",
        ]

        # DLC regions (added only when the relevant toggle is on)
        if self.options.dlc_the_bad_seed:
            region_names += ["Dilapidated Arboretum", "Morass", "Nest"]
        if self.options.dlc_fatal_falls:
            region_names += ["Fractured Shrines", "Undying Shores", "Mausoleum"]
        if self.options.dlc_rise_of_the_giant:
            region_names += ["Cavern", "Guardian's Haven", "Astrolab", "Collector's Lair"]
        if self.options.dlc_queen_and_the_sea:
            region_names += ["Undying Shores", "Infested Shipwreck", "Lighthouse"]

        # Deduplicate (Undying Shores appears in two DLCs)
        region_names = list(dict.fromkeys(region_names))

        # Create Region objects
        regions: Dict[str, Region] = {}
        for name in region_names:
            region = Region(name, self.player, self.multiworld)
            regions[name] = region
            self.multiworld.regions.append(region)

        # Create all entrances between regions (rules attached later)
        def connect(source: str, target: str) -> None:
            if source in regions and target in regions:
                regions[source].connect(regions[target], f"{source} -> {target}")

        connect("Menu",                  "Prisoners' Quarters")
        connect("Prisoners' Quarters",   "Promenade")
        connect("Prisoners' Quarters",   "Toxic Sewers")
        connect("Promenade",             "Ramparts")
        connect("Promenade",             "Ossuary")
        connect("Promenade",             "Prison Depths")
        connect("Toxic Sewers",          "Ramparts")
        connect("Toxic Sewers",          "Ancient Sewers")
        connect("Toxic Sewers",          "Corrupted Prison")
        connect("Ramparts",              "Black Bridge")
        connect("Ossuary",               "Insufferable Crypt")
        connect("Ancient Sewers",        "Insufferable Crypt")
        connect("Black Bridge",          "Stilt Village")
        connect("Insufferable Crypt",    "Slumbering Sanctuary")
        connect("Stilt Village",         "Graveyard")
        connect("Stilt Village",         "Clock Tower")
        connect("Slumbering Sanctuary",  "Clock Tower")
        connect("Graveyard",             "Clock Tower")
        connect("Clock Tower",           "Forgotten Sepulcher")
        connect("Clock Tower",           "Clock Room")
        connect("Forgotten Sepulcher",   "Clock Room")
        connect("Clock Room",            "High Peak Castle")
        connect("Clock Room",            "Derelict Distillery")
        connect("High Peak Castle",      "Throne Room")
        connect("Derelict Distillery",   "Throne Room")

        # DLC connections
        if self.options.dlc_the_bad_seed:
            connect("Prisoners' Quarters",   "Dilapidated Arboretum")
            connect("Dilapidated Arboretum", "Morass")
            connect("Morass",                "Nest")
            connect("Nest",                  "Stilt Village")
        if self.options.dlc_fatal_falls:
            connect("Black Bridge",          "Fractured Shrines")
            connect("Fractured Shrines",     "Undying Shores")
            connect("Undying Shores",        "Mausoleum")
            connect("Mausoleum",             "Clock Tower")
        if self.options.dlc_rise_of_the_giant:
            connect("Prisoners' Quarters",   "Cavern")
            connect("Cavern",                "Guardian's Haven")
            connect("Guardian's Haven",      "Astrolab")
            connect("Astrolab",              "Collector's Lair")
        if self.options.dlc_queen_and_the_sea:
            connect("Black Bridge",          "Undying Shores")
            connect("Undying Shores",        "Infested Shipwreck")
            connect("Infested Shipwreck",    "Lighthouse")

        # Populate regions with locations
        for loc_name, loc_data in ALL_LOCATIONS.items():
            # Skip event locations (handled separately below)
            if loc_data.code is None:
                continue
            # Skip DLC locations if that DLC is not enabled
            if loc_data.dlc and not getattr(self.options, loc_data.dlc):
                continue
            # Skip locations whose region wasn't created
            if loc_data.region not in regions:
                continue

            location = APLocation(
                self.player, loc_name, loc_data.code, regions[loc_data.region]
            )
            regions[loc_data.region].locations.append(location)

        # ── Victory event ──────────────────────────────────────────────────────
        goal = self.options.goal.value

        if goal == Goal.option_hand_of_the_king:
            victory_region = regions["Throne Room"]
            victory_name = "Defeat Hand of the King"
        elif goal == Goal.option_the_collector:
            victory_region = regions.get("Collector's Lair", regions["Throne Room"])
            victory_name = "Defeat The Collector"
        else:  # target_bsc — victory is item-based, no event location needed
            return

        from BaseClasses import Location as APLocation, LocationProgressType
        victory_loc = APLocation(self.player, victory_name, None, victory_region)
        victory_loc.place_locked_item(
            DeadCellsItem("Victory", ItemClassification.progression, None, self.player)
        )
        victory_region.locations.append(victory_loc)

    # ── Items ─────────────────────────────────────────────────────────────────

    def create_items(self) -> None:
        """Build the item pool and add it to the multiworld."""
        pool: List[Item] = []

        def add(name: str, data: DeadCellsItemData) -> None:
            pool.append(DeadCellsItem(name, data.classification, data.code, self.player))

        # Runes — always included (they're the progression backbone)
        for name, data in RUNE_ITEMS.items():
            add(name, data)

        # BSC — only if bsc_shuffle is on
        if self.options.bsc_shuffle:
            for name, data in BSC_ITEMS.items():
                add(name, data)

        # Scrolls — only if scroll_shuffle is on
        if self.options.scroll_shuffle:
            for name, data in SCROLL_ITEMS.items():
                # Add multiple copies — scrolls appear many times per run
                for _ in range(3):
                    add(name, data)

        # Blueprints — base game
        for name, data in BLUEPRINT_ITEMS.items():
            add(name, data)

        # Blueprints — DLC (only if relevant DLC is on)
        for name, data in DLC_BLUEPRINT_ITEMS.items():
            # Determine which DLC this blueprint belongs to by ID range
            if data.code is None:
                continue
            if 45_000_300 <= data.code <= 45_000_319 and self.options.dlc_rise_of_the_giant:
                add(name, data)
            elif 45_000_320 <= data.code <= 45_000_339 and self.options.dlc_the_bad_seed:
                add(name, data)
            elif 45_000_340 <= data.code <= 45_000_359 and self.options.dlc_fatal_falls:
                add(name, data)
            elif 45_000_360 <= data.code <= 45_000_379 and self.options.dlc_queen_and_the_sea:
                add(name, data)

        # Count how many locations we have to fill
        location_count = len([
            loc for loc_name, loc in ALL_LOCATIONS.items()
            if loc.code is not None
            and (not loc.dlc or getattr(self.options, loc.dlc))
        ])

        # Pad pool with filler and traps to match location count
        trap_count = int((location_count - len(pool)) * (self.options.trap_percentage / 100))
        filler_count = location_count - len(pool) - trap_count

        trap_names = list(TRAP_ITEMS.keys())
        filler_names = list(FILLER_ITEMS.keys())

        for i in range(trap_count):
            name = trap_names[i % len(trap_names)]
            add(name, TRAP_ITEMS[name])

        for i in range(max(0, filler_count)):
            name = filler_names[i % len(filler_names)]
            add(name, FILLER_ITEMS[name])

        self.multiworld.itempool += pool

    # ── Rules ─────────────────────────────────────────────────────────────────

    def set_rules(self) -> None:
        set_rules(self.multiworld, self.player, self.options)

    # ── Slot data (sent to the in-game DCCM client) ───────────────────────────

    def fill_slot_data(self) -> Dict[str, Any]:
        """Return data the DCCM in-game client needs to connect and sync."""
        return self.options.as_dict(
            "goal",
            "target_bsc_level",
            "dlc_rise_of_the_giant",
            "dlc_the_bad_seed",
            "dlc_fatal_falls",
            "dlc_queen_and_the_sea",
            "scroll_shuffle",
            "bsc_shuffle",
            "starting_weapon",
        )