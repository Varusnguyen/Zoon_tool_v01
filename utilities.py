import json
import os
import logging


log_dir = 'logs'
logger = logging.getLogger('log')

def read_config(filename):
    """ 
    Read configure from config.json file, including private, pets' id, etc. Return dictionary of the configures
    """
    try:
        with open(filename) as f:
            configs = json.load(f)
        return configs
    except:
        print("Cannot read config file")

def write_tracking(logs):
    """
    Write transaction history to file for tracking
    """
    if isinstance(logs, list):
        logs = "\n".join(log.strip() for log in logs)
    logger.info(logs)

def read_tracking(filename):
    """
    Read from tracking file to play next turn
    """
    with open(os.path.join(os.getcwd(), log_dir, filename), 'r') as f:
        data = f.read()
    return data

def create_tracking_file(filename):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if not os.path.exists(os.path.join(os.getcwd(), log_dir, filename)):
        with open(os.path.join(os.getcwd(), log_dir, filename), 'w') as f:
            f.write("Time,PetID,Fight turn,Fee\n")

def configure_logging(log_dir, log_file):
    logpath = os.path.join(os.getcwd(), log_dir, log_file)
    logger.setLevel(logging.INFO)
    ch = logging.FileHandler(logpath)
    ch.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(ch)