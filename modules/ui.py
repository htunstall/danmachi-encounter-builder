import tkinter
from tkinter.font import Font
from tkinter.scrolledtext import ScrolledText

import time
import os
import platform
import json


from . import logic
from . import classes

# -----------------------------------------------------------------------------
# Global Variables
# -----------------------------------------------------------------------------
min_width = 675 # Std: 650
min_height = 685
xpad = 3
ixpad = 2
ypad = 4
iypad= 2


#------------------------------------------------------------------------------
# Write to the logbox
#------------------------------------------------------------------------------
def log(logbox, message, blank=False, append=None, colour="black", tag_number=0, font="normal", underline=False, show_time=False):
    """
    This procedure writes the message to the log box, with various controlable options,
      for example, the append feild can append font of a different colour to the same line.
      
    Variable list:
        logbox:      The object that is the ScrolledText widget
        message:     A text string message
        blank:       If True, then then a blank line is printed to the ScrolledText
        append:      If this is not None, then this text string is appended to the end of the
                        message string. The font colour is determined by the colour variable,
                        and if underline is True the appended text is underlined.
        colour:      The colour of the appended text
        tag_number:  This is a unique ID for the appended text, if two IDs match then the
                        formating of the appended strings will be the same
        font:        Is the appended text "normal", "bold" etc.
        underline:   Controls the underline of the appended text
        show_time:   If True, the time will be prepended to the message like so "(HH:MM) "
    """
    _user_message = None
    _size = 10
    d_font = Font(family='Consolas', size=_size)
    if not blank:
        if show_time:
            _user_message = "({}) {}".format(time.strftime("%H:%M"), message)
        else:
            _user_message = message
    else:
        _user_message = ""
    
    if font == "bold":
        font = Font(family='Consolas', weight="bold", size=_size)
    else:
        font = d_font
    
    # Make the logbox editable
    logbox.config(state="normal")    
    # Add some text
    tag = "{0}".format(tag_number)
    if append != None:        
        logbox.insert("end", _user_message,  "default")
        logbox.insert("end", str(append) + "\n", tag)
    else:
        logbox.insert("end", _user_message + "\n", tag)
        
    logbox.tag_config(tag, foreground=colour, underline=underline, font=font)    
    logbox.tag_config("default", foreground="black", font=d_font)
    # Scroll to the end and make the box uneditable
    logbox.see("end")
    logbox.config(state="disabled")

#------------------------------------------------------------------------------

def draw_icon(root, conf_values):
    """
    Set the icon of the window root after checking if we are on a windows machine.
       Since, testing showed that linux machines can't have icons set.
    """
    # If the system is windows set the icon (as this breaks the linux version)
    system_id = platform.system()
    if system_id == "Windows":
        # Set the .ico from the ui folder
        root.iconbitmap(os.path.abspath(os.path.join(conf_values.paths.data_files, "icon.ico")))

#------------------------------------------------------------------------------

def build_click(logbox, conf_values, build_values, level, size, floor, drop_chance, cr_zero, dc_easy, dc_rolled):
    """
    This procedure is called by the build encounter button. It collects all the user set
       data from the ui and assigns it to the build_values class object. Then it invokes
       the build_enc() procedure from the logic.py file. After that, a list of unique 
       monsters for the encouter are made from the returned list of Monster class objects
       and this list is set the the build_values class object.
       
    Variables:
        logbox:       Tkinter ScrolledText widget object.
        conf_values:  A Conf class object.
        build_values: A Build class object.
        
        (The remaining variables are all collected from the user interface. And
            are immediately saved into the build_values calss object.)
    """
    conf_values.drop_chance = drop_chance
    build_values.level      = level
    build_values.size       = size
    build_values.floor      = floor
    build_values.cr_zero    = cr_zero
    build_values.dc_easy    = dc_easy
    build_values.dc_rolled  = dc_rolled
    
    encounter_monsters = logic.build_enc(logbox, conf_values, build_values)
    
    # Create a list of unique encounter monsters
    uniq_mon = []
    # Use a set to determine if the monster has already been added to the 
    #    uniq_mon list.
    set_names = set()
    for monster in encounter_monsters:
        if monster.name in set_names:
            continue
        else:
            uniq_mon.append(monster)
            set_names.add(monster.name)
    
    # Make the uniq_mon list availble ouside of this procedure
    build_values.cur_encounter = uniq_mon

