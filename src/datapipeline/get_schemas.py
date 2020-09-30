from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import pandas_gbq
import sys

if __name__ == "__main__":

    PROJECT_ID = 'inep-286513'
    CREDENTIALS = service_account.Credentials.\
                from_service_account_file('./key/inep-286513-1145bd3494b1.json')
    pandas_gbq.context.credentials = CREDENTIALS
    pandas_gbq.context.project = PROJECT_ID

    try:
        subset = sys.argv[1]
    except Exception as e:
        raise ValueError('Pass folder to save as parameter')

    DATASET_ID = subset

    client = bigquery.Client(credentials=CREDENTIALS)

    DATASET_ID = subset
    tables = client.list_tables(DATASET_ID)

    print('Reading tables...')
    dataset_ref = client.dataset(DATASET_ID, project=PROJECT_ID)
    my_tables = {}
    total_tables = set()
    for table in tables:
        table_id = table.table_id
        table_ref = dataset_ref.table(table_id)
        table_obj = client.get_table(table_ref)
        columns = [schema.name for schema in table_obj.schema]
        [total_tables.add(col) for col in columns]
        my_tables[table_id] = columns
    print('Creating DataFrame...')
    df = pd.DataFrame(False, columns = total_tables, index = my_tables.keys())
    for k in my_tables.keys():
        df.loc[k, my_tables[k]] = True

    df = df.reset_index()
    df = df.rename(columns = {'index':'Table_Name'})


    pd_gbq_table = f'table_schemas.{subset}'
    print(f'Uploadig {pd_gbq_table} to BQ...')
    pandas_gbq.to_gbq(df, pd_gbq_table, project_id=PROJECT_ID, if_exists='replace' )
    print(f'Done!')