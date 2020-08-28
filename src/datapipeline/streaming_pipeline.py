import os
import sys
import re
import shutil
from google.oauth2 import service_account

from os.path import dirname
sys.path.append(dirname(__file__))
from pipe_lib import *


def run_pipeline(link, subset, PROJECT_ID, CREDENTIALS, error, bq_error):
    root_dir = os.path.join('data','unzipped',subset)
    
    skip = False
    try:
        download_inep(link,subset)
        unzip_download(subset)
        unzip_data(subset)
        rename_files(subset)
    except:
        skip = True

    if skip:
        error += [link.split('.')[0].split('/')[-1]]
    else:
        populate_doc_bucket(subset, PROJECT_ID)
        populate_data_bucket(subset, PROJECT_ID)
        bq_error = create_bq_table(subset, PROJECT_ID, CREDENTIALS, bq_error)

    return error, bq_error


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
    
    error, bq_error = [], []

    with open(os.path.join('data/links',f'{subset}.txt'),'r') as f:
        
        lines = f.readlines()
        for link in lines:
        
            zipped_path = os.path.join('data', 'zipped')
            unzipped_path = os.path.join('data', 'unzipped')         
            create_path(zipped_path)
            create_path(unzipped_path)
            create_path(os.path.join(zipped_path, subset))
            create_path(os.path.join(unzipped_path, subset))

            error, bq_error = run_pipeline(link, subset, PROJECT_ID, CREDENTIALS, error, bq_error)
            
            shutil.rmtree(zipped_path)
            shutil.rmtree(unzipped_path)
    
    print('\n\n-------------------')
    print('Links not completed:')
    for e in error:
        print(e)
    print('')
    for e in bq_error:
        print(e)