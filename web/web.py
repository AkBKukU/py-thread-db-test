import os
from multiprocessing import Process
import asyncio

from quart import Quart

"""Create and configure an instance of the Quart application."""
app = Quart(__name__, instance_relative_config=True)

from . import view
app.register_blueprint(view.bp)
from . import chat
app.register_blueprint(chat.bp)


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
</ul>"""



def app_process(host="0.0.0.0",port=5000,debug=False,use_reloader=False):

    return Process(
            target=app.run,
            kwargs={
            "host":host,
            "port":port,
            "debug":debug,
            "use_reloader":use_reloader
            }
    )


def app_task(host="0.0.0.0",port=5000,debug=False,use_reloader=False):

    return app.run_task(
            host=host,
            port=port,
            debug=debug
            )


if __name__ == '__main__':
    web_task=app_task()
    asyncio.run(web_task)
