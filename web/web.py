import os
from multiprocessing import Process
import asyncio

from quart import Quart


class WebServer(object):
    def __init__(self,host="0.0.0.0",port=5000,debug=False,use_reloader=False):
        """Create and configure an instance of the Quart application."""
        self.app = Quart(__name__, instance_relative_config=True)

        # Setup based on arguments
        self.host = host
        self.port = port
        self.debug = debug
        self.use_reloader = use_reloader

        @self.app.route("/hello")
        def hello():
            return "Hello, World!"

        @self.app.route("/")
        def index():
            return """
    <H1>Examples:</H1>
    <ul>
        <li><a href="hello">Hello World</a></li>
        <li><a href="view/db">SQLite DB Hammering</a></li>
        <li><a href="chat/">WebSocket Chat</a></li>
    </ul>"""


        from . import view
        from . import chat

        self.app.register_blueprint(view.bp)
        self.app.register_blueprint(chat.bp)

    def create_process(self):

        return Process(
                target=self.app.run,
                kwargs={
                "host":self.host,
                "port":self.port,
                "debug":self.debug,
                "use_reloader":self.use_reloader
                }
        )


    def create_task(self):

        return self.app.run_task(
                host=self.host,
                port=self.port,
                debug=self.debug
                )


if __name__ == '__main__':
    web_server = WebServer()
    web_task=web_server.create_task()
    asyncio.run(web_task)
