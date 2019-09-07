from app.extensions.mta_api import stream_and_update_line_statuses
from app.helpers.line_data import all_lines

from application import db


def status_service_func():
    stream_and_update_line_statuses(all_lines(), db)

SERVICES = {
    'status': {
        'states': [
            'start',
            'stop'
        ],
        'instance': None,
        'func': status_service_func
    }
}
