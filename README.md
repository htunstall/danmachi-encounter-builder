# DanMachi Encounter Builder

This tool can be used in conjunction with the information located here (https://sites.google.com/site/danmachidnd/) to run a D&D 5th edition campaign.

## Use

The `data_files` directory contains the configuration file `default.ini` and the `monster_database` files, which you can edit to adjust the settings if the program. The other two files `xp_conversion` and `xp_database` should not need editing as they draw there values from the dungeon masters guide and other official sources.

### Running a python file
Run the `danmachi_builder.py` file to start the program. This program has been developed using anaconda3 (https://www.anaconda.com/download/) however the dependencies are far less than what are included in anaconda:

- `os`
- `sys`
- `time`
- `random`
- `platform`
- `configparser`
- `csv`
- `tkinter`
- `platform`

### Running an exe file
Two executable files have been included in the `dist` directory. They were compiled on Windows 7 Professional, so it may not run on all versions of windows. The `DanMachiBuilder.exe` file runs the program without a command prompt, whereas the `wCMD_DanMachiBuilder.exe`  displays the cmd whilst running the program. If you are unable to run the executable files follow the steps below to compile the executable file:

1. Start a command prompt with the `PYTHONPATH` or `PATH` set correctly (see opening an anaconda terminal below)
2. Navigate to the root directory of this repository on you system (the folder containing `danmachi_builder.py`) using the `cd` command. For example if this repositroy was on your desktop you would type the following command: `cd C:\Users\[username]\Desktop\danmachi-encounter-builder` (Note this command is case sensitive)
3. If you have pyinstaller installed move straight to step 4, otherwise run the following command to install pyinstaller: `pip install pyinstaller`
4. There are two executable files. To generate the:
    1. `DanMachiBuilder.exe` file, type: `pyinstaller -Fw -i data_files\icon.ico -n DanMachiBuilder danmachi_builder.py`
    2. `wCMD_DanMachiBuilder.exe` file, type: `pyinstaller -F -i data_files\icon.ico -n wCMD_DanMachiBuilder danmachi_builder.py`
5. The new executable has replaced the old one in the `dist` folder.
6. Run the executable!

### Opening a python `PATH` set command prompt
1. After installing Anaconda3 (https://www.anaconda.com/download/) open the anaconda navigator
2. follow the steps in the screenshot below:

![alt text](https://raw.githubusercontent.com/htunstall/danmachi-encounter-builder/master/documentation/images/anaconda-navigator-open-teminal.png)

3. Great! You have a command prompt with the correct `PYTHONPATH` open

## Example UI

![alt text](https://raw.githubusercontent.com/htunstall/danmachi-encounter-builder/master/documentation/images/ui_example.png)


*Figure 1*

## Known Bugs

- None

## Breif Documentation
### Build information Pane
#### Dungeon (Floor)

The floor of the dungeon the party is on. This determines which types of monsters spawn based on the settings in the `monster_database.csv` file, which is located in the `data_files` folder. Different monsters also have a preference for spawning on a certain floor. For example these monsters avalible to spawn on floor 1:

Monster           | Floor Preference | Floor Range |
----------------- | ---------------- | ----------- |
Kobold            |         1        |   1 to 4    |
Blood Hawk        |         2        |   1 to 4    |
Constrictor Snake |         2        |   1 to 4    |
Goblin            |         1        |   1 to 4    |
Blink Dog         |         3        |   1 to 4    |
Giant Wolf Spider |         4        |   1 to 4    |
Hobgoblin         |         1        |   1 to 4    |
Lizardfolk        |         3        |   1 to 4    |
Orc               |         3        |   1 to 4    |
Bugbear           |         2        |   1 to 4    |
Ogre              |         2        |   1 to 4    |


* On floor one you are more likely to get Kobolds, Goblins and Hobgoblins.
* Whereas on floor three you are more likely to get Hyenas, Blink Dogs, Lizardfolk and Orcs.

#### Dungeon (Allow CR 0 Monsters)

If this is checked, CR 0 monsters can be included in the encounter. Again, these monsters are pulled from the `monster_database.csv` file.

 Monster          | Floor Preference | Floor Range |
----------------- | ---------------- | ----------- |
Rat               |         1        |   1 to 50   |
Bat               |         1        |   1 to 50   |
Hyena             |         3        |   3 to 50   |
Jackal            |         4        |   4 to 50   |
Giant Fire Beetle |         5        |   5 to 50   |

#### Party (Size)

The numper of players in the party. This is used to calculate the XP for the encounter.

#### Party (Level)

The level of the players in the party. Unfortunaitly, this only allows for all aprty members to be the same level. If this is not the cae, please adhust the difficulty acordingly.

#### Party (Drop Chance)

This is the drop chance DC as described [here](https://sites.google.com/site/danmachidnd/custom-rules/the-dungeon) in the Drop Items section.

#### Difficulty (DC for Encounter & DC Rolled)

The DC for the encounter acts as the lower bound for diffuculty, as when this value is combined with the DC rolled, the difficulty for the encounter is calculated.

When the DC Rolled is one the difficulty is "Deadly" as defined in the DM's guide (p. 82), and when the DC rolled is one less than the DC for encounter then the difficulty is "Easy". Any number inbetween is a linear spline between the easy and deadly dificulties. At the moment multipliers are not inplemented for scaling dificulty. 

- - - -
### Controls Pane
#### Build Encounter

When you click this button the values from the `Build Information` pane are taken and used to generate an encounter. The output is placed in the log frame.

#### Wipe Event Log

When clicked the `Event Log` is cleared.

#### Show Monster Stats

This button opens a new user interface with all the current monsters in the encounter listed as clickable buttons (Figure 2). When each of these buttons are clicked then the stats for that monster are displayed in a new window (Figure 3). Multiple monster stat windows can be opened at once.

![alt text](https://raw.githubusercontent.com/htunstall/danmachi-encounter-builder/master/documentation/images/ui_select-a-monster.png)


*Figure 2*

![alt text](https://raw.githubusercontent.com/htunstall/danmachi-encounter-builder/master/documentation/images/ui_example-monster.png)*


*Figure 3*

- - - -
### Event Log Pane

All the output from the program is displayed in this log box. The most recent encounter in this box is the "active" encounter for the `Show Monster Stats` button.
