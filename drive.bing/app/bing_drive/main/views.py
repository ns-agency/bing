#!/usr/bin/env python3
import functools
import re
import datetime
import os
import logging

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
    jsonify,
    send_from_directory,
)

import base64

from flask_cors import CORS
from . import bp as app  # Note that app = blueprint, current_app = flask context

CORS(app)

ROOT = os.path.normpath(os.path.join(__file__, "../../../frontend/dist"))


def get_files_for_acc(username, role):
    r = list(current_app.db.execute("SELECT name, content FROM files where author=%s", (username,)))
    if role == "Staff":
        r += list(current_app.db.execute("SELECT name, content FROM files where author='staff_account'"))
    return r


@app.route("/", methods=["GET"])
def home():
    return send_from_directory(f"{ROOT}", "index.html")


@app.route("/docs/<path>", methods=["GET"])
def docs_serve(path):
    return send_from_directory(f"/app/web/docs", path)


@app.route("/js/<path>", methods=["GET"])
def js_serve(path):
    return send_from_directory(f"{ROOT}/js", path)


@app.route("/css/<path>", methods=["GET"])
def css_serve(path):
    return send_from_directory(f"{ROOT}/css", path)


@app.route("/img/<path>", methods=["GET"])
def img_serve(path):
    return send_from_directory(f"{ROOT}/img", path)


@app.route("/register", methods=["POST"])
def register():
    payload = request.json
    username = payload.get("username", None)
    password = payload.get("password", None)

    if not username or not password:
        return "invalid username/password", 400
    if username == "admin" or username == "staff_account":
        return "username taken", 400
    if current_app.db.execute("SELECT * FROM users WHERE username = %s", (username,)).first() is not None:
        return "username taken", 400

    current_app.db.execute("INSERT INTO users VALUES(%s,%s,'User')", (username, password))
    session["username"] = username
    session["role"] = "User"
    return ":)", 200


@app.route("/login", methods=["POST"])
def login():
    p = request.json
    res = current_app.db.execute(
        "SELECT username,role FROM users WHERE username = %s AND password = %s", (p["username"], p["password"])
    ).first()
    if res is None:
        return "invalid username/password", 400

    [username, role] = res
    session["username"] = username
    session["role"] = role
    return ":)", 200


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return ":)", 200


@app.route("/upload", methods=["POST"])
def upload():
    p = request.json
    me = session["username"]
    name = p["name"]
    text = p["text"]

    if len(p["text"]) > 64:
        return "File contents > 64 chars", 400

    if len(p["name"]) > 64:
        return "File name > 64 chars", 400

    files = get_files_for_acc(me, session["role"])

    if len(files) > 5:
        return "max files for acc reached", 400

    if current_app.db.execute("SELECT * FROM files WHERE name = %s AND author = %s", (name, me)).first() is not None:
        return "file name taken", 400

    current_app.db.execute("INSERT INTO files(name,content,author) VALUES(%s,%s,%s)", (name, text, me))
    return ":)", 200


@app.route("/me", methods=["GET"])
def me():
    results = get_files_for_acc(session["username"], session["role"])
    files = [{"name": r[0], "content": r[1]} for r in results]

    if session["role"] == "Admin":
        files += [
            {
                "name": "BREAK2{f46728bf-0f09-4a39-822a-4cf231325e90}",
                "content": "cheeky, no flag tho",
                "author": "admin",
            }
        ]
    return jsonify({"username": session["username"], "role": session["role"], "files": files})


@app.route("/admin", methods=["GET", "POST"])
def admin():
    success = False
    if request.method == "POST":
        if request.form.get("pin", "0000") == "2941":
            success = True
    return render_template("admin.html", success=success)


@app.route("/document/<name>", methods=["GET"])
def view_document(name):
    username = base64.b64decode(request.args["r"]).decode("utf-8")

    content = current_app.db.execute(
        "SELECT content FROM files WHERE name = %s AND author = %s", (name, username)
    ).first()

    if not content and session["role"] == "Staff":
        content = current_app.db.execute(
            "SELECT content FROM files WHERE name = %s AND author = 'staff_account'", (name,)
        ).first()

    return content[0] if content else "ruh roh"


@app.route("/api/secret/no/really/give_staff_access")
def staff_access():
    username = request.args["username"]
    current_app.db.execute("UPDATE users set role='Staff' WHERE username = %s", (username,))

    session["role"] = "Staff"
    return ":)", 200


@app.route("/api/peek/<username>", methods=["GET", "POST"])
def peek(username):
    if session["role"] != "Staff" and session["role"] != "Admin":
        return ":(", 404
    rows = current_app.db.execute("SELECT id,name,author from files where author = %s", (username,))
    return jsonify([{"id": r[0], "name": r[1], "author": r[2]} for r in rows])


@app.route("/api/peek/file", methods=["GET", "POST"])
def peekFile():
    if session["role"] != "Staff" and session["role"] != "Admin":
        return ":(", 404
    file_id = request.args["file_id"]
    res = current_app.db.execute("SELECT id,name,content,author from files where id = " + file_id).first()
    if res is None:
        return ":(", 400
    return jsonify({"id": res[0], "name": res[1], "content": res[2], "author": res[3]})


@app.route("/ping")
def ping():
    return "pong"


@app.route("/flag_debug", methods=["POST"])
def flag_debug():
    if request.form.get("flag_secret", "") == current_app.config["FLAG_SECRET"]:
        return current_app.config["FLAG"]
    return ":(", 401
