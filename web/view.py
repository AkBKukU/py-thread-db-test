
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

bp = Blueprint("view", __name__, url_prefix="/view")


@bp.route("/page", methods=("GET", "POST"))
async def page():
        """
        Renders a simple page from a template
        """

        return await render_template("view/page.html")


@bp.route("/db", methods=("GET", "POST"))
async def db():
        """
        Renders a simple page from a template
        """
        db = DBDemo()
        db.execute("INSERT INTO timestamps(wordplace) VALUES (?)",["This is some text"])

        data = db.execute("SELECT wordplace, timeinstance FROM timestamps",[])

        pprint(data)
        return await render_template("view/db.html", data=data)
