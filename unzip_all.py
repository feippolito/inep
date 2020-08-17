import zipfile
import os
# with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
#     zip_ref.extractall(directory_to_extract_to)

for root, dirs, files in os.walk(".", topdown = False):
  for f in files:
    if not '.zip' in f:
      continue
    dir_name = 'unzipped/' + f.split('.')[0]
    os.mkdir(dir_name)
    with zipfile.ZipFile(f, 'r') as zip_ref:
      zip_ref.extractall(dir_name)