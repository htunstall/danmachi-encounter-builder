# DanMachi Encounter Builder

This tool can be used in conjunction with the information located here (https://sites.google.com/site/danmachidnd/) to run a D&D 5th edition campaign.

## Use

The `data_files` directory contains the configuration file `default.ini` and the `monster_database` files, which you can edit to adjust the settings if the program. The other two files `xp_conversion` and `xp_database` should not need editing as they draw there values from the dungeon masters guide and other official sources.

Run the `danmachi_builder.py` file to start the program. This program has been developed using anaconda3 (https://www.anaconda.com/download/) however the dependencies are far less than what are included in anaconda:

- `os`
- `time`
- `random`
- `configparser`
- `csv`
- `tkinter`
- `platform`

## Example UI

![alt text](https://raw.githubusercontent.com/htunstall/danmachi-encounter-builder/master/documentation/images/example_ui.png)

## Known Bugs

- The wipe event log button doesn't wipe the event log
