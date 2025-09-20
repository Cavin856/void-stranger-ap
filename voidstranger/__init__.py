import importlib
from typing import Dict, List
from collections import defaultdict
from BaseClasses import Region, Item, CollectionState, ItemClassification
from worlds.AutoWorld import WebWorld, World, LogicMixin

from .Constants.ItemNames import greed_coin
from .Items import VoidStrangerItem, burden_item_data_table, misc_item_data_table, brand_item_data_table, \
    statue_item_data_table, shortcut_item_data_table, locust_item_table, item_data_table, item_table, \
    prog_brand_item_data_table
from .Locations import VoidStrangerLocation, burden_location_data_table, misc_location_data_table,\
    mural_location_data_table, statue_location_data_table, shortcut_location_data_table, chest_location_data_table, \
    location_table, greed_chest_location_data_table
from .Options import VoidStrangerOptions
from .Constants import ItemNames, LocationNames
from .LocationGroups import vs_location_groups

class VoidStrangerWebWorld(WebWorld):
    theme = "stone"


class VoidStrangerWorld(World):

    #Class Data
    game = "Void Stranger"
    web = VoidStrangerWebWorld()
    options_dataclass = VoidStrangerOptions
    options: VoidStrangerOptions
    location_name_to_id = location_table
    item_name_to_id = item_table
    location_name_groups = vs_location_groups

    #Instance Data
    locusts: ItemClassification.progression
    goal_logic_mapping: Dict[str, List[List[str]]]
    greed_coin_count: int
    
    
    
    # for shuffle floors, we make a list with all main floors allowed by settings (generate keys method or w/e)
    #   then pick a random subset of them to reach 256 floors after first including the required floors.
    # for every floor with a shortcut, we pick a side brane and update the shortcut destination to that new side brane, and add the side brane to a list.
    # then at the end, every side brane in that list gets assigned a possibly random exit floor, somewhere on the main brane_order.
    # lastly, brand floors get their table updated too, and are handled similarily to shortcut floors.
    
    # add exception for B143, where Gor gives you a free locust if you have none? Or just ignore that.
    
    # don't forget that B222 skips a floor
    
    # how dungeon lists work is it's the floor data, but with an extra tag for if it's a main or not, and all grouped under the {DungeonName} key.
    # If the dungeon is excluded by yaml option (either by name, or randomly via dungeon count), it checks the "Standalone" tag for if specific required floors can be added by themselves, without the entrance.
    # Standalone floors become optional for that floor type (main or side)
    # If the dungeon is included, all required dungeon floors are put into their respective required list.
    # we cannot/shouldn't shuffle dungeon entrances?
    # if floor shuffle, assume all dungeons that appear have checks
    # figure out what to do if too many dungeons disabled, becuase then too many side branes are disabled?
    
    def generate_brane_list(self, state) -> None: 
        state.vs_state_initialized[self.player] = True
        state.vs_stale_pathfinding[self.player] = False
        state.vs_brane_order[self.player] = []
        state.vs_brane_list[self.player] = {}
        state.vs_dungeon_list[self.player] = []
        
        pool_required_main = {}
        pool_required_side = {}
        pool_optional_main = {}
        pool_optional_side = {}
        pool_dungeons = {}
        goal_dungeons = ["DIS"]
        floor_pack_list = ["vanilla_floors"]
        # if goal settings
            # add dungeons to goal_dungeons
        #if add community floor packs
            #floor_pack_list.extend(self.options.EnabledFloors)
        
        for enabled_floor_pack in floor_pack_list:
            floor_pack = importlib.import_module(f".Floors.{enabled_floor_pack}", package = __name__)
            pool_required_main.update(floor_pack.RequiredMainBranes)
            pool_required_side.update(floor_pack.RequiredSideBranes)
            pool_optional_main.update(floor_pack.OptionalMainBranes)
            pool_optional_side.update(floor_pack.OptionalSideBranes)
            pool_dungeons.update(floor_pack.Dungeons)
        
        # when shuffle floors is off, excluded dungeons remain, but logic won't place anything there.
        # when shuffle floors is on, excluding a dungeon will remove it's entrance and all related floors entirely
        if False: #if shuffle floors
            print("dummy line")
            # if treasure hunter / ninnie (except always do this?)
                # add first and last floors of their sequence to required, as well as 5 other random floors from their sequence
                # then, put the rest of their sequence into optional
            # edit brand and shortcut connections as necessary
            # for dungeon not in goal_dungeons:
                # etc
            # for generation, include option for a floor to be "locked" behind the placement of another floor.
            # aka, if a floor is placed, it pulls it's corrosponding floor from the locked pool
            # also, allow for floors to be placed in any order, sometimes shortcuts taken first, sometimes not, etc
            
        else:
            state.vs_brane_order[self.player] = Floors.vanilla_floors.VanillaBraneOrder
            state.vs_brane_list[self.player].update(pool_required_main)
            state.vs_brane_list[self.player].update(pool_required_side)
            state.vs_brane_list[self.player].update(pool_optional_main)
            state.vs_brane_list[self.player].update(pool_optional_side)
            state.vs_brane_list[self.player].update(Floors.vanilla_floors.VanillaDungeonEntrances)
        
        # Add the access rule tags to each active floor
        for brane in state.vs_brane_list[self.player]:
            state.vs_brane_list[self.player][brane].update({"Accessible": False, "Locust_Score": -1})
        
        # parse stair connections with "next"
        for brane in state.vs_brane_order[self.player]:
            if state.vs_brane_list[self.player][brane]["Stairs"] != False:
                if state.vs_brane_list[self.player][brane]["Stairs"][0] == "next":
                    if state.vs_brane_order[self.player].index(brane) == 255:
                        if False:   # if white void dungeon is enabled
                            state.vs_brane_list[self.player][brane]["Dungeon"] = ("white_void", state.vs_brane_list[self.player][brane]["Stairs"][1])
                        state.vs_brane_list[self.player][brane]["Stairs"] = False
                    else:
                        state.vs_brane_list[self.player][brane]["Stairs"] = (state.vs_brane_order[self.player][state.vs_brane_order[self.player].index(brane) + 1], state.vs_brane_list[self.player][brane]["Stairs"][1]) # messy line to replace a tuple

        # parse brane connections
        #for brane in state.vs_brane_order[self.player]:
        #    if state.vs_brane_list[self.player][brane]["Brand_Room"] != False:
        #        if state.vs_brane_list[self.player][brane]["Shortcut"] == False:
        #            state.vs_brane_list[self.player][brane]["Shortcut"] = []
        #        for brand_carve in Floors.vanilla_floors.VanillaBrandCarving[brane]:
        #            state.vs_brane_list[self.player][brane]["Shortcut"].append((brand_carve[0], brand_carve[1]))
        #    state.vs_brane_list[self.player][brane]["Brand_Room"] = False
        #
        #for brane in state.vs_brane_list[self.player]:
        #    print(brane + " " + str(state.vs_brane_list[self.player][brane]["Shortcut"]))
        #input()
        #self.calculate_accessibility(state)
    
    # connection tuple format: (destination, [[option A item_tuples],[option B item_tuples]], running_locust_score)
    def check_floor_connection(self, state, connection_tuple, current_brane, brane_index) -> tuple[bool, str, int|str]:
        from .Rules import check_item_tuples
        if state.vs_brane_list[self.player][connection_tuple[0]]["Accessible"] == True and state.vs_brane_list[self.player][connection_tuple[0]]["Locust_Score"] >= connection_tuple[2]:
            return False, current_brane, brane_index
        if check_item_tuples(self, state, connection_tuple[1]):
            if connection_tuple[0] in state.vs_brane_order[self.player]:
                brane_index = state.vs_brane_order[self.player].index(connection_tuple[0])
            else:
                brane_index = "???"
            return True, connection_tuple[0], brane_index
        else:
            return False, current_brane, brane_index
            
    
    def calculate_accessibility(self, state) -> None:
        from .Rules import has_item_by_type, check_item_tuples
        if not state.vs_state_initialized[self.player]:
            self.generate_brane_list(state)
            
        shortcut_list = []          # connection tuples: (destination, [[option A item_tuples],[option B item_tuples]], running_locust_score)
        smiler_list = []            # tuples with format: (current_floor, brane_index, [[option A item_tuples],[option B item_tuples]], running_locust_score, [last_checked_index_offset])
        interface_list = []         # tuples with format: (current_floor, brane_index, [[option A item_tuples],[option B item_tuples]], running_locust_score, [last_checked_index_offset])
        
        # clear lingering tags from previous pathfinding attempt
        for brane in state.vs_brane_list[self.player]:
            state.vs_brane_list[self.player][brane].update({"Accessible": False, "Locust_Score": -1})
        
        brane_index = state.vs_brane_order[self.player].index("B001")
        current_brane = "B001"
        if self.options.locustsanity:
            running_locust_score = state.prog_items[self.player]["locusts"]
        else:
            running_locust_score = 0
        
        while True:
            #print(shortcut_list)
            #print(current_brane)
            #print(brane_index)
            #input(running_locust_score)
            result = False
            state.vs_brane_list[self.player][current_brane]["Accessible"] = True
            state.vs_brane_list[self.player][current_brane]["Locust_Score"] = running_locust_score
            
            if not self.options.locustsanity:
                running_locust_score += state.vs_brane_list[self.player][current_brane]["Chest_Score"]
                if running_locust_score > 99:
                    running_locust_score = 99
            
            if state.vs_brane_list[self.player][current_brane]["Shortcut"] != False:
                # allowing for multiple shortcuts on the same floor
                for shortcut in state.vs_brane_list[self.player][current_brane]["Shortcut"]:
                    shortcut_list.append((shortcut[0], shortcut[1], running_locust_score))
            if state.vs_brane_list[self.player][current_brane]["Smiler"] != False:
                smiler_list.append((current_brane, brane_index, state.vs_brane_list[self.player][current_brane]["Smiler"], running_locust_score, [0])) #putting the last var in a list is hacky
            if state.vs_brane_list[self.player][current_brane]["Interface"] != False and has_item_by_type(self, state, "item", ItemNames.interface_manip):
                interface_list.append((current_brane, brane_index, state.vs_brane_list[self.player][current_brane]["Interface"], running_locust_score, [0]))
            if state.vs_brane_list[self.player][current_brane]["Brand_Room"] != False:
                for brand_carve in Floors.vanilla_floors.VanillaBrandCarving[current_brane]:
                    shortcut_list.append((brand_carve[0], brand_carve[1], running_locust_score))
                #input(shortcut_list)
            
            if state.vs_brane_list[self.player][current_brane]["Stairs"] != False:
                # check for Skipped tag
                result, current_brane, brane_index = self.check_floor_connection(state, (state.vs_brane_list[self.player][current_brane]["Stairs"][0], state.vs_brane_list[self.player][current_brane]["Stairs"][1], running_locust_score), current_brane, brane_index)
                if result:
                    continue
            
            # do interface connections first?
            if shortcut_list != []:
                for shortcut in shortcut_list:
                    result, current_brane, brane_index = self.check_floor_connection(state, shortcut, current_brane, brane_index)
                    shortcut_list.remove(shortcut)
                    if result:
                        running_locust_score = shortcut[2]
                        break
                if result:
                    continue
            
            if smiler_list != []:
                for smiler in smiler_list:
                    current_brane = smiler[0]
                    brane_index = smiler[1]
                    next_floor_offset = smiler[4][0]
                    if check_item_tuples(self, state, smiler[2]): #redundant, but filters out unreachable smilers earlier
                        while not result:
                            next_floor_offset += 1
                            if next_floor_offset > 99 or smiler[3] - next_floor_offset < 0:
                                #print(smiler)
                                #print(next_floor_offset)
                                #input("abort")
                                smiler_list.remove(smiler)
                                break
                            if brane_index + next_floor_offset > 255:
                                #enable white_void
                                smiler_list.remove(smiler)
                                break
                            next_floor = state.vs_brane_order[self.player][brane_index + next_floor_offset]
                            if not self.options.locustsanity:
                                running_locust_score = 0
                            else:
                                running_locust_score = smiler[3] - next_floor_offset
                            result, current_brane, brane_index = self.check_floor_connection(state, (next_floor, smiler[2], running_locust_score), current_brane, brane_index)
                            #print(next_floor)
                            #print(smiler)
                            #input(result)
                        if result:
                            smiler[4][0] = next_floor_offset
                            break
                if result:
                    continue
            
            #for brane in state.vs_brane_list[self.player]:
            #   print(brane + " " + str(state.vs_brane_list[self.player][brane]["Accessible"]))
            #input()
            break
        state.vs_stale_pathfinding[self.player] = True
    
    
    #add update_locust_counts function
    def collect(self, state: "CollectionState", item: "Item") -> bool:
        change = super().collect(state, item)
        if change and item.name == ItemNames.locust_idol:
            state.prog_items[item.player]["locusts"] += 1
        elif change and item.name == ItemNames.tripled_locust:
            state.prog_items[item.player]["locusts"] += 3
        state.vs_stale_pathfinding[self.player] = False
        #for brane in state.vs_brane_list[self.player]:
           #print(brane + " " + str(state.vs_brane_list[self.player][brane]["Accessible"]))
        #print (item.name)
        #input()
        return change

    def remove(self, state: "CollectionState", item: "Item") -> bool:
        change = super().remove(state, item)
        if change and item.name == ItemNames.locust_idol:
            state.prog_items[item.player]["locusts"] -= 1
        elif change and item.name == ItemNames.tripled_locust:
            state.prog_items[item.player]["locusts"] -= 3
        state.vs_stale_pathfinding[self.player] = False
        return change

    def create_item(self, name: str) -> VoidStrangerItem:
        return VoidStrangerItem(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        item_pool: list[VoidStrangerItem] = []

        location_count: int = 7

        item_pool += [self.create_item(name)
                      for name in burden_item_data_table.keys()
                      if name not in self.options.start_inventory]

        item_pool += [self.create_item(name)
                      for name in misc_item_data_table.keys()
                      if name not in self.options.start_inventory]

        if self.options.locustsanity:
            location_count += 68
            gray_locusts: int = 42
            gray_triple_locusts: int = 26
            #for later
            lillith_locusts: int = 40
            lillith_triple_locusts: int = 29

            if self.options.greedzone:
                location_count += 15
                self.greed_coin_count: int = int(self.options.greedcoinamount.value)
                if self.greed_coin_count > 15:
                    gray_locusts -= self.greed_coin_count - 15 #removing locusts to make room for more greed coins if needed
                    if gray_locusts < 0: #if there are more greed coins than locusts, start removing triple locusts
                        gray_triple_locusts += gray_locusts
                item_pool += [self.create_item(ItemNames.greed_coin) for _ in range(self.greed_coin_count)]

            item_pool += [self.create_item(ItemNames.tripled_locust) for _ in range(gray_triple_locusts)]
            item_pool += [self.create_item(ItemNames.locust_idol) for _ in range(gray_locusts)]
        if self.options.brandsanity:
            location_count+= 9

            if self.options.progressivebrands:
                item_pool += [self.create_item(ItemNames.brand_prog) for _ in range(9)]
            else:
                item_pool += [self.create_item(name)
                              for name in brand_item_data_table.keys()
                              if name not in self.options.start_inventory]
        if self.options.idolsanity:
            location_count+= 3
            item_pool += [self.create_item(name)
                          for name in statue_item_data_table.keys()
                          if name not in self.options.start_inventory]
        if self.options.shortcutsanity:
            location_count+= 5
            item_pool += [self.create_item(name)
                          for name in shortcut_item_data_table.keys()
                          if name not in self.options.start_inventory]

        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        from .Regions import region_data_table

        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

            # Create locations.
        for region_name, region_data in region_data_table.items():
            region = self.multiworld.get_region(region_name, self.player)

            region.add_locations({
                location_name: location_data.address for location_name, location_data in
                burden_location_data_table.items() if location_data.region == region_name
            }, VoidStrangerLocation)

            region.add_locations({
                location_name: location_data.address for location_name, location_data in
                misc_location_data_table.items() if location_data.region == region_name
            }, VoidStrangerLocation)

            if self.options.locustsanity:
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in
                    chest_location_data_table.items() if location_data.region == region_name
                }, VoidStrangerLocation)

                if self.options.greedzone:
                    region.add_locations({
                        location_name: location_data.address for location_name, location_data in
                        greed_chest_location_data_table.items() if location_data.region == region_name
                    }, VoidStrangerLocation)

            if self.options.brandsanity:
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in
                    mural_location_data_table.items() if location_data.region == region_name
                }, VoidStrangerLocation)

            if self.options.idolsanity:
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in
                    statue_location_data_table.items() if location_data.region == region_name
                }, VoidStrangerLocation)

            if self.options.shortcutsanity:
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in
                    shortcut_location_data_table.items() if location_data.region == region_name
                }, VoidStrangerLocation)

            region.add_exits(region_data_table[region_name].connecting_regions)

    def set_rules(self) -> None:
        from .Rules import set_rules
        set_rules(self)

    def fill_slot_data(self):
        return {
            "locustsanity": self.options.locustsanity.value,
            "brandsanity": self.options.brandsanity.value,
            "progressivebrands": self.options.progressivebrands.value,
            "idolsanity": self.options.idolsanity.value,
            "shortcutsanity": self.options.shortcutsanity.value,
            "shortcutcheating": self.options.shortcutcheating.value,
            "greedzone": self.options.greedzone.value,
            "greedcoinamount": self.options.greedcoinamount.value,
            "skipcutscenes": self.options.skipcutscenes.value,
            "visibleinterface": self.options.visibleinterface.value
        }
        
class vsstate(LogicMixin):
    vs_stale_pathfinding: dict[int, bool]
    vs_brane_order: dict[int, list]            # ordered list of all 255 main branes in the seed
    vs_brane_list: dict[int, dict]             # dict of all branes in the seed, in the form {brane_id: {brane_data}}
    vs_dungeon_list: dict[int, list]           # list of dungeons in the seed, in format (dungeon_name, accessible?)
    
    def init_mixin(self, _):
        self.vs_state_initialized = defaultdict(lambda: False)
        self.vs_stale_pathfinding = defaultdict(lambda: False)
        self.vs_brane_order = defaultdict(lambda: [])
        self.vs_brane_list = defaultdict(lambda: {}) 
        self.vs_dungeon_list = defaultdict(lambda: [])
        