Blockchain A-Z: Build a Blockchain

Basic blockchain with python + flask

requirement:

    $pip install -r requirement.txt


Assuming, 3 boot nodes 

    $export FLASK_APP=basic_flask.py
    $flask --app basic_flask.py run --host=127.0.0.1 --port=6001 --debug
    $flask --app basic_flask.py run --host=127.0.0.1 --port=6002 --debug
    $flask --app basic_flask.py run --host=127.0.0.1 --port=6003 --debug
