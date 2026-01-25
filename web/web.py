import os

from quart import Quart


def create_app(test_config=None):
    """Create and configure an instance of the Quart application."""
    app = Quart(__name__, instance_relative_config=True)


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


    from . import view
    from . import chat

    app.register_blueprint(view.bp)
    app.register_blueprint(chat.bp)

    #app.add_url_rule("/", endpoint="index")

    return app

if __name__ == '__main__':
    app = create_app(test_config=None)
    app.run()
