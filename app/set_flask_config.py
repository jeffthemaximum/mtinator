def set_flask_config(app):
    app.config.from_object('config.BaseConfig')
