import zipfile
import os
from pyunpack import Archive

rar_files, zip_files = [], []

try:
  subset = sys.argv[1]
except Exception as e:
  raise ValueError('Pass folder to save as parameter')

for dirpath, subdirs, files in os.walk("./unzipped/{subset}"):
  for f in files:
    if f.endswith('.zip'):
      zip_files.append(os.path.join(dirpath, f))
    if f.endswith('.rar'):
      rar_files.append(os.path.join(dirpath, f))

for zip_file in zip_files:
  base_name = os.path.dirname(zip_file)
  with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(base_name)
  os.remove(zip_file)

for rar_file in rar_files:
  base_name = os.path.dirname(rar_file)
  Archive(rar_file).extractall(base_name)
  os.remove(rar_file)