#------------------------------------------------------------------------------

def wipe_log(logbox, build_values):
    """
    Clear the ScrolledText logbox, and set the current encounter list to a NoneType.
    """
    logbox.config(state="normal")
    logbox.delete("1.0", tkinter.END)
    logbox.config(state="disabled")
    
    # Reset encounter
    build_values.cur_encounter = None

#------------------------------------------------------------------------------

def update_ui(dc_slider, dc_spinbox, dc_limit):
    """
    Update the limits for the DC rolled in the uim after the dc spinbox is updated.
    """
    dc_slider.configure(to=dc_limit)
    dc_spinbox.configure(to=dc_limit)

#------------------------------------------------------------------------------

def show_monster_stats_ui(build_values, conf_values):
    """
    This is called by the show monster stats button. This spawns a toplevel window
       containing a button for each monster in the build_values.cur_encounter. If
       it is a NoneType, remind the user they need to build an encounter first!
    """
    # Do we have an encounter
    if build_values.cur_encounter != None:
        top = tkinter.Toplevel()
        top.minsize(width=250, height=25)
        top.resizable(width=False, height=False)
    
        top.title("Select a monster!")
        draw_icon(top, conf_values)

        for monster in build_values.cur_encounter:
            tkinter.Button(top, text=monster.name, padx=4, pady=4, command=lambda i_mon=monster:get_monster(conf_values, i_mon)).pack(side="top", anchor="nw", fill="x", expand=1, padx=xpad, pady=ypad)
    else:
        tkinter.messagebox.showinfo("Info", "You have not got an encoutner built!\nPlease build an encounter then select this button.")

#------------------------------------------------------------------------------

def get_monster(conf_values, o_monster):
    """
    This procedure is invoked by the monster buttons in the select a monster toplevel
       ui. This converts from a Monster class object (used in building the encoutner),
       to the associated monster dictionary loaded from the monster.json file. Then
        the procedure to show the monsters stats to the user is called.
    """
    monster_dict = None
    display = True
    
    json_file = os.path.join(conf_values.paths.data_files, "json", "monsters.json")
    
    if os.path.isfile(json_file):
        with open(json_file, "r", encoding="utf8") as f:
            monsters_list = json.load(f)["monster"]
    else:
        print("Not a file")
        tkinter.messagebox.showwarning("Warning!", "The program has encountered a Tarrasque... and the whole party was TPK'd.\n\n(The monsters.json could not be found. This is a FATAL error, the program is unable to display monster stats!)")
        display = False
        
    if display:
        # If we have a set reference, save searching for the monster
        if o_monster.reference != None:
            print(monsters_list[o_monster.reference])
        else:
            for i, monster_dict in enumerate(monsters_list):
                if monster_dict["name"] == o_monster.name:
                    
                    monster_dict = monsters_list[i]
                    print("Index in list:", i, "| Monster name:", o_monster.name)
                    break
        
        spawn_stats_ui(monster_dict, conf_values)

#------------------------------------------------------------------------------

def hline(root, width):
    """
    Draw a horizontal line on the window "root" of pixel width "width".
    """
    hline = tkinter.Frame(root, width=width, background="black")
    hline.pack(side="top", anchor="nw")

#------------------------------------------------------------------------------
    
