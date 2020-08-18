import os
import sys
import pandas_gbq
import pandas as pd
from google.oauth2 import service_account

CREDENTIALS   = service_account.Credentials.from_service_account_file('./key/inep-286513-1145bd3494b1.json')
pandas_gbq.context.credentials = CREDENTIALS

PROJECT_ID = 'inep-286513'

try:
  subset = sys.argv[1]
except Exception as e:
  raise ValueError('Subset required')


for dirpath, subdirs, files in os.walk("./unzipped/superior"):
  for f in files:
    if f.endswith('.CSV') or f.endswith('.csv') and (not f[0].isdigit()):
      absolute_path = os.path.join(dirpath, f)
      tablename = f.split('.')[0]
      TABLE = f'{subset}.{tablename}'
      print(TABLE)
      try:
        df = pd.read_csv(absolute_path, nrows=0, sep = '|', encoding = "ISO-8859-1")
          pandas_gbq.to_gbq(df, TABLE,
          project_id=PROJECT_ID,
          credentials=CREDENTIALS,
          if_exists='fail')
      except:
        print(f'Could not create {TABLE}')