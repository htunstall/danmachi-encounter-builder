import os
import csv
import random

#from tkinter import messagebox

from . import ui
from . import classes

# -----------------------------------------------------------------------------
# Procedures
# -----------------------------------------------------------------------------
def build_enc(logbox, conf_values, build_values):
    monster_list = []
    # Load in data from the *.csv files
    xp_list = load_csv_xp(conf_values)
    xp_conv = load_csv_xp_conversion(conf_values)
    load_csv_monsters(logbox, monster_list, conf_values)
    
    # -------------------------------------------------------------------------
    # Calculate the scaled dificulty
    # -------------------------------------------------------------------------
    # dc_easy is the dc of the encounter roll. Roll under it and an encounter
    #  ensues
    list_diff = [None] * (build_values.dc_easy - 1)
    # XP increment value
    xp_inc = float( (float(xp_list[build_values.level][4]) - 
                    (float(xp_list[build_values.level][1]) * 0.6)) /
                    (float(build_values.dc_easy) - 1))
    # Easy XP for party current level
    list_diff[0] = int(xp_list[build_values.level][1]) 
    # Deadly XP for part current level
    list_diff[build_values.dc_easy-2] = int(xp_list[build_values.level][4])
    # Create the list of scaled dificulties
    for i in range(1, build_values.dc_easy - 2):
        list_diff[i] = int(list_diff[i-1] + xp_inc)
    
    # Reverse the list to have the indexes relate in the corect order
    #  (e.g. 1/9 = Deadly : 9/9 = Easy)
    list_diff = list_diff[::-1]
    total_xp = list_diff[build_values.dc_rolled-1] * build_values.size
    # Text version of the dificulty to print to the user
    t_diff = "{0}/{1}".format(build_values.dc_rolled, build_values.dc_easy-1)
    
    
    # If the Logbox is NOT empty
    if not logbox.compare("end-1c", "==", "1.0"):
        # Send two blank rows to the logbox
        ui.log(logbox, "", blank=True)
        ui.log(logbox, "========================================================")
        ui.log(logbox, "", blank=True)
        
    ui.log(logbox, "", append="{0} Encounter - Total XP: {1}".format(t_diff, total_xp),
           tag_number="title", font="bold", underline=True, show_time=True)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Remove variables not used again
    del (xp_inc, i, t_diff, list_diff)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    # -------------------------------------------------------------------------
    # Buy the monster CR values for the encounter from the total XP
    # -------------------------------------------------------------------------
    # If we're not allowing CR 0, start at index 2 for the cr generation
    start_i = 1 # CR 0 : xp 10    
    if not build_values.cr_zero:    
        start_i = 2 # CR 0.125 : xp 25
    
    # Set buy minimum for later floors
    if build_values.floor >= 5:
        start_i = 3 # Minimum 0.25 CR
    elif build_values.floor >= 8:
        start_i = 3 # This need updating
    
    # Whilst a monster could be added to the encounter
    #  xp_conv[start_i][0] - Either 10 xp (CR 0) or 25 xp (CR 0.125)
    encounter_cr = [] # This is is list of CR
    encounter_mo = [] # This is a list of Monster objects
    while total_xp >= int(xp_conv[start_i][1]):
        highest_cr = None
        # Find the highest possible CR monster avalible
        for i in range(1, len(xp_conv)-1):
            if float(xp_conv[i][1]) > total_xp:
                highest_cr = float(xp_conv[i-1][0])
                highest_cr_i = i - 1
                break
        
        # Limit the highest CR based on the floor we are on. If the encounter
        #  could have a higher CR based purely on total XP
        if  highest_cr > float(conf_values.floor_cr_limits[build_values.floor]):
            highest_cr = float(conf_values.floor_cr_limits[build_values.floor])
            for i in range(1, len(xp_conv)-1):
                if highest_cr == float(xp_conv[i][0]):
                    highest_cr_i = i
                    break
        
        # Pick a random CR monster to buy
        cur_i = random.randint(start_i, highest_cr_i)
        encounter_cr.append(xp_conv[cur_i][0])
        total_xp = total_xp - float(xp_conv[cur_i][1])
    # Sort the encounter monsters from weakest to strongest
    encounter_cr.sort()
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Remove variables not used again
    del (start_i, cur_i, i,
         highest_cr, highest_cr_i,
         total_xp)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
    # -------------------------------------------------------------------------
    # Create a list of monsters that can be used in this encoutner 
    # -------------------------------------------------------------------------
    i_use = set() # Will contain the indexes of the rows to use in monster_list
    for cr in encounter_cr:        
        for i in range(0,len(monster_list)):
            if (monster_list[i].cr in encounter_cr and
                 build_values.floor >= float(monster_list[i].floor_start) and
                 build_values.floor <= float(monster_list[i].floor_end)
                 ):
                i_use.add(i)
    
    # Create a list of tuples, each tuple being the monsters aplicable for the
    #  CR of that position in the list and the CR
    list_of_monsters_per_cr = []
    for cr in encounter_cr:
        list_of_monsters = []
        for i in i_use:
            if monster_list[i].cr == cr:
                list_of_monsters.append(monster_list[i])
        list_of_monsters_per_cr.append(list([list_of_monsters, cr]))
    
    prev_cr = list_of_monsters_per_cr[0][1]
    i_to_remove = []
    cur_cr = None
    for i in range(1, len(list_of_monsters_per_cr)):
        cur_cr = list_of_monsters_per_cr[i][1]
        if cur_cr == prev_cr:
            i_to_remove.append(i)
        else:
            prev_cr = cur_cr
    
    # Reverse the order so when deleting indexes the indexes don't "move"
    i_to_remove.reverse()        
    for i in i_to_remove:
        del list_of_monsters_per_cr[i]
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Remove variables not used again
    del (cr, prev_cr, cur_cr, i, i_to_remove, list_of_monsters)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    # -------------------------------------------------------------------------
    # Select which monsters are in the encounter, based of the bought CR values
    # ------------------------------------------------------------------------- 
    # For each cr in the encounter generate a monster | Weighted
    cr_done = []
    cr_done_i = []
    # For each different CR in the encounter
    for _monster_list, cr in list_of_monsters_per_cr:    
        # =====================================================================    
        # Calculate the weighting for selecting each monster in the list
        # =====================================================================
        monster_weightings = []
        # How many mosters of the current CR are there?
        _monster_list_len = encounter_cr.count(cr)
        for _monster in _monster_list:
            weight = 100 # Default weighting                
            # Remove weight for the distance the monsters are from their
            #  prefered floor
            floor_away = abs(int(build_values.floor) - int(_monster.floor_preference))
            weight = weight - (floor_away * 20)
            
            # Append the weight for this monster
            monster_weightings.append(weight)
        
        # =====================================================================
        # Pick the monsters in the encoutner for this CR
        # =====================================================================
        _k = 1 # _k is the number of monsters to pick: default 1
        num_of_monster1 = None
        num_of_monster2 = None
        if _monster_list_len >= 4:
            # If we have 4 or more monsters of the same CR in the fight
            if _monster_list_len <= 7 and len(_monster_list) >= 2:
                _k = 2
            else:
                # We have 8 or more monsters                
                if len(_monster_list) >= 3:
                    _k = 3
                elif len(_monster_list) == 2:
                    _k = 2
            _choices = random.choices(_monster_list, weights=monster_weightings, k=_k)
            
            # =================================================================
            # Populate the encounter_mo list
            # =================================================================
            if len(_choices) == 1:
                # One type of monster
                for i in range(0, _monster_list_len):
                    encounter_mo.append(_choices[0])
            elif len(_choices) == 2:
                # Two types of monster
                num_of_monster1 = int(_monster_list_len / 2)
                num_of_monster2 = _monster_list_len - num_of_monster1
                # Put monsters 1 into the encounter list
                for i in range(0, num_of_monster1):
                    encounter_mo.append(_choices[0])
                # Put monsters 2 into the encounter list
                for i in range(0, num_of_monster2):
                    encounter_mo.append(_choices[1])
            elif len(_choices) == 3:
                # Three types of monster
                num_of_monster1 = int(_monster_list_len / 3)
                num_of_monster2 = _monster_list_len - (num_of_monster1 * 2)
                # Put monsters 1 & 2 into the encounter list
                for i in range(0, num_of_monster1):
                    encounter_mo.append(_choices[0])
                    encounter_mo.append(_choices[1])
                # Put monsters 3 into the encounter list
                for i in range(0, num_of_monster2):
                    encounter_mo.append(_choices[2])
        else:
            # If we have less than 4 monsters in the battle, pick one
            _choices = random.choices(_monster_list, weights=monster_weightings, k=_k)
            # Put the monsters into the encounter list
            for i in range(0, _monster_list_len):
                encounter_mo.append(_choices[0])
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Remove variables not used again
    del (   monster_weightings, weight, cr_done, cr_done_i,
            _choices, cr, floor_away, list_of_monsters_per_cr,
            _k, _monster_list, _monster_list_len, i, 
            num_of_monster1, num_of_monster2)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    # -------------------------------------------------------------------------
    # Sort the list so monsters of the same CR are listed in alphabetical order
    # ------------------------------------------------------------------------- 
    monster_sublists = []
    sublist = []
    cr_prev = encounter_mo[0].cr
    # Create sublists to sort
    for _monster in encounter_mo:
        # If the cr is the same
        if _monster.cr == cr_prev:            
            sublist.append([_monster, _monster.name])
        else:
            monster_sublists.append(list(sublist))
            sublist.clear()
            sublist.append([_monster, _monster.name])
            cr_prev = _monster.cr
    # Make sure to add the last sublist ot the list of sublists
    monster_sublists.append(list(sublist))
    
    # Sort the sublists by mosnter name
    for _list in monster_sublists:
        _list.sort(key=lambda tup: tup[1])
    
    # Rewrite the monster list in sorted order
    encounter_mo.clear()
    for _list in monster_sublists:
        for monster in _list:
            encounter_mo.append(monster[0])
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Remove variables not used again
    del (monster_sublists, sublist,
         _monster, cr_prev)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # -------------------------------------------------------------------------
    # Ouptut to the user the encounter
    # -------------------------------------------------------------------------
    # Create the set of unique monsters in this encounter (start empty)
    u_mons = set()
    # Print the selected mosters to the console, with a drop chance
    for _monster in encounter_mo:
        u_mons.add(_monster.name)
        _message = "{0:<21} - CR: {1:<6} | Drop: ".format(_monster.name, _monster.cr)
        rnd = random.randint(1, 20)
        if conf_values.drop_chance <= rnd:    
            # You get the drop!
            if _monster.drop != "null":
                # If we know what tie drop item is
                rnd = _monster.drop
            appnd_str = "{:>2}".format(rnd)
            ui.log(logbox, _message, append=appnd_str, colour="green",
                   tag_number=conf_values.tag_number)
            conf_values.tag_number += 1
        else:
            # You don't get the drop
            appnd_str = "{:>2}".format(rnd)
            ui.log(logbox, _message, append=appnd_str, colour="red",
                   tag_number=conf_values.tag_number)
            conf_values.tag_number += 1
    
    # Print the total CR of the fight
    total_cr = float(0)
    for cr in encounter_cr:
        total_cr = total_cr + float(cr)        
    ui.log(logbox, "                Total - CR: ", append="{0}".format(total_cr),
           tag_number=conf_values.tag_number, font="normal")
    
    # Create a dictionary for each monster and initialise the count to zero
    mon_count = dict.fromkeys(u_mons, 0)
    # Calculate the number of each monster in the encounter
    for _monster in encounter_mo:
        mon_count[_monster.name] += 1
    
    str_mon_count = ""
    prev_mon = ""
    column = 0
    # Print the collated number of monsters as a string
    for _monster in encounter_mo:
        _name = _monster.name
        if prev_mon != _name:
            prev_mon = _name
            _count = mon_count[_name]
            if mon_count[_name] > 1:
                _name += "s"
                
            # Create newlines so the output is nicer
            if column > 1: # If we're in the 3rd column go to a new line
                str_mon_count += "\n"
                column = 0
            
            column += 1
            str_mon_count += "| {:<2} {:<23} |".format(_count, _name)
    
    # If we haven't finished a line
    if column != 2:
        # Pad
        str_mon_count += "| {:<2} {:<23} |".format("", "")
    
    ui.log(logbox, "", append="Total Number of Monsters",
           tag_number="title", font="bold", underline=True)
    ui.log(logbox, str_mon_count, append="",
           tag_number=conf_values.tag_number, font="normal")
    conf_values.tag_number += 1
    
    # Set the encounter monsters back to a ui global variable
    #ui.cur_encounter = encounter_mo
    return encounter_mo
    
