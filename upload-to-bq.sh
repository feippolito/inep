bq mk --transfer_config       
--target_dataset=superior
--display_name='2010_DM_CURSO'
--schedule='every 24 hours'
--params='{"data_path_template":"gs://inep-superior/2010_DM_CURSO.CSV",     
"destination_table_name_template":"2010_DM_CURSO",     
"file_format":"CSV",  
"ignore_unknown_values":"false",  
"field_delimiter":"|",   
"skip_leading_rows":"1",  
"allow_quoted_newlines":"false",  
"allow_jagged_rows":"false",  
"max_bad_records":"0",  
"delete_source_files":"false"}',
--data_source=google_cloud_storage