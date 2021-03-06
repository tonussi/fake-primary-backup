import json
from flask import Flask
from flask import request
from flask import jsonify
from model.primary_backup import PrimaryBackup
from service.health_check_service import HealthCheckService
from service.replica_writer_service import ReplicaWriterService
from service.data_source_writer_service import DataSourceWriterService

app = Flask(__name__)


@app.route('/', methods=['GET'])
def base_url():
    """Base url to test API. Here its possible to directly check the health of the backups"""
    response = HealthCheckService().perform()
    return jsonify(response)


@app.route('/db', methods=['POST'])
def send_data_to_file():
    """URL for registering data."""
    db_new_inserts = json.loads(request.data)["inserts"]
    response = DataSourceWriterService().perform(db_new_inserts)
    return jsonify(response)


@app.route('/rep', methods=['POST'])
def send_data_to_replica():
    """URL for registering data."""
    db_new_inserts = json.loads(request.data).get("inserts", [])
    which_replica = json.loads(request.data).get("which_replica", None)

    response = {}

    if which_replica:
        response = ReplicaWriterService(which_replica).perform(db_new_inserts)
    else:
        response = DataSourceWriterService().perform(db_new_inserts)

    return jsonify(response)


@app.route('/pb', methods=['POST'])
def start_primary_backup():
    """URL for registering data."""
    response = PrimaryBackup().perform()
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
