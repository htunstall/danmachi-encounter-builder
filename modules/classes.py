class Monster:
    name             = None
    cr               = None
    floor_start      = None
    floor_end        = None
    floor_preference = None
    drop             = None
    reference        = None

class Paths:
    cwd = None
    data_files = None
    modules = None

class Conf:
    version = "1.1.1"
    tag_number = 1
    solo_chance = None
    drop_chance = None
    floor_cr_limits = [None] * 51
    paths = Paths()

class Build:
    level = 1
    size = 1
    floor = 1
    cr_zero = False
    dc_rolled = 9
    dc_easy = 10
    cur_encounter = None

class Lookup:
    size_to_text = {"T" : "Tiny", "S" : "Small", "M" : "Medium",
                    "L": "Large", "H" : "Huge",  "G" : "Gigantic"}
    value_to_mod = { 1 : "-5",  2 : "-4",  3 : "-4",  4 : "-3",  5 : "-3",  6 : "-2",
                     7 : "-2",  8 : "-1",  9 : "-1", 10 : "+0", 11 : "+0", 12 : "+1",
                    13 : "+1", 14 : "+2", 15 : "+2", 16 : "+3", 17 : "+3", 18 : "+4",
                    19 : "+4", 20 : "+5", 21 : "+5", 22 : "+6", 23 : "+6", 24 : "+7",
                    25 : "+7", 26 : "+8", 27 : "+8", 28 : "+9", 29 : "+9", 30 : "+10"}
    cr_to_xp     = { 0 : 10, 0.125 : 25,  0.25 : 50,   0.5 : 100,   1 : 200,    2 : 450,
                     3 : 700,    4 : 1100,   5 : 1800,   6 : 2300,  7 : 2900,   8 : 3900,
                     9 : 5000,  10 : 5900,  11 : 7200,  12 : 8400, 13 : 10000, 14 : 11500,
                    15 : 13000, 16 : 15000, 17 : 18000, 18 : 20000}