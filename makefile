make superior:
	chmod +x data/zipped/superior/donwload.sh
	data/zipped/superior/donwload.sh

	mv *.zip data/zipped/superior/

	python3 src/data-pipeline/unzip-downloaded.py "superior"
	python3 src/data-pipeline/unzip-data.py "superior"
	python3 src/data-pipeline/rename-files.py "superior"
	python3 src/data-pipeline/create-populate-bucket.py "superior"
	rm -d data/unzipped/superior

make censo-escolar:
	chmod +x data/zipped/censo-escolar/donwload.sh
	data/zipped/censo-escolar/donwload.sh

	timeout 3

	mv *.zip data/zipped/censo-escolar/

	python3 src/data-pipeline/unzip-downloaded.py "censo-escolar"
	python3 src/data-pipeline/unzip-data.py "censo-escolar"
	python3 src/data-pipeline/rename-files.py "censo-escolar"
	python3 src/data-pipeline/create-populate-bucket.py "censo-escolar"
	rm -dr data/unzipped/censo-escolar
