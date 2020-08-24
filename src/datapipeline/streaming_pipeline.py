import os
import sys
import re
import shutil
from google.oauth2 import service_account

from os.path import dirname
sys.path.append(dirname(__file__))
from pipe_lib import *


def run_pipeline(link, subset, PROJECT_ID, CREDENTIALS):
    root_dir = os.path.join('data','unzipped',subset)

    download_inep(link,subset)
    unzip_download(subset)
    unzip_data(subset)
    rename_files(subset)
    populate_doc_bucket(subset, PROJECT_ID)
    populate_data_bucket(subset, PROJECT_ID)
    create_bq_table(subset, PROJECT_ID, CREDENTIALS)

def create_path(path):
    if not os.path.exists(path):
        os.mkdir(path)

if __name__ == "__main__":
    
    PROJECT_ID = 'inep-286513'
    CREDENTIALS   = service_account.Credentials.\
                    from_service_account_file('./key/inep-286513-1145bd3494b1.json')
    
    try:
        subset = sys.argv[1]
    except Exception as e:
        raise ValueError('Pass folder to save as parameter')

    create_bq_dataset(subset, PROJECT_ID, CREDENTIALS)
    create_bucket(subset, PROJECT_ID)

    with open(os.path.join('data/links',f'{subset}.txt'),'r') as f:
        
        create_path(os.path.join('data', 'zipped'))
        create_path(os.path.join('data', 'unzipped'))
        create_path(os.path.join('data', 'zipped', subset))
        create_path(os.path.join('data', 'unzipped', subset))

        lines = f.readlines()
        for link in lines:
            run_pipeline(link, subset, PROJECT_ID, CREDENTIALS)

        shutil.rmtree(os.path.join('data', 'zipped' ))
        shutil.rmtree(os.path.join('data', 'unzipped' ))

