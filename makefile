make vm-setup:
	sudo apt update
	sudo apt-get update
	sudo apt-get install python3.8
	sudo apt install python3-pip
	pip3 install --upgrade pip
	pip3 install -r requirements.txt
	sudo pip3 install patool
	sudo apt install unrar
	gcloud auth login

make superior:
	python3 src/data_pipeline/download_inep.py "superior"
	python3 src/data_pipeline/unzip_downloaded.py "superior"
	python3 src/data_pipeline/unzip_data.py "superior"
	python3 src/data_pipeline/rename_files.py "superior"
	python3 src/data_pipeline/create_populate_bucket_data.py "superior"
	python3 src/data_pipeline/create_populate_bucket_doc.py "superior"
	## python3 src/data_pipeline/create_bq_schemas.py "superior"
	## python3 src/data_pipeline/populate_bq.py "/superior"
	rm -dr data/unzipped/superior

make censo-escolar:
	python3 src/data_pipeline/download_inep.py "censo-escolar"
	python3 src/data_pipeline/unzip_downloaded.py "censo-escolar"
	# python3 src/data_pipeline/unzip_data.py "censo-escolar"
	python3 src/data_pipeline/rename_files.py "censo-escolar"
	# python3 src/data_pipeline/create_populate_bucket_data.py "censo-escolar"
	python3 src/data_pipeline/create_populate_bucket_doc.py "censo-escolar"
	## python3 src/data_pipeline/create_bq_schemas.py "censo-escolar"
	## python3 src/data_pipeline/populate_bq.py "censo-escolar"
	rm -dr data/unzipped/censo-escolar