from flask import Flask

def create_app():
    """ Создаем основное приложение """
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():
        from .views import view
        from .filters import _slice
        from .database import DataBase

        # REGISTER ROUTES
        app.register_blueprint(view, url_prefix='/')

        # REGISTER CONTEXT PROCESSOR
        @app.context_processor
        def slice():
            return dict(slice=_slice)

        return app