def draw_stat(stat, monster, root, position, root_width):
    """
    This procedure draws the stats for the monster stat window. It uses a dictionary
       from the class Lookup to also display the modifier for the numerical stat value.
     
     Variables:
         stat:       A string used to lookupo the stat value from the dictionary monster.
         monster:    A dictionary loaded from the monster.json file. Containing all the 
                        stats to display to the user.
         root:       The window or frame to draw these stat widgets in.
         position:   Which column is the stat located in using the tkinter.object.grid()
                        packing procedure.
         root_width: The width, in pixels, of the root object, so the stats can be evenly
                        spaced across the window/frame.
    """
    lookup = classes.Lookup()
    value    = int(monster[stat])
    pad_width = root_width / 6
    stat_cap = stat[0].upper()+stat[1:]
    
    o_text = tkinter.Label(root, text=stat_cap)
    o_text.grid(row=0, column=position)
    
    o_value_text = tkinter.Label(root, text="{} ({})".format(value, lookup.value_to_mod[value]))
    o_value_text.grid(row=1, column=position)
    
    padding = tkinter.Frame(root, width=pad_width)
    padding.grid(row=2, column=position)

#------------------------------------------------------------------------------

def draw_lineitem(root, root_width, position, dict, key, title, padx, width=500):
    """
    This displays a line of the monsters abilities: e.g. Skills, Languages etc.
    
    Variables:
        root:        The object that the line is being drawn in.
        root_width:  The pixel width of the root object.
        position:    The row the line is being drawn in suing the tkinter.object.grid()
                        packing procedure.
        dict:        The dictionary that contains the lines value to display.
        key:         The key for the value of the line we wish to display.
        title:       The name of the stat to be displayed. i.e what is displayed in column 0.
        padx:        The number of pixels to pad the text by in the x direction.
        width:       The pixel width of the text row (not the title) to determine when
                        to wrap onto the second line
    """
    lookup = classes.Lookup()
    bold_font = Font(weight="bold", size=9)
    #=========================
    # If the key exists
    #=========================
    if key in dict:
        value = dict[key]
        tkinter.Label(root, anchor="ne", text=title, wraplength=root_width - width, font=bold_font).grid(row=position, column=0, sticky="ne", padx=padx)
        
        txt_str = ""
        if type(value) == str:
            #=========================
            # If before the dict value
            #=========================
            if key == "senses":
                txt_str += "{}, ".format(value)
    
            if key == "senses":
                txt_str += "passive perception {}".format(dict["passive"])
            else:
                txt_str += value
                
            #=========================
            # If after the dict value
            #=========================
            if key == "cr":
                if "/" in value:
                    split_value = value.split("/")
                    value = int(split_value[0]) / int(split_value[1])
                txt_str += " ({:,} XP)".format(lookup.cr_to_xp[float(value)])
        else:
            for line in value:
                txt_str += "{}\n".format(line)
    
        tkinter.Label(root, anchor="w", justify="left", text=txt_str, wraplength=width).grid(row=position, column=1, sticky="w", padx=padx)

#------------------------------------------------------------------------------
        
def multiline(root, _list, root_width, padx):
    """
    This procedure invokes multiple lines of teh procedure "draw_lineitem()" for each
       item in the list it is given.
       
    Variables:
        root:       The window/frame the widgets are drawn in.
        _list:      Either a list or dict. If it is a list, each item of the list must
                       be a dictionary containing the keys "name" and "text", simesimilarly
                       if a dict is provided it must also conform to this critera. This list
                       or dict is from the monsters.json file.
        root_width: The width of the root window/frame this is drawn in (in pixels).
        padx:       The number of pixels to pad in the x dicection.
    """
    row = 0
    # If the given list is actually a list of dictionarys
    if type(_list) == list:
        for item in _list:
            draw_lineitem(root, root_width, row, item, "text", "{}: ".format(item["name"]), padx)
            row += 1
    
    # Otehrwise it is just a dictionary
    else:
        draw_lineitem(root, root_width, row, _list, "text", "{}: ".format(_list["name"]), padx)

#------------------------------------------------------------------------------
            
