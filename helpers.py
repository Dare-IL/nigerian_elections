from box import Box
import sys, string, os
import datetime
import pandas as pd

def read_config(config_name: str) -> Box:
    '''
    Read from a file e.g. config.yaml in the current
    directory.

    Args: name of config file (must be .yml or .yaml)
    Returns: Box object of config

    '''
    
    config_path = os.getcwd() + '/' + config_name
    config_file = Box()
    config_file.merge_update(Box.from_yaml(filename=config_path))

    return config_file


def make_data_dirs(start: str, end: str) -> string:   
    '''
    Create data directory for channel
    Args: channel name
    '''  

    # check if data directory exits if not create
    if not os.path.isdir('./data/twitter'):
        os.system("mkdir data")
        os.system("mkdir data/twitter")

    dir = f'./data/twitter/{start}_{end}'

    # check if directory exits if not create
    if not os.path.isdir(dir):
        os.system(f"mkdir {dir}")
    
    return dir

def get_latest_dir():
    '''
    
    ''' 
    dirs = []
    for dir in os.listdir("./data/twitter"):        
        dirs.append(dir)
    
    latest_dir = sorted(dirs)[-1]
    latest_path = f'./data/twitter/{latest_dir}'

    return latest_path