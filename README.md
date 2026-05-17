# void-stranger-ap
Archipelago integration for Void Stranger. By being here I assume you know everything about the game, if you haven't 
finished the game, then scram!

## How to install this
For generation:
Drop the voidstranger.apworld file into your Archipelago\custom_worlds folder

For playing the game:

Navigate to the betas tab under properties for the game on steam and select the 'old_version_1.1.1' beta to go back to 
the previous version of the game.


Find the data.win file for Void Stranger at {YourSteamLibrary}\steamapps\common\Void Stranger, and patch it using either:

---
### Windows
vsap.bdf (using https://www.romhacking.net/utilities/929/)

or

vsap.xdelta (using https://www.romhacking.net/utilities/598/)

### Linux
install `xdelta3` via your package manager (or distro specific tools) and use the command:

```sh
xdelta3 -d -s data.win vsap.xdelta data_patched.win
```

inside your game directory

or

install `bsdiff` via your package manager (or distro specific tools) and use the command:

```sh
bspatch data.win data_patched.win patch.bdfs
```

inside your game directory

---
and replace the existing data.win file with the patched one, still named data.win. It might also be wise to keep a copy 
of the original data.win file as a backup in case at any point you need to patch the game again (When the patch is 
updated with new content or a fix)

Finally, be sure to add gm-apclientpp.dll and ap_room_names.csv to the Void Stranger folder

## AP Menu

If the game was patched successfully, you can open the AP menu by pushing F10 or binding a controller button to it.
The AP menu has multiple pages, which can be navigated with left and right.

- Connection page

  This is the default page. Here you can input the connection details to connect to the AP server.
  Press Tab to move to the next field, Delete to clear the current field, and Enter to connect to AP.
  Your most recent connection will be saved.

- Mon Bank page

  Any locusts you receive from AP are sent here (if Locust-Sanity is turned on). Up/Down to navigate the options.
  You can withdraw and throw out locusts at will. Throwing out locusts DOES NOT deposit them back into the bank.
  Upon Atoning, your locust count resets as well as the amount withdrawn, but not the amount received.
  For rando balance reasons, you cannot withdraw if that would cause you to hold more than you've received.

- Tracker page

  This page keeps track of all the items you've received.
  Top row is brands, middle row is statues (only three are implemented), bottom row in order is:
  Void Memory, Seal of Lust, Void Wings, Mon Badge (Unimplemented), Void Sword, Seal of Sloth, Void Rod, Interface Manip
  Shortcuts will show up on the right hand side with the shortcut number and an image depicting it.
  The DIS Brand appears as a large DIS Badge between the three rows and the shortcuts, if you have it.

- Waypoints page

  This page allows you to set up to three simultanious waypoints and warp back to them at will.
  Waypoints restore your locust count to what it was when the waypoint was made.
  Waypoints can only be set on numbered branes.

- Extra page

  This page was added as a result of having too many pages.
  The Connection, Debug, and Palette pages can be loaded from here, as these pages are not frequently required.

- Debug page

  Shows several internal variables used for debugging.
  If something clearly wrong occurs with your AP connection, or some items seem to vanish from your inventory,
  please ping @Cavin856 with a screenshot of the debug page in the Void Stranger channel in the AP discord.

  Palette page

  Allows previewing and selecting a custom palette from the palettes.txt file.
  Place the palettes.txt file (a sample file is included) in the save directory, which is NOT the same as the game directory.
  Typically found in appdata/local/void_stranger
  Custom palettes much follow the following format, where each color is a valid hex color preceeded by 0x (this means no #'s)
  Name1
  0xColor1
  0xColor2
  0xColor3
  0xColor4
  Name2
  etc

## Known bugs

1. If your endless void rod was sent to you while you are "Waiting for VR Connection" (Don't have the regular
 Void Rod) you may need to reconnect to properly get the upgrade. Previously you would be unable to get it at all if it
was sent to you while not connected in game, this issue should finally be resolved but please report if this is still 
happening.

2. The greed zone might not open properly the first time, it's unclear from the small amount of testing done. If you run
 into this issue then reconnecting should fix it. 

3. There is a bug with how the game is recompiled by UMT that can cause crashes when a textbox displays with different 
dialogue sounds. I fixed all the ones needed to complete a run, but I'm sure there are other instances of this across 
the game. If you run into this please provide the crash message, so I can fix it.

If you run into an issue not on this list, try reconnecting to the AP server. Regardless of if this resolves the issue, 
report it either on the Void Stranger thread on the AP discord or open an issue with the details here on the repository.

## General options/game info
Game Spoilers ahead, read at your own risk

The apworld assumes you play as Gray with the DIS ending as the only goal. Playing as Lillie will make certain locust 
chest locations uncheckable, and Cif cannot goal. 

Items are not received if the player does not carry the void rod. 
An error message will display: "Waiting for VR Connection" until it is picked up. Then the game sends a sync message to 
the AP server and all items are received. 

The Pause menu contains 2 new options replacing the close game option: Atone and End Run. The first acts as a portable 
atoner, letting you go back to B001 at any time. The second is used to go back to brand entry, mostly so players can 
quickly exit their current run. Going back to brand entry in the middle of an AP run is not recommended as you will lose
your items.

By default, the following are randomized: 

- Burdens
- Seals on the Endless Void Rod, with killing the traitors as locations
- The Endless Void Rod
- The ability to access the interface, with a location on the Egg in Gor's chamber since it hints about the interface. 
Make sure to have the Void Memory for that check.

The location and Item names are intentionally vague to minimize spoiling the game for other players, if you need 
to see what all the names mean you can check the 
item names here: https://github.com/CriminalPancake/void-stranger-ap/blob/main/voidstranger/Constants/ItemNames.py

and the location 
names here: https://github.com/CriminalPancake/void-stranger-ap/blob/main/voidstranger/Constants/LocationNames.py

There are options for the following:

- Randomizing normal chests. Adds locust idols to the pool, and they are managed by the Mon Bank. See "AP Menu" above.
- Adding the ability to use brands to the item pool, with the murals having locations. Without a Void Lord's Brand,
  you cannot progress beyond their domain. No shortcuts of any kind are considered
  in the logic with this enabled at the moment
- Disabling Smilers, Lovers and Killers until finding their respective items. Adds locations for talking to them with 
the void memory. Note that getting all of these items is required for go mode, and you may get stuck without them
in the final area
- Adding ability to use shortcuts to the item pool, talking to Mon in each location gives checks
- Adding the 15 chests (including the 3 before the final room) at the end Mon's Lair as locations. The item pool will 
have 15 "Greed Coins" added which lock the entrance until they are all collected. You can also add more Greed Coins to 
the pool, removing locusts from the pool to make room. This option only works with normal chests being randomized 
already.
- Skipping the long sequence of cutscenes before the final section of gameplay.
- Making the voiders covering the interface invisible, keeping important info visible in all rooms.

For now, the only goal is the DIS ending, goal is sent after completing the final gameplay section before the ending 
sequence.

## Future Plans

This is not an exhaustive list of all future planned updates.
Many more features are planned, but not currently in development.

0.10.0      Logic Part 2, Custom Palette support
0.10.1      Many bug fixes
0.11.0      "Dungeons" / new vanilla checks, Traps
0.12.0      Revamped Item Tracker, New Location Tracker

## Contributors

ThatOneGuy - For making the Manual Void Stranger AP Implementation

[@Rayze421](https://github.com/Rayze421) - For adding location groups to the apworld for plando support, testing, and 
brainstorming ideas.

[@LeonarthCG](https://github.com/LeonarthCG) - For helping a massive amount with the gamemaker net code side of things 
(and of course working on that library in the first place!).

[@CriminalPancake](https://github.com/CriminalPancake) -  For making the initial AP development and paving the way to make future developments possible.

[@Cavin856](https://github.com/Cavin856) -  For handling the current AP development

[@Eijebong](https://github.com/Eijebong) - For rewriting and helping considerably with the pathfinding algorithm and debugging/fuzzing

[@Mysteryem](https://github.com/Mysteryem) - For further help with bugfixes in the python code

Anonymous - For arranging the default custom palettes