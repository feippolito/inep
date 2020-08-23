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
unzipped_path = f'data/unzipped/{subset}/'

if not os.path.exists('data/unzipped/'):
  os.mkdir('data/unzipped/')

if not os.path.exists(unzipped_path):
  os.mkdir(unzipped_path)

zipped_path = f"data/zipped/{subset}"
create_path(unzipped_path)

# walk for in every zipped/{subset} .zip file
for root, dirs, files in os.walk(zipped_path, topdown = False):
  for f in files:
    if not f.endswith('.zip'):
      continue

    # if f is a .zip
    # create subdirectory in unzipped
    try:
      new_dir = os.path.join(unzipped_path,f.split('.')[0])
      create_path(new_dir)

      # path to zipped file
      zip_file = os.path.join(zipped_path,f)
      print(f'unzipping {os.path.join(new_dir, f)}')

      #unzip file | zipped/subset/file.zip -> unzziped/subset/new-dir
      with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(new_dir)

      # delete zipped file
      print(f'Deleting {zip_file}')
      os.remove(zip_file)

    except:
      print(f'Failed {zip_file}')