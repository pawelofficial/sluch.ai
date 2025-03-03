import logging 
import os 
import yaml 
from pathlib import Path
import os 
import shutil 
import pandas as pd 
import random 
import datetime
import string 



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
    permanent_data_dir=os.path.join(parent_dir,"permanent_data")
    permanent_user_dir=os.path.join(permanent_data_dir,name)
    if not os.path.exists(permanent_user_dir):
        os.makedirs(permanent_user_dir)

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
    dic['permanent_user_dir']=permanent_user_dir
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


def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

        
def random_string(length):
    chars = string.ascii_letters + string.digits  # Letters (A-Z, a-z) + Digits (0-9)
    return ''.join(random.choices(chars, k=length))

def make_passwords(N=10,pwd_N=4):
    parent_dir = Path(__file__).parent.parent  # Gets the parent directory of the current file
    csv_fp=os.path.join(parent_dir,"permanent_data","passwords","passwords.csv")
    df=pd.read_csv(csv_fp)
    
    # random string 
    dic={}
    for i in range(N):
        dic['username']=random_string(pwd_N)
        dic['activation_time']=None # datetime.datetime.now() 
        dic['days_ttl']=1
        dic['deactivation_time']=None # dic['activation_time']+datetime.timedelta(days=dic['days_ttl'])
        dic['active']=False
        df.loc[len(df)]=dic
    df.to_csv(csv_fp,index=False)
        
def activate_account(accountname):
    parent_dir = Path(__file__).parent.parent  # Gets the parent directory of the current file
    csv_fp=os.path.join(parent_dir,"permanent_data","passwords","passwords.csv")
    df=pd.read_csv(csv_fp)
    assert accountname in df['username'].values, f"Account {accountname} not found"
    assert accountname !='admin'
    index=df.loc[df['username']==accountname].index[0]
    # check if already active
    if df.loc[index,'active']:
        return
    ts_now=datetime.datetime.now()
    df.loc[index,'active']=True
    df.loc[index,'activation_time']=ts_now
    ttl=int(df.loc[index,'days_ttl'])
    df.loc[index,'deactivation_time']=ts_now + datetime.timedelta(days=ttl)
    df.to_csv(csv_fp,index=False)
    
def check_account_status(accountname):
    parent_dir = Path(__file__).parent.parent  # Gets the parent directory of the current file
    csv_fp=os.path.join(parent_dir,"permanent_data","passwords","passwords.csv")
    df=pd.read_csv(csv_fp)
    assert accountname in df['username'].values, f"Account {accountname} not found"
    assert accountname !='admin'
    index=df.loc[df['username']==accountname].index[0]
    active=df.loc[index,'active']
    if not active:
        return False,None,None
    
    activation_time=df.loc[index,'activation_time']
    deactivation_time=df.loc[index,'deactivation_time']
    assert deactivation_time>datetime.datetime.now()
    return active,activation_time,deactivation_time
    
# checks if days_ttl passed and deactivates accounts 
def refresh_accounts():
    parent_dir = Path(__file__).parent.parent  # Gets the parent directory of the current file
    csv_fp=os.path.join(parent_dir,"permanent_data","passwords","passwords.csv")
    df=pd.read_csv(csv_fp)
    for no,row in df.iterrows():
        if row['active']:
            if row['deactivation_time']<datetime.datetime.now():
                df.loc[no,'active']=False
    df.to_csv(csv_fp,index=False)
    
    
    
        
with open( os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.yaml"),  "r") as file:
    CONFIG = yaml.safe_load(file)['CONFIGS']