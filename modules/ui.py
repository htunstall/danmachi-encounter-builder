import tkinter
from tkinter.font import Font
from tkinter.scrolledtext import ScrolledText
#from tkinter import messagebox
#from tkinter import filedialog

import time
import os
import platform

from . import logic

# -----------------------------------------------------------------------------
# Global Variables
# -----------------------------------------------------------------------------
min_width = 600 # Std: 650
min_height = 550
xpad = 3
ixpad = 2
ypad = 4
iypad= 2



# -----------------------------------------------------------------------------
# Write to the logbox
# -----------------------------------------------------------------------------
def log(logbox, message, blank=False, append=None, colour="black", tag_number=0, font="normal", underline=False):
    _user_message = None
    _size = 10
    d_font = Font(family='Consolas', size=_size)
    if not blank:
        _user_message = "{} - {}".format(time.strftime("%H:%M:%S"), message)
    else:
        _user_message = ""
    
    if font == "bold":
        font = Font(family='Consolas', weight="bold", size=_size)
    else:
        font = d_font
    
    # Make the logbox editable
    logbox.config(state = "normal")    
    # Add some text
    tag = "{0}".format(tag_number)
    if not append == None:        
        logbox.insert("end", _user_message,  "default")
        logbox.insert("end", str(append) + "\n", tag)
    else:
        logbox.insert("end", _user_message + "\n", tag)
        
    logbox.tag_config(tag, foreground=colour, underline=underline, font=font)    
    logbox.tag_config("default", foreground="black", font=d_font)
    # Scroll to the end and make the box uneditable
    logbox.see("end")
    logbox.config(state = "disabled")

def build_click(logbox, conf_values, build_values, level, size, floor, drop_chance, cr_zero, dc_easy, dc_rolled):
    conf_values.drop_chance = drop_chance
    build_values.level = level
    build_values.size = size
    build_values.floor = floor
    build_values.cr_zero = cr_zero
    build_values.dc_easy = dc_easy
    build_values.dc_rolled = dc_rolled
    
    logic.build_enc(logbox, conf_values, build_values)

def wipe_log(logbox):
    logbox.delete("1.0")

def update_ui(dc_slider, dc_spinbox, dc_limit):
    dc_slider.configure(to=dc_limit)
    dc_spinbox.configure(to=dc_limit)
    
