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

class colour:
   purple = "\033[95m"
   cyan = "\033[96m"
   darkcyan = "\033[36m"
   blue = "\033[94m"
   green = "\033[92m"
   yellow = "\033[93m"
   red = "\033[91m"
   bold = "\033[1m"
   underline = "\033[4m"
   end = "\033[0m"