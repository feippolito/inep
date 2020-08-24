import os
import sys
import re

try:
  subset = sys.argv[1]
except Exception as e:
  raise ValueError('Pass folder to save as parameter')


for dirpath, subdirs, files in os.walk(f"./data/unzipped/{subset}"):
  for f in files:
    if f.endswith('.CSV')  or f.endswith('.csv') or\
       f.endswith('.pdf')  or f.endswith('.PDF') or\
       f.endswith('.xlsx') or f.endswith('.XLSX') or\
       f.endswith('.TXT')  or f.endswith('.txt'):

      ano = dirpath.split('/')[4].split('_')[-1]
      fname, extension = f.split('.')
      fname = re.sub('[^A-Za-z0-9]+', '', fname)
      new_name = f'{ano}_{fname}.{extension}'.replace(' ','').encode("ascii", "ignore").decode()
      absolute_path = os.path.join(dirpath, f)

      new_absolute_path = os.path.join(dirpath,new_name)
      os.rename(absolute_path, new_absolute_path)