def spawn_stats_ui(monster, conf_values):
    """
    This procedure creates a toplevel item to draw all the monsteer stats contained
       within the "monster" dict, and draws all the relevent information.
       
    Variables:
        monster:     A monster dictionary, loaded from the json file.
        conf_values: A class object Conf.
    """
    lookup = classes.Lookup()
    padx  = 2
    pady  = 2
    master_width = 600
    master_height = 300
    
    top = tkinter.Toplevel()
    # Set master window size
    top.minsize(width=master_width, height=master_height)
    top.resizable(width=False, height=False)
    
    top.title("{} | Monster Stats".format(monster["name"]))
    
    draw_icon(top, conf_values)
        
    #==========================================================================
    # Title Frame
    #==========================================================================
    name_info_pane = tkinter.Frame(top)
    name_info_pane.pack(side="top", anchor="nw")
    
    # Name
    mon_name_text = tkinter.Label(name_info_pane, text=monster["name"], font=("Helvetica", 16))
    mon_name_text.pack(side="top", anchor="nw", padx=padx, pady=pady)
    
    # Size and alignment 
    mon_size_align = tkinter.Label(name_info_pane, text="{} {}, {}".format(lookup.size_to_text[monster["size"]], monster["type"], monster["alignment"]))
    mon_size_align.pack(side="top", anchor="nw", padx=padx, pady=pady)
    
    # Seperator
    hline(top, master_width)

    
    #==========================================================================
    # AC, HP & Speed
    #==========================================================================
    ac_etc_pane = tkinter.Frame(top)
    ac_etc_pane.pack(side="top", anchor="nw", padx=padx, pady=pady)
    
    # AC
    draw_lineitem(ac_etc_pane, master_width, 0, monster, "ac", "Armor Class:", padx)
    
    # HP
    draw_lineitem(ac_etc_pane, master_width, 1, monster, "hp", "Hit Points:", padx)
   
    # Speed
    draw_lineitem(ac_etc_pane, master_width, 2, monster, "speed", "Speed:", padx)
    
    # Seperator
    hline(top, master_width)
    
    
    #==========================================================================
    # Stats
    #==========================================================================
    stats_pane = tkinter.Frame(top)
    stats_pane.pack(side="top", anchor="nw", padx=padx, pady=pady)
    
    draw_stat("str", monster, stats_pane, 0, master_width)
    draw_stat("dex", monster, stats_pane, 1, master_width)
    draw_stat("con", monster, stats_pane, 2, master_width)
    draw_stat("int", monster, stats_pane, 3, master_width)
    draw_stat("wis", monster, stats_pane, 4, master_width)
    draw_stat("cha", monster, stats_pane, 5, master_width)
    
    # Seperator
    hline(top, master_width)
    
    
    #==========================================================================
    # Info
    #==========================================================================
    info_pane = tkinter.Frame(top)
    info_pane.pack(side="top", anchor="nw", padx=padx, pady=pady)
    
    # Skills
    draw_lineitem(info_pane, master_width, 0, monster, "skill", "Skills:", padx)
    
    # Senses
    draw_lineitem(info_pane, master_width, 1, monster, "senses", "Senses:", padx)
    
    # Senses
    draw_lineitem(info_pane, master_width, 2, monster, "languages", "Languages:", padx)
    
    # CR
    draw_lineitem(info_pane, master_width, 3, monster, "cr", "Combat Rating:", padx)
    
    # Seperator
    hline(top, master_width)
    
    
    #==========================================================================
    # Attacks
    #==========================================================================
    attack_pane = tkinter.Frame(top)
    attack_pane.pack(side="top", anchor="nw", padx=padx, pady=pady)
    
    if "trait" in monster:
        multiline(attack_pane, monster["trait"], master_width, padx)
    
    # Seperator
    hline(top, master_width)
    
    
    #==========================================================================
    # Actions
    #==========================================================================
    actions_pane = tkinter.Frame(top)
    actions_pane.pack(side="top", anchor="nw", padx=padx, pady=pady)
    
    if "action" in monster:
        multiline(actions_pane, monster["action"], master_width, padx)
    
    # Seperator
    hline(top, master_width)
    
    
