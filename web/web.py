import os
from multiprocessing import Process
import asyncio

from quart import Quart

"""Create and configure an instance of the Quart application."""
def build_app(config_data=None):

    app = Quart(__name__, instance_relative_config=True)
    app.config['config']=config_data
    from . import view
    app.register_blueprint(view.bp)
    from . import chat
    app.register_blueprint(chat.bp)
    from . import photo
    app.register_blueprint(photo.dynamicRoutes(app,photo.bp))


    @app.route("/hello")
    def hello():
        return "Hello, World!"

    @app.route("/")
    def index():
        return """
    <H1>Examples:</H1>
    <ul>
    <li><a href="hello">Hello World</a></li>
    <li><a href="view/db">SQLite DB Hammering</a></li>
    <li><a href="chat/">WebSocket Chat</a></li>
    <li><a href="photo/">Photo DB action example</a></li>
    </ul>"""

    return app


def app_process(host="0.0.0.0",port=5000,debug=False,use_reloader=False,config_data=None):
    app = build_app(config_data)
    return Process(
            target=app.run,
            kwargs={
            "host":host,
            "port":port,
            "debug":debug,
            "use_reloader":use_reloader
            }
    )


def app_task(host="0.0.0.0",port=5000,debug=False,use_reloader=False,config_data=None):
    app = build_app(config_data)
    return app.run_task(
            host=host,
            port=port,
            debug=debug
            )


if __name__ == '__main__':
    web_task=app_task()
    asyncio.run(web_task)
