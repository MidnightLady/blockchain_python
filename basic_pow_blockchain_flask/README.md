

requirement:

    $pip install -r requirement.txt


Assuming, 3 boot nodes 

    $export FLASK_APP=basic_flask.py
    $flask run --host=127.0.0.1 --port=6001
    $flask run --host=127.0.0.1 --port=6002
    $flask run --host=127.0.0.1 --port=6003
