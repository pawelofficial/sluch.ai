import logging 
import os 
import yaml 
from pathlib import Path
import os 
import shutil 

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

def purge_dir(directory,inclusive=True):
    """Completely removes all contents of the given directory."""
    if not os.path.exists(directory):
        return  # Directory doesn't exist, nothing to do

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):  
            os.remove(item_path)  # Remove files and symlinks
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)  # Remove directories and their contents
    if inclusive:
        os.rmdir(directory)
        
# deletes everything in given data directory
def make_temp_data_dirs(name=None,purge=False):
    parent_dir = Path(__file__).parent.parent  # Gets the parent directory of the current file
    data_dir=os.path.join(parent_dir,"data")

    if not name:
        name='test_user'
    
    user_dir=os.path.join(data_dir,name)
    if purge:
        purge_dir(user_dir,inclusive=False)

    os.makedirs(user_dir)
    dic={'user_dir':user_dir}
    dirs_list=['01_user_input','02_audio_input','03_audio_slices','04_stt_slices','05_notes','06_audio_recordings','07_user_notes' ]
    for dir in dirs_list:
        new_dir=os.path.join(data_dir,name,dir)
        os.makedirs(new_dir)
        dic[dir]=new_dir
    return dic 
    
# gets fpses of given user directory in data 
def get_user_dirs(name=None):
    try:
        if name is None:
            name='test_user'
        parent_dir = Path(__file__).parent.parent  # Gets the parent directory of the current file
        data_dir=os.path.join(parent_dir,"data")
        user_dir=os.path.join(data_dir,name)
        dirs=os.listdir(user_dir)
        dirs_fps=[os.path.join(user_dir,dir) for dir in dirs]
        dirs_fps.append(user_dir)
        dic={}
        dic['user_dir']=user_dir
        for i,dir in enumerate(dirs):
            dic[dir]=dirs_fps[i]

        return dic
    except Exception as er:
        print(er)
        return {}


        
        
with open( os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.yaml"),  "r") as file:
    CONFIG = yaml.safe_load(file)['CONFIGS']