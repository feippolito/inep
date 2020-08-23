import os 
import sys

try:
  subset = sys.argv[1]
except Exception as e:
  raise ValueError('Subset required')

for dirpath, subdirs, files in os.walk(f"./unzipped/{subset}"):
    for f in files:
        if f.endswith('.CSV') or f.endswith('.csv') and (not f[0].isdigit()):

          print(f)

          absolute_path = os.path.join(dirpath, f)

          command =  f'bq mk --transfer_config '
          command += f'--target_dataset=superior ' 
          command += f'--display_name="{f.split(".")[0]}" '
          command += '--params='
          command += "'"
          command += '{"data_path_template":'
          command += f'"gs://inep-{subset}/{f}", '
          command += f'"destination_table_name_template":"{f.split(".")[0]}", '
          command += f'"file_format":"CSV", '
          command += f'"ignore_unknown_values":"false", '
          command += f'"field_delimiter":"|", '
          command += f'"skip_leading_rows":"1", '
          command += f'"allow_quoted_newlines":"false", '
          command += f'"allow_jagged_rows":"false", '
          command += f'"max_bad_records":"0", '
          command += '"delete_source_files":"false"}'
          command += "' "
          command += f'--data_source=google_cloud_storage '

          os.system(command)
          print('\n')