# -----------------------------------------------------------------------------
#  Called procedure
# -----------------------------------------------------------------------------
def show(conf_values, build_values):
    """
    Invoked from the main python file danmachi_builder.py to draw the master tkinter window.
    
    Variables:
        conf_values:  A Conf class object.
        build_values: A Build class object.
    """
    window = tkinter.Tk()
    # Set the master window title (N.B: version is set from the danmachi_builder.py file)
    window.title("DanMachi Encounter Builder - Ver: {} - Author: Harry Tunstall".format(conf_values.version))
    
    draw_icon(window, conf_values)
        
    # Set master window size
    window.minsize(width=min_width, height=min_height)
    window.resizable(width=True, height=True)
    # Set the size of the larger font
    l_font = Font(family='Helvetica', size=13) # Unlucky for some


    #--------------------------------------------------------------------------
    # Tkinter Variables
    #--------------------------------------------------------------------------
    floor = tkinter.IntVar() # Party level
    size = tkinter.IntVar() # Party size
    level = tkinter.IntVar() # Party level
    drop_chance = tkinter.IntVar() # number at which drops occour
    drop_chance.set(conf_values.drop_chance)
    cr_zero = tkinter.BooleanVar() # Are we haveing CR 0 monsters
    cr_zero.set(build_values.cr_zero)
    dc_easy = tkinter.IntVar() # DC at whcih monsters dont spawn
    dc_easy.set(build_values.dc_easy)
    dc_rolled = tkinter.IntVar() # number at which drops occour
    dc_rolled.set(build_values.dc_rolled)
    
    
    #--------------------------------------------------------------------------
    # Top Frame
    #--------------------------------------------------------------------------
    top_frame = tkinter.Frame(window)
    top_frame.pack(side="top", anchor="w", padx=xpad, pady=ypad, ipadx=ixpad, ipady=iypad)
    
    #--------------------------------------------------------------------------
    # Build Information Frame
    #--------------------------------------------------------------------------
    build_info = tkinter.LabelFrame(top_frame, text="Build Information")
    build_info.pack(side="top", anchor="w", padx=xpad, pady=ypad, ipadx=ixpad, ipady=iypad)

    #--------------------------------------------------------------------------
    # Dungeon Information Frame
    #--------------------------------------------------------------------------
    floor_frame = tkinter.LabelFrame(build_info, text="Dungeon")
    floor_frame.grid(row=0, column=0, padx=xpad, pady=ypad)
    
    # Floor Number
    floor_lb = tkinter.Label(floor_frame, text="Floor: ", pady=ypad)
    floor_lb.pack(side="left")
    floor_box = tkinter.Spinbox(floor_frame, from_=1, to=49, width=2, state="readonly",
                                textvariable=floor, font=l_font)
    floor_box.pack(side="left")
    
    # CR 0 Monsters Check Box
    cr_zero_bt = tkinter.Checkbutton(floor_frame, text="Allow CR 0 Monsters",
                                     variable=cr_zero, onvalue=True, offvalue=False)
    cr_zero_bt.pack(side="left", padx=xpad, pady=ypad-3)
    if build_values.cr_zero == True:
        cr_zero_bt.select()
    else:
        cr_zero_bt.deselect()
    
    #--------------------------------------------------------------------------
    # Party Frame
    #--------------------------------------------------------------------------    
    party_frame = tkinter.LabelFrame(build_info, text="Party")
    party_frame.grid(row=0, column=1, padx=xpad, pady=ypad)
    
    # Size
    size_lb = tkinter.Label(party_frame, text="Size: ", pady=ypad)
    size_lb.pack(side="left")
    size_box = tkinter.Spinbox(party_frame, from_=1, to=8, width=2,
                               state="readonly", textvariable=size, font=l_font)
    size_box.pack(side="left", padx=xpad, pady=ypad-3)
    
    # Level
    level_lb = tkinter.Label(party_frame, text="level: ")
    level_lb.pack(side="left")
    level_box = tkinter.Spinbox(party_frame, from_=1, to=20, width=2,
                                state="readonly", textvariable=level, font=l_font)
    level_box.pack(side="left", padx=xpad, pady=ypad-3)
    
    # Drop Chance
    drop_chance_lb = tkinter.Label(party_frame, text="  Drop Chance: ", pady=ypad)
    drop_chance_lb.pack(side="left")
    drop_chance_box = tkinter.Spinbox(party_frame, from_=1, to=20, width=2, state="readonly",
                                textvariable=drop_chance, font=l_font)
    drop_chance_box.pack(side="left", padx=xpad, pady=ypad-3)
    
    #--------------------------------------------------------------------------
    # Difficulty Frame
    #--------------------------------------------------------------------------
    diff_frame = tkinter.LabelFrame(build_info, text="Difficulty")
    diff_frame.grid(row=1, column=0, columnspan=2, padx=xpad, sticky="w")
    
    # DC Encounter
    dc_easy_lb = tkinter.Label(diff_frame, text="DC for Encounter: ", pady=ypad)
    dc_easy_lb.grid(row=0, column=0, sticky="e")
    dc_easy_spin = tkinter.Spinbox(diff_frame, from_=10, to=20, width=2,
                                   state="readonly", textvariable=dc_easy,
                                   font=l_font, command=lambda:update_ui(dc_slider,
                                                                         dc_rolled_spin,
                                                                         dc_easy.get()-1))
    dc_easy_spin.grid(row=0, column=1)
    
    # DC Rolled    
    dc_rolled_lb = tkinter.Label(diff_frame, text="DC Rolled: ", pady=ypad)
    dc_rolled_lb.grid(row=1, column=0, sticky="e")
    dc_rolled_spin = tkinter.Spinbox(diff_frame, from_=1, to=dc_easy.get()-1,
                                     width=2, state="readonly", textvariable=dc_rolled,
                                     font=l_font)
    dc_rolled_spin.grid(row=1, column=1)    
    dc_slider = tkinter.Scale(diff_frame, from_=1, to=dc_easy.get()-1,
                              variable=dc_rolled, orient=tkinter.HORIZONTAL,
                              length=200, showvalue=False)
    dc_slider.grid(row=1, column=2, sticky="e")
    
    
    #-------------------------------------------------------------------------- 
    # Controls Frame
    #--------------------------------------------------------------------------
    master_butons = tkinter.LabelFrame(window, text="Controls")
    master_butons.pack(side="top", anchor="w", padx=xpad, pady=ypad, ipadx=ixpad, ipady=iypad)
    
    # Build Button
    build_bt = tkinter.Button(master_butons, text="Build Encounter",
                              command=lambda:build_click(logbox,
                                                         conf_values,
                                                         build_values,
                                                         level.get(),
                                                         size.get(),
                                                         floor.get(),
                                                         drop_chance.get(),
                                                         cr_zero.get(),
                                                         dc_easy.get(),
                                                         dc_rolled.get()))
    build_bt.pack(side="left", anchor="w", padx=xpad, pady=ypad)
    
    # Wipe Log Button
    wipe_lb_bt = tkinter.Button(master_butons, text="Wipe Event Log",
                              command=lambda:wipe_log(logbox, build_values))
    wipe_lb_bt.pack(side="left", anchor="w", padx=xpad, pady=ypad)
    
    # Show monster stats Button
    wipe_lb_bt = tkinter.Button(master_butons, text="Show Monster Stats",
                              command=lambda:show_monster_stats_ui(build_values, conf_values))
    wipe_lb_bt.pack(side="left", anchor="w", padx=xpad, pady=ypad)
    
    #--------------------------------------------------------------------------
    # Event Log Frame
    #--------------------------------------------------------------------------
    log_frame = tkinter.LabelFrame(window, text="Event Log")
    log_frame.pack(side="top", anchor="w", fill="both", expand=1, padx=xpad, pady=ypad, ipadx=ixpad, ipady=iypad)

    # ScrolledText log box
    logbox = ScrolledText(log_frame, undo=True, borderwidth=3, wrap='word', state="disabled")
    logbox.pack(fill="both", expand=1, side="top", padx=xpad, pady=ypad)

    window.mainloop()