# -----------------------------------------------------------------------------
# Called procedure
# -----------------------------------------------------------------------------
def show(conf_values, build_values):
    window = tkinter.Tk()
    # Set the master window title
    window.title("DanMachi Encounter Builder - Ver: 0.4-dev - Author: Harry Tunstall")
    # If the system is windows set the icon (as this breaks the linux version)
    system_id = platform.system()
    if system_id == "Windows":
        # Set the .ico from the ui folder
        window.iconbitmap(os.path.abspath(os.path.join(conf_values.paths.data_files, "icon.ico")))
    # Set master window size
    window.minsize(width=min_width, height=min_height)
    #window.resizable(width=False, height=False)
    # Set the size of the larger font
    l_font = Font(family='Helvetica', size=13) # Unlucky for some

    # -------------------------------------------------------------------------
    # Variables
    # -------------------------------------------------------------------------
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
    
    # -------------------------------------------------------------------------
    #  Top Frame
    # -------------------------------------------------------------------------
    top_frame = tkinter.Frame(window)
    top_frame.pack(side="top", anchor="nw", padx=xpad, pady=ypad, ipadx=ixpad, ipady=iypad)
    
    # -------------------------------------------------------------------------
    #  Build Information Frame
    # -------------------------------------------------------------------------
    build_info = tkinter.LabelFrame(top_frame, text="Build Information")
    build_info.pack(side="left", anchor="nw", padx=xpad, pady=ypad, ipadx=ixpad, ipady=iypad)

    floor_frame = tkinter.Frame(build_info)
    floor_frame.pack(side="top", anchor="nw")
    
    # Floor Number
    floor_lb = tkinter.Label(floor_frame, text="Floor: ", pady=ypad)
    floor_lb.pack(side="left")
    floor_box = tkinter.Spinbox(floor_frame, from_=1, to=49, width=2, state="readonly",
                                textvariable=floor, font=l_font)
    floor_box.pack(side="left")
    
    # Drop Chance
    floor_lb = tkinter.Label(floor_frame, text="  Drop Chance: ", pady=ypad)
    floor_lb.pack(side="left")
    floor_box = tkinter.Spinbox(floor_frame, from_=1, to=20, width=2, state="readonly",
                                textvariable=drop_chance, font=l_font)
    floor_box.pack(side="left")
    
    # CR 0 Monsters Check Box
    cr_zero_bt = tkinter.Checkbutton(floor_frame, text="Allow CR 0 Monsters",
                                     variable=cr_zero, onvalue=True, offvalue=False)
    cr_zero_bt.pack(side="left", padx=xpad, pady=ypad-3)
    if build_values.cr_zero == True:
        cr_zero_bt.select()
    else:
        cr_zero_bt.deselect()
    
    # -------------------------------------------------------------------------
    # Difficulty Frame
    # -------------------------------------------------------------------------
    diff_frame = tkinter.LabelFrame(build_info, text="Difficulty")
    diff_frame.pack(side="top", anchor="nw", padx=xpad, fill='x', expand=1)
    
    # DC for Encounter
    diff_frame_slider = tkinter.Frame(diff_frame)
    diff_frame_slider.pack(side="top", anchor="nw", fill='x', expand=1)
    
    dc_easy_lb = tkinter.Label(diff_frame_slider, text="DC for Encounter: ", pady=ypad)
    dc_easy_lb.pack(side="left")
    dc_easy_spin = tkinter.Spinbox(diff_frame_slider, from_=10, to=20, width=2,
                                   state="readonly", textvariable=dc_easy,
                                   font=l_font, command=lambda:update_ui(dc_slider,
                                                                         dc_rolled_spin,
                                                                         dc_easy.get()-1))
    dc_easy_spin.pack(side="left")
    
    # DC Rolled
    dc_rolled_frame = tkinter.Frame(diff_frame)
    dc_rolled_frame.pack(side="top", anchor="nw", fill='x', expand=1)
    
    dc_rolled_lb = tkinter.Label(dc_rolled_frame, text="DC Rolled: ", pady=ypad)
    dc_rolled_lb.pack(side="left")
    dc_rolled_spin = tkinter.Spinbox(dc_rolled_frame, from_=1, to=dc_easy.get()-1,
                                     width=2, state="readonly", textvariable=dc_rolled,
                                     font=l_font)
    dc_rolled_spin.pack(side="left")    
    dc_slider = tkinter.Scale(dc_rolled_frame, from_=1, to=dc_easy.get()-1,
                              variable=dc_rolled, orient=tkinter.HORIZONTAL,
                              length=250, showvalue=False)
    dc_slider.pack(side="left")
    
    # -------------------------------------------------------------------------
    # Party Frame
    # -------------------------------------------------------------------------    
    size_level_frame = tkinter.LabelFrame(build_info, text="Party")
    size_level_frame.pack(side="left", anchor="nw", padx=xpad, pady=ypad)
    
    # Size
    size_lb = tkinter.Label(size_level_frame, text="Size: ", pady=ypad)
    size_lb.pack(side="left")
    size_box = tkinter.Spinbox(size_level_frame, from_=1, to=8, width=2,
                               state="readonly", textvariable=size, font=l_font)
    size_box.pack(side="left", padx=xpad, pady=ypad-3)
    
    # Level
    level_lb = tkinter.Label(size_level_frame, text="level: ")
    level_lb.pack(side="left")
    level_box = tkinter.Spinbox(size_level_frame, from_=1, to=20, width=2,
                                state="readonly", textvariable=level, font=l_font)
    level_box.pack(side="left", padx=xpad, pady=ypad-3)
    
    # ------------------------------------------------------------------------- 
    # Controls Frame
    # -------------------------------------------------------------------------
    master_butons = tkinter.LabelFrame(top_frame, text="Controls")
    master_butons.pack(side="left", anchor="nw", padx=xpad, pady=ypad, ipadx=ixpad, ipady=iypad)
    
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
    build_bt.pack(side="top", anchor="w", padx=xpad, pady=ypad)
    
    # Wipe Log Button
    wipe_lb_bt = tkinter.Button(master_butons, text="Wipe Event Log",
                              command=lambda:wipe_log(logbox))
    wipe_lb_bt.pack(side="top", anchor="w", padx=xpad, pady=ypad)
    
    # -------------------------------------------------------------------------
    #  Event Log Frame
    # -------------------------------------------------------------------------
    log_frame = tkinter.LabelFrame(window, text="Event Log")
    log_frame.pack(side="top", anchor="n", fill="both", expand=1, padx=xpad, pady=ypad)

    # ScrolledText log box
    logbox = tkinter.scrolledtext.ScrolledText(log_frame, undo=True, borderwidth=3, wrap='word', state="disabled")
    logbox.pack(fill="both", expand=1, side="top", padx=xpad, pady=ypad)

    window.mainloop()