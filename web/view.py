
from pprint import pprint

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from util.db import DBDemo

bp = Blueprint("view", __name__, url_prefix="/view")


@bp.route("/page", methods=("GET", "POST"))
def page():
        """
        Renders a simple page from a template
        """

        return render_template("view/page.html")


@bp.route("/db", methods=("GET", "POST"))
def db():
        """
        Renders a simple page from a template
        """
        db = DBDemo()
        db.execute("INSERT INTO timestamps(wordplace) VALUES (?)",[["This is some text"]])

        data = db.execute("SELECT wordplace, timeinstance FROM timestamps",[])

        pprint(data)
        return render_template("view/db.html", data=data)
