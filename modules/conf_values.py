import configparser
import os

# -----------------------------------------------------------------------------------
#  Only used in this module
# -----------------------------------------------------------------------------------
config = configparser.SafeConfigParser()
# This SHOULD never change...
filename =  os.path.abspath(os.path.join(os.getcwd(), "data_files", "default.ini"))

def config_section_map(section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

# -----------------------------------------------------------------------------------
# Called Functions
# -----------------------------------------------------------------------------------
def get(section, var_name):
    config.read(filename)
    var = config_section_map(section)[var_name]
    return var

def set(section, option, value):
    config.set(section, option, value)
    with open(filename, 'w') as file:
        config.write(file)

def set_list(section = [], option = [], value = []):
    for i in range(0, len(section)):
        config.set(section[i], option[i], value[i])
    with open(filename, 'w') as file:
        config.write(file)