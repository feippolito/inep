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

    if DATASET_ID == 'superior':
        j = 2
    else:
        j = 1

    print('Reading tables...')
    dataset_ref = client.dataset(DATASET_ID, project=PROJECT_ID)
    my_tables = {}
    total_tables = set()
    for table in tables:
        table_id = table.table_id.replace(' ','_')
        table_ref = dataset_ref.table(table_id)
        table_obj = client.get_table(table_ref)
        columns = [schema.name for schema in table_obj.schema]
        [total_tables.add(col) for col in columns]
        my_tables[table_id] = columns

    my_tables2 = {}
    tables_columns = {}
    has_columns = {}
    for k, i in my_tables.items():
        k_ = k.split('_')[j]
        if k_ not in my_tables2:
            my_tables2[k_] = set()
            tables_columns[k_] = set()
            has_columns[k_] = {}
        my_tables2[k_] = my_tables2[k_] | set([k])
        tables_columns[k_] = tables_columns[k_] | set(i)
        has_columns[k_][k] = i

    for k_ in tables_columns.keys():
        print('Creating DataFrame...')
        df = pd.DataFrame(False, columns = list(tables_columns[k_]),
                                 index = list(my_tables2[k_]))
        for k in has_columns[k_].keys():
            df.loc[k, has_columns[k_][k]] = True

        df = df.reset_index()
        df = df.rename(columns = {'index':'Table_Name'})

        pd_gbq_table = f'table_schemas.{DATASET_ID}_{k_}'
        print(f'Uploadig {pd_gbq_table} to BQ...')
        pandas_gbq.to_gbq(df, pd_gbq_table, project_id=PROJECT_ID, if_exists='replace' )
    print(f'Done!')