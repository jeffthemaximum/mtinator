from app import create_app

app_data = create_app()

app = app_data['app']
db = app_data['db']
migrate = app_data['migrate']

from app import models, routes
