import os 
import sys

try:
  subset = sys.argv[1]
except Exception as e:
  raise ValueError('Subset required!')


def create_bucket(PROJECT_ID, BUCKET_LOCATION, BUCKET_NAME):

  command = f'gsutil mb -p {PROJECT_ID} -l {BUCKET_LOCATION} -b on gs://{BUCKET_NAME}'

  os.system(command)
  return command

if __name__ == "__main__":

  PROJECT_ID = 'inep-286513'
  BUCKET_LOCATION = 'SOUTHAMERICA-EAST1'
  BUCKET_NAME = f'{PROJECT_ID}-{subset}-doc'

  print('creating bucket')
  c = create_bucket(PROJECT_ID, BUCKET_LOCATION, BUCKET_NAME)
  print(c)

  print('populating bucket')
  for dirpath, subdirs, files in os.walk(f"./data/unzipped/{subset}"):
    for f in files:
      if f.endswith('.pdf')  or f.endswith('.PDF') or\
         f.endswith('.xlsx') or f.endswith('.XLSX') or\
         f.endswith('.TXT')  or f.endswith('.txt'):
              
        absolute_path = os.path.join(dirpath, f)
        command = f"gsutil cp '{absolute_path}' gs://{BUCKET_NAME}/{f}"
        print(command)
        os.system(command)

        # os.remove(absolute_path)