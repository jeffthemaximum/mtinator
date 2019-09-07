from flask import current_app


def feed_id_to_url(feed_id):
    key = current_app.config['MTA_API_KEY']
    url = f"http://datamine.mta.info/mta_esi.php?key={key}&feed_id={feed_id}"
    return url
