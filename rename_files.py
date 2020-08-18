import os
import sys

try:
  subset = sys.argv[1]
except Exception as e:
  raise ValueError('Pass folder to save as parameter')

for dirpath, subdirs, files in os.walk(f"./unzipped/{subset}"):
    for f in files:
        if f.endswith('.CSV') or f.endswith('.csv') and (not f[0].isdigit()):
            ano = dirpath.split('/')[3].split('_')[-1]
            new_name = f'{ano}_{f}'
            absolute_path = os.path.join(dirpath, f)

            new_absolute_path = os.path.join(dirpath,new_name)
            os.rename(absolute_path, new_absolute_path)