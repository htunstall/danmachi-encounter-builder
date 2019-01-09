import os
import sys

# Define where the modules folder is located and add it to the path
modules_path = os.path.abspath(os.path.join(os.getcwd(), "modules"))
if not sys.path.count(modules_path) >= 1:
    # Add the modules folder to the python enviroment
    sys.path.insert(0, modules_path)
del modules_path

import ui
import conf_values as conf
import classes

# -----------------------------------------------------------------------------
# Execultes when code starts
# -----------------------------------------------------------------------------
conf_values = classes.Conf()
build_values = classes.Build()

conf_values.paths.cwd = os.path.abspath(os.getcwd())
conf_values.paths.data_files = os.path.join(conf_values.paths.cwd, "data_files")
conf_values.paths.modules = os.path.join(conf_values.paths.cwd, "modules")

conf_values.solo_chance = int(conf.get("Encounter", "solo_chance"))
conf_values.drop_chance = int(conf.get("Encounter", "drop_chance"))
build_values.cr_zero = conf.get("Encounter", "cr_zero")

conf_values.floor_cr_limits[4] = int(conf.get("Cr_Limits", "up_to_floor_4"))    
conf_values.floor_cr_limits[7] = int(conf.get("Cr_Limits", "up_to_floor_7"))
conf_values.floor_cr_limits[12] = int(conf.get("Cr_Limits", "up_to_floor_12"))

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
ui.show(conf_values, build_values)