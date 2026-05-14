from dataclasses import dataclass

from Options import Choice, Range, Toggle, PerGameCommonOptions

class LogicComplexity(Choice):
    """
    Determines the routing complexity required of the player.
    Not currently implemented
    
    Simple: Smiler Idols and Cheats will not be factored into logic unless absolutely required to reach a location.
        Many (future) settings will be unavailable with Simple Logic.
    
    Full: Any method to reach a location will be in logic.
    
    """
    display_name = "Logic Complexity"
    option_simple = 0
    option_full = 1
    default = 0

class LocustCapacityUp(Range):
    """
    How much each Max Locust Up will increase you locust carrying capacity.
    No effect without Locustsanity. Valid range is 1-5.
    It is not reccommended to set this to 1, as there are not enough locations
    """
    display_name = "Max Locust Up Size"
    range_start = 1
    range_end = 5
    default = 2

class Brandsanity(Toggle):
    """
    When enabled, the ability to carve each lord's brand into rooms are shuffled into the item pool and
     the inspecting each mural depicting them gives a check.
    """
    display_name = "Brandsanity"
    default = 1

class Idolsanity(Toggle):
    """
    When enabled, the Lover, Smiler, and Killer Idols are eggs until their respective items are received, and
     once restored, talking to them with the void memory gives checks.
    """
    display_name = "Idolsanity"

class Shortcutsanity(Toggle):
    """
    When enabled, the ability to use each of Mon's shortcuts are shuffled into the item pool, and talking to them is a check.
    """
    display_name = "Shortcutsanity"
    default = 1

class GreedZone(Toggle):
    """
    When enabled, adds 15 items and locations, for the 15 chests at the end of a certain optional area accessible from B193.
    Entry is locked until all Greed Coins are collected.
    Only works if Locustsanity is enabled.
    """
    display_name = "Greed Zone"

class GreedCoinAmount(Range):
    """
    Sets the amount of Greed Coins in the pool.
    Only works if the Greed Zone is enabled. Valid range is 1-30.
    """
    display_name = "Greed Coin Amount"
    range_start = 1
    range_end = 30
    default = 15

class SkipCutscenes(Toggle):
    """
    When enabled, the final cutscene at the end of the game is skipped, stepping onto the elevator brings you
     instantly to controlling Lily in the final room.
    """
    display_name = "Skip Cutscenes"
    default = 1

class VisibleInterface(Toggle):
    """
    Normally before receiving the ability to manipulate the interface, it is entirely blocked by voider statues in rooms
     that allow access to the interface. If you prefer to see the interface even when you cant mess with it, set this to
     true so these specific voiders are invisible.
    """
    display_name = "Visible Interface"

@dataclass
class VoidStrangerOptions(PerGameCommonOptions):
    logiccomplexity: LogicComplexity
    locustcapacityup: LocustCapacityUp
    brandsanity: Brandsanity
    idolsanity: Idolsanity
    shortcutsanity: Shortcutsanity
    greedzone: GreedZone
    greedcoinamount: GreedCoinAmount
    skipcutscenes: SkipCutscenes
    visibleinterface: VisibleInterface