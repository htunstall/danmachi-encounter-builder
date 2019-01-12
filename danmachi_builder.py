import tkinter
import os

from modules import ui
from modules import conf_values as conf
from modules import classes

ui.version = "0.5.1"
# -----------------------------------------------------------------------------
# Executes when code starts
# -----------------------------------------------------------------------------
# Create a tempory window to house tkinter messageboxes 
root = tkinter.Tk()
root.withdraw()

conf_values  = classes.Conf()
build_values = classes.Build()

conf_values.paths.cwd        = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

print("\nroot dir:", conf_values.paths.cwd, "\n")

if os.path.basename(conf_values.paths.cwd) == "dist":
    print("In dist directory, puling up to the root directory...")
    conf_values.paths.cwd =  os.path.abspath(os.path.join(conf_values.paths.cwd, ".."))
    print("\nroot dir:", conf_values.paths.cwd, "\n")

conf_values.paths.data_files = os.path.join(conf_values.paths.cwd, "data_files")
conf_values.paths.modules    = os.path.join(conf_values.paths.cwd, "modules")

conf_values.solo_chance = int(conf.get("Encounter", "solo_chance", conf_values))
conf_values.drop_chance = int(conf.get("Encounter", "drop_chance", conf_values))
build_values.cr_zero    =     conf.get("Encounter", "cr_zero",     conf_values)

conf_values.floor_cr_limits[4] = int(conf.get("Cr_Limits", "up_to_floor_4",   conf_values))
conf_values.floor_cr_limits[7] = int(conf.get("Cr_Limits", "up_to_floor_7",   conf_values))
conf_values.floor_cr_limits[12] = int(conf.get("Cr_Limits", "up_to_floor_12", conf_values))

# Set the floor limit to the first limit at the end of floor 4
floor_lim = conf_values.floor_cr_limits[4]
# Fill in the rest of the empty list with the correct floor limit
for i in range(1, len(conf_values.floor_cr_limits)):
    if conf_values.floor_cr_limits[i] == None:
        conf_values.floor_cr_limits[i] = floor_lim
    elif conf_values.floor_cr_limits[i] == floor_lim:
        for j in range(i+1, len(conf_values.floor_cr_limits)):
            if not conf_values.floor_cr_limits[j] == None:
                floor_lim = conf_values.floor_cr_limits[j]
                break
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Remove variables not used again
del (i, j, floor_lim)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# remove the temporary window used to show error messages
root.destroy()

ui.show(conf_values, build_values)