# -----------------------------------------------------------------------------
# Procedures for File Importing
# -----------------------------------------------------------------------------
# Loads the *.csv info into a list of monster objects
def load_csv_monsters(logbox, monster_list, conf_values):  
    csv_file = os.path.abspath(os.path.join(conf_values.paths.data_files, "monster_database.csv"))
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        lines = list(reader)
        
    for line in lines:
        if not line[0] == "Name":
            monster_list.append(classes.Monster())
            end_i = len(monster_list) - 1
            monster_list[end_i].name = line[0]
            monster_list[end_i].cr = line[1]
            monster_list[end_i].floor_start = line[2].split("-")[0]
            monster_list[end_i].floor_end = line[2].split("-")[1]
            monster_list[end_i].floor_preference = line[3]
            monster_list[end_i].drop = line[4]
            if line[5] == "None":
                line[5] = None    
            monster_list[end_i].reference = line[5]
            
# Loads the *.csv info into a list of CR <--> XP conversions
def load_csv_xp(conf_values):
    csv_file = os.path.abspath(os.path.join(conf_values.paths.data_files, "xp_database.csv"))
    xp_list = None
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        xp_list = list(reader)
    return xp_list

# Loads the *.csv info into a list of XP per player per level for each diff
def load_csv_xp_conversion(conf_values):
    csv_file = os.path.abspath(os.path.join(conf_values.paths.data_files, "xp_conversion.csv"))
    xp_conv = None
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        xp_conv = list(reader)
    return xp_conv