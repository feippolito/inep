import zipfile
import os
import sys

"""
Pass a subset name as an argument

python3 unzip_downloaded.py "subset"

where subset is a directory which contains all the zip files 


/inep/zipped/{subset}/*.zip
"""

def create_path(path):
  if not os.path.exists(path):
    os.mkdir(path)

try:
  subset = sys.argv[1]
except Exception as e:
  raise ValueError('Pass folder to save as parameter')

# create subset folder inside unzipped
base_name = f'unzipped/{subset}/'
create_path(base_name)

# walk for in every zipped/{subset} .zip file
for root, dirs, files in os.walk(f"./zipped/{subset}", topdown = False):
  for f in files:
    print('\n',files,'\n')
    if f.endswith('.zip'):
      continue

  # if f is a .zip
    # create subdirectory in unzipped  
    dir_name = base_name + f.split('.')[:-1]
    create_path(dir_name):
    print(f'unzipping {dir_name}')

    # path to zipped file
    zip_file = f'./zipped/{subset}/{f}'

    #unzip file | zipped/subset/file.zip -> unzziped/subset/new-dir
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
      zip_ref.extractall(dir_name)

    #delete zipped file
    # print(f'Deleting {zip_file}')
    # os.remove(zip_file)