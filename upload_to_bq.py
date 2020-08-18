import os 
import sys

try:
  subset = sys.argv[1]
except Exception as e:
  raise ValueError('Subset required')

for dirpath, subdirs, files in os.walk(f"./unzipped/{subset}"):
    for f in files:
        if f.endswith('.CSV') or f.endswith('.csv') and (not f[0].isdigit()):
            absolute_path = os.path.join(dirpath, f)
            
            
            command = f'gsutil cp {absolute_path} gs://inep-{subset}/{f}'
            os.system(command)