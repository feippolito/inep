import zipfile
import os
import sys
from pyunpack import Archive

rar_files, zip_files = [], []

try:
  subset = sys.argv[1]
except Exception as e:
  raise ValueError('Subset required!')


if __name__ == "__main__":
  for dirpath, subdirs, files in os.walk(f"data/unzipped/{subset}"):
    for f in files:
      if f.endswith('.zip'):
        zip_files.append(os.path.join(dirpath, f))
      if f.endswith('.rar'):
        rar_files.append(os.path.join(dirpath, f))

  print('total zip: ',len(zip_files))
  for zip_file in zip_files:
    base_name = os.path.dirname(zip_file)
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
          zip_ref.extractall(base_name)
    os.remove(zip_file)

  print('total rar: ',len(rar_files))
  for rar_file in rar_files:
    base_name = os.path.dirname(rar_file)
    Archive(rar_file).extractall(base_name)
    os.remove(rar_file)