
from pprint import pprint

from quart import Blueprint
from quart import flash
from quart import g
from quart import redirect
from quart import render_template
from quart import request
from quart import session
from quart import url_for

from util.db import DBDemo

bp = Blueprint("chat", __name__, url_prefix="/chat")


@bp.route("/", methods=("GET", "POST"))
async def page():
        """
        Renders a simple page from a template
        """
        db = DBDemo()
        data = db.execute("SELECT timestamp, sender, message FROM chat",[])

        return await render_template("chat/page.html", data=data)


@bp.route("/send", methods=("GET", "POST"))
async def db():
        """
        Renders a simple page from a template
        """

        data = await ( request.get_json() )

        db = DBDemo()
        db.execute("INSERT INTO chat(sender,message) VALUES (?,?)",[data["sender"],data["message"]])

        resp = db.execute("SELECT timestamp, sender, message FROM chat",[])

        return await render_template("chat/page.html", data=resp)

