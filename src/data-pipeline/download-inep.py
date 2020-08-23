import os
import sys

try:
  subset = sys.argv[1]
except Exception as e:
  raise ValueError('Pass folder to save as parameter')

with open(os.path.join('data/links',f'{subset}.txt'),'r') as f:
    lines = f.readlines()

for line in lines:
    command = f'wget {line} -P ./data/zipped/{subset}'
    os.system(command)