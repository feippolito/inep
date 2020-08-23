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
	python3 src/data-pipeline/download-inep.py "superior"
	python3 src/data-pipeline/unzip-downloaded.py "superior"
	python3 src/data-pipeline/unzip-data.py "superior"
	python3 src/data-pipeline/rename-files.py "superior"
	python3 src/data-pipeline/create-populate-bucket-data.py "superior"
	python3 src/data-pipeline/create-populate-bucket-doc.py "superior"
	# python3 src/data-pipeline/create-bq-schmeas.py "superior"
	# python3 src/data-pipeline/populate-bq.py "superior"
	rm -dr data/unzipped/superior

make censo-escolar:
	python3 src/data-pipeline/download-inep.py "censo-escolar"
	python3 src/data-pipeline/unzip-downloaded.py "censo-escolar"
	python3 src/data-pipeline/unzip-data.py "censo-escolar"
	python3 src/data-pipeline/rename-files.py "censo-escolar"
	python3 src/data-pipeline/create-populate-bucket-data.py "censo-escolar"
	python3 src/data-pipeline/create-populate-bucket-doc.py "censo-escolar"
	# python3 src/data-pipeline/create-bq-schmeas.py "censo-escolar"
	# python3 src/data-pipeline/populate-bq.py "censo-escolar"
	rm -dr data/unzipped/censo-escolar
