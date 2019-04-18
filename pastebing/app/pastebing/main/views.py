#!/usr/bin/env python3
import functools
import re
import datetime

import base58
import sqlalchemy
from flask import (
    render_template_string,
    request,
    render_template,
    current_app,
    flash,
    redirect,
    url_for,
    session,
    make_response,
    Response,
)

from . import bp as app  # Note that app = blueprint, current_app = flask context


def require_auth(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        if "username" not in session:
            flash("You must login to view this page.", "danger")
            return redirect(url_for("main.login"))

        return f(*args, **kwargs)

    return wrap


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            with current_app.db.isolate() as conn:
                conn.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        except sqlalchemy.exc.IntegrityError:
            flash("Username already taken!", "danger")
            return render_template("register.html")
        else:
            session["username"] = username

            return redirect(url_for("main.pastes"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            with current_app.db.isolate() as conn:
                r = conn.execute("SELECT id FROM users WHERE username=%s AND password=%s", (username, password)).first()

            if not r:
                raise RuntimeError("Incorrect username and/or password!")
        except RuntimeError as e:
            flash(str(e), "danger")
            return render_template("login.html")
        else:
            session["username"] = username

            return redirect(url_for("main.pastes"))

    return render_template("login.html")


@app.route("/pastes", methods=["GET"])
@require_auth
def pastes():
    # Fetch all posts by this user
    with current_app.db.isolate() as conn:
        pastes = conn.execute(
            "SELECT * FROM pastes WHERE author IN (SELECT id FROM users WHERE username=%s)", (session["username"])
        ).fetchall()

    # Coerce them all into dicts for ez indexing
    pastes = sorted([dict(x) for x in pastes], key=lambda p: p["created_at"], reverse=True)

    return render_template("pastes.html", pastes=pastes)


@app.route("/new", methods=["GET", "POST"])
@require_auth
def new_paste():
    if request.method == "POST":
        title = request.form["title"]
        contents = request.form["contents"]

        # Get the authors ID, and number of posts they've made
        with current_app.db.isolate() as conn:
            author_id = conn.execute("SELECT id FROM users WHERE username=%s", (session["username"],)).first()[0]
            post_count = conn.execute("SELECT COUNT(*) FROM pastes WHERE author=%s", (author_id,)).first()[0]

        # Generate the new post ID
        post_id = base58.b58encode(f"{author_id}:{post_count + 1}").decode("UTF-8")

        # Insert new paste
        try:
            with current_app.db.isolate() as conn:
                conn.execute(
                    "INSERT INTO pastes (id, title, author, contents) VALUES (%s, %s, %s, %s)",
                    (post_id, title, author_id, contents),
                )
        except Exception as e:
            flash("Something went wrong while creating your paste, try again later.", "danger")

            return render_template("new_paste.html")
        else:
            flash("Created paste successfully!", "success")

            return redirect(url_for("main.pastes"))

    return render_template("new_paste.html")


@app.route("/raw/<paste_id>")
def raw_paste(paste_id):
    # Get the paste, if it exists
    with current_app.db.isolate() as conn:
        paste = conn.execute("SELECT contents FROM pastes WHERE id=%s", (paste_id,)).first()

    if not paste:
        resp = Response("Paste not found.")
        resp.headers["Content-Type"] = "text/plain"
        resp.status_code = 404

        return resp

    resp = Response(paste[0])
    resp.headers["Content-Type"] = "text/plain"

    return resp


@app.route("/ping")
def ping():
    return "pong"


@app.route("/flag_debug", methods=["POST"])
def flag_debug():
    if request.form.get("flag_secret", "") == current_app.config["FLAG_SECRET"]:
        return current_app.config["FLAG"]
    return ":(", 401
