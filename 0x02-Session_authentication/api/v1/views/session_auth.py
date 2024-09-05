#!/usr/bin/env python3
""" Session authentication """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from os import getenv


@app_views.route("/auth_session/login/",
                 methods=["POST"],
                 strict_slashes=False)
def login_auth():
    """POST /api/v1/auth_session/login"""
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    out = jsonify(user.to_json())
    out.set_cookie(getenv("SESSION_NAME"), auth.create_session(user.id))
    return out


@app_views.route("/auth_session/logout/",
                 methods=["DELETE"],
                 strict_slashes=False)
def logout():
    """DELETE /api/v1/auth_session/logout
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
