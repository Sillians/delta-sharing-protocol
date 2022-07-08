install:
	# install dependencies
	pip install --upgrade pip && \
		pip3 install -r requirements.txt    

# black is the uncompromising python code formatter, used to control over minutiae of hand-formatting.
format:
	black *.py

# pylint is a python static code analysis tool which looks for programming errors, helps enforcing a coding standard
lint: 
	pylint --disable=R,C delta_share.py

start_server:
	./delta-sharing-server-0.4.0/bin/delta-sharing-server -- --config ./delta-sharing-server-0.4.0/conf/delta-sharing-server.yaml


all: install format lint start_server
