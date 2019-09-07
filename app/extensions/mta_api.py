from google.transit import gtfs_realtime_pb2
from urllib.request import urlopen

from app.helpers.line_data import all_lines, line_to_feed_id
from app.helpers.mta_helpers import feed_id_to_url
from app.helpers.object_helpers import multi_getattr
from app.helpers.sqlalchemy_helpers import get_or_create, update_line_and_status


def get_data(feed_id):
    feed = gtfs_realtime_pb2.FeedMessage()
    response = urlopen(feed_id_to_url(feed_id))
    feed.ParseFromString(response.read())
    for entity in feed.entity:
        if entity.HasField('alert'):
            return entity.alert


def get_line_status(line_name, db):
    # TODO refactor "status" var to constant instead of hardcoded string

    feed_id = line_to_feed_id(line_name)
    data = get_data(feed_id)
    status_name = 'not delayed'

    if data is not None:
        if hasattr(data, 'informed_entity'):
            routes = [multi_getattr(datum, 'trip.route_id')
                      for datum in data.informed_entity]
            if line_name in routes:
                status_name = 'delayed'

    return status_name


def stream_and_update_line_statuses(lines, db):
    for line_name in lines:
        status_name = get_line_status(line_name, db)
        update_line_and_status(line_name, status_name, db)
