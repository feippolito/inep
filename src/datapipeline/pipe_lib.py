import zipfile
import os
import sys
from pyunpack import Archive
import zipfile
import re
from google.cloud import bigquery

def create_path(path):
    if not os.path.exists(path):
        os.mkdir(path)

def download_inep(link, subset):
  command = f'wget {link} -P ./data/zipped/{subset}'
  os.system(command)
  os.system(f'mv *.zip ./data/zipped/{subset}')

def unzip_download(subset):
  unzipped_path = os.path.join('data','unzipped', subset)
  zipped_path = os.path.join('data','zipped', subset)

  # walk for in every zipped/{subset} .zip file
  for root, dirs, files in os.walk(zipped_path):
    for f in files:
      if not f.endswith('.zip'):
        continue

      # if f is a .zip
      # create subdirectory in unzipped
      new_dir = os.path.join(unzipped_path,f.split('.')[0])
      create_path(new_dir)

      # path to zipped file
      zip_file = os.path.join(zipped_path,f)
      print(f'unzipping {os.path.join(new_dir, f)}')
      
      try:
        #unzip file | zipped/subset/file.zip -> unzziped/subset/new-dir
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
          zip_ref.extractall(new_dir)

        # delete zipped file
        print(f'Deleting {zip_file}')
        os.remove(zip_file)

      except:
        print(f'Failed {zip_file}')

def unzip_data(subset):
  rar_files, zip_files = [], []
  unzipped_path = os.path.join('data','unzipped', subset)
  for dirpath, subdirs, files in os.walk(unzipped_path):
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

def rename_files(subset):
  unzipped_path = os.path.join('data','unzipped', subset)
  for dirpath, subdirs, files in os.walk(unzipped_path):
    for f in files:
      ano = dirpath.split('/')[3].split('_')[-1]
      if (f.endswith('.CSV')  or f.endswith('.csv') or  \
          f.endswith('.pdf')  or f.endswith('.PDF') or  \
          f.endswith('.xlsx') or f.endswith('.XLSX') or \
          f.endswith('.xls') or f.endswith('.XLS') or   \
          f.endswith('.TXT')  or f.endswith('.txt')) and (not f.startswith(f'{ano}_') ):
        fname, extension = f.split('.')
        fname = re.sub('[^A-Za-z0-9-_-]+', '', fname)
        new_name = f'{ano}_{fname}.{extension}'.replace(' ','').encode("ascii", "ignore").decode()
        absolute_path = os.path.join(dirpath, f)

        new_absolute_path = os.path.join(dirpath,new_name)
        os.rename(absolute_path, new_absolute_path)

def create_bucket(subset, PROJECT_ID, BUCKET_LOCATION = 'SOUTHAMERICA-EAST1'):
  BUCKET_NAME = f'{PROJECT_ID}-{subset}'
  doc_command = f'gsutil mb -p {PROJECT_ID} -l {BUCKET_LOCATION} -b on gs://{BUCKET_NAME}-doc'
  command = f'gsutil mb -p {PROJECT_ID} -l {BUCKET_LOCATION} -b on gs://{BUCKET_NAME}'
  print(f'creating bucket {BUCKET_NAME}')
  
  os.system(command)
  os.system(doc_command)

def populate_doc_bucket(subset, PROJECT_ID):
  unzipped_path = os.path.join('data','unzipped', subset)
  BUCKET_NAME = f'{PROJECT_ID}-{subset}-doc'
  print(f'populating bucket {BUCKET_NAME}')
  for dirpath, subdirs, files in os.walk(unzipped_path):
    for f in files:
      if f.endswith('.xls')  or f.endswith('.XLS')  or \
         f.endswith('.pdf')  or f.endswith('.PDF')  or \
         f.endswith('.xlsx') or f.endswith('.XLSX') or \
         f.endswith('.TXT')  or f.endswith('.txt'):
              
        absolute_path = os.path.join(dirpath, f)
        command = f"gsutil cp '{absolute_path}' gs://{BUCKET_NAME}/{f}"
        os.system(command)

def populate_data_bucket(subset, PROJECT_ID):
  BUCKET_NAME = f'{PROJECT_ID}-{subset}'
  unzipped_path = os.path.join('data','unzipped', subset)
  print(f'populating bucket {BUCKET_NAME}')
  for dirpath, subdirs, files in os.walk(unzipped_path):
    for f in files:
      if f.endswith('.CSV') or f.endswith('.csv') and (not f[0].isdigit()):
              
        absolute_path = os.path.join(dirpath, f)
        print(f'uploading {f}')
        command = f'gsutil cp {absolute_path} gs://{PROJECT_ID}-{subset}/{f}'
        os.system(command)

def create_bq_table(subset, PROJECT_ID, CREDENTIALS, bq_error):
  client = bigquery.Client(project=PROJECT_ID, credentials=CREDENTIALS)
  unzipped_path = os.path.join('data','unzipped', subset)
  for dirpath, subdirs, files in os.walk(unzipped_path):
    for filename in files:
      if filename.endswith('.CSV') or \
         filename.endswith('.csv') and \
         (not filename[0].isdigit()):
        table_id = f"{PROJECT_ID}.{subset}.{filename.split('.')[0]}"

        job_config = bigquery.LoadJobConfig(
            autodetect=True, source_format=bigquery.SourceFormat.CSV,
            encoding='ISO-8859-1')

        uri = f"gs://{PROJECT_ID}-{subset}/{filename}"

        print(uri , ' -> ', table_id)
        try:
          load_job = client.load_table_from_uri(
              uri, table_id, job_config=job_config)
          load_job.result()  # Waits for the job to complete.
          destination_table = client.get_table(table_id)
          print("Loaded {} rows.".format(destination_table.num_rows))
        except:
          bq_error += [table_id]

  return bq_error

def create_bq_dataset(subset, PROJECT_ID, CREDENTIALS,
                      DATASET_LOCATION='SOUTHAMERICA-EAST1'):
                      
  client = bigquery.Client(project=PROJECT_ID, credentials=CREDENTIALS)
  dataset_id = f"{client.project}.{subset}"
  dataset = bigquery.Dataset(dataset_id)
  dataset.location = DATASET_LOCATION
  try:
    dataset = client.create_dataset(dataset, timeout=30)  # Make an API request.
    print("Created dataset {}.{}".format(client.project, dataset.dataset_id))
  except Exception as e:
    print(f'{dataset_id} already exists')