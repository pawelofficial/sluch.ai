import logging 
import os 
import yaml 

def setup_logger(name,mode='w',fp=None):
    # Create a custom logger
    if fp is None:
        raise ValueError("Please provide a file path")
    logger = logging.getLogger(name)

    # Set the level of logger to INFO
    logger.setLevel(logging.INFO)

    # Create handlers
    c_handler = logging.StreamHandler()

    f_handler = logging.FileHandler(fp,mode)

    # Set level of handlers to INFO
    c_handler.setLevel(logging.ERROR)
    f_handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(format)
    f_handler.setFormatter(format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger

def purge_dir(fp):
    print(f'purging {fp}')
    for f in os.listdir(fp):
        os.remove(os.path.join(fp, f))
        
        
with open( os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.yaml"),  "r") as file:
    CONFIG = yaml.safe_load(file)['CONFIGS']