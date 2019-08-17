"""Setting files processing."""
import configparser


def readConfig(filePath):
    """Converts data from an ini file to dict"""
    config = configparser.ConfigParser()
    config.read(filePath)

    data = {}
    for section in config.sections():
        data[section] = {}
        for option in config.options(section):
            data[section][option] = config.get(section, option)
    return data
