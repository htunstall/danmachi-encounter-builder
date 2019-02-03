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

### Opening a `PYTHONPATH` command prompt
1. After installing Anaconda3 (https://www.anaconda.com/download/) open the anaconda navigator
2. follow the steps in the screenshot below:

![alt text](https://raw.githubusercontent.com/htunstall/danmachi-encounter-builder/master/documentation/images/anaconda-navigator-open-teminal.png)

3. Great! You have a command prompt with the correct `PYTHONPATH` open

## Example UI

![alt text](https://raw.githubusercontent.com/htunstall/danmachi-encounter-builder/master/documentation/images/example_ui.png)

## Known Bugs

- None
