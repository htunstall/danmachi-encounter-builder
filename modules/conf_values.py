import configparser
import os

# -----------------------------------------------------------------------------------
#  Only used in this module
# -----------------------------------------------------------------------------------
config = configparser.SafeConfigParser()

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

def get_filename(conf_values):
    filename =  os.path.abspath(os.path.join(conf_values.paths.data_files, "default.ini"))
    return filename

# -----------------------------------------------------------------------------------
# Called Functions
# -----------------------------------------------------------------------------------
def get(section, var_name, conf_values):
    config.read(get_filename(conf_values))
    var = config_section_map(section)[var_name]
    return var

def set(section, option, value, conf_values):
    config.set(section, option, value)
    with open(get_filename(conf_values), 'w') as file:
        config.write(file)

def set_list(section, option, value, conf_values):
    # section, option and value are all list opjects
    for i in range(0, len(section)):
        config.set(section[i], option[i], value[i])
    with open(get_filename(conf_values), 'w') as file:
        config.write(file)