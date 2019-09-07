from flask import (
    abort,
    request,
)

from application import app, db
from app.extensions.mta_api import get_line_status, stream_and_update_line_statuses
from app.helpers.line_data import all_lines, line_to_feed_id
from app.helpers.service_helpers import SERVICES
from app.helpers.service_thread import ServiceThread
from app.helpers.sqlalchemy_helpers import update_line_and_status
from app.models import Line, Status


@app.route('/status', methods=['GET'])
def status():
    line_name = request.args.get('line')

    if (line_name is None):
        abort(404)

    if (line_name not in all_lines()):
        abort(404)

    status_name = get_line_status(line_name, db)
    update_line_and_status(line_name, status_name, db)

    return {
        'line': line_name,
        'status': status_name
    }


@app.route('/uptime', methods=['GET'])
def uptime():
    line_name = request.args.get('line')

    if (line_name is None):
        abort(404)

    if (line_name not in all_lines()):
        abort(404)

    line = Line.query.filter_by(name=line_name).first()

    if line is None:
        abort(404)

    uptime = format(line.uptime(), '.8f')

    return {
        'line': line_name,
        'uptime': uptime
    }


@app.route('/services', methods=['POST'])
def services():
    data = request.get_json()
    service_name = data.get('name')

    if service_name is None:
        abort(404)

    service_config = SERVICES.get(service_name)

    if service_config is None:
        abort(404)

    if (data['state'] not in service_config['states']):
        abort(404)

    if (data['state'] == 'start'):
        if SERVICES[service_name]['instance'] is None:
            t = ServiceThread(service_config['func'])
            SERVICES[service_name]['instance'] = t

    if (data['state'] == 'stop'):
        if SERVICES[service_name]['instance'] is not None:
            SERVICES[service_name]['instance'].kill.set()
            SERVICES[service_name]['instance'] = None

    return data
