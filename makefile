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
	# python3 src/datapipeline/streaming_pipeline.py "superior"
	python3 src/datapipeline/get_schemas.py "superior"

make censo_escolar:
	# python3 src/datapipeline/streaming_pipeline.py "censo_escolar"
	python3 src/datapipeline/get_schemas.py "censo_escolar"