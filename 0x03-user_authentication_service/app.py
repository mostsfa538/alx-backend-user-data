#!/usr/bin/env python3
""" Flask app """
from flask import Flask, jsonify, request, abort
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=["GET"])
def home():
    """ return a JSON payload of the form """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """ Register user """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 404


@app.route('/sessions', methods=['POST'])
def login():
    """ create a new session for the user """
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    out = jsonify(email=email, message="logged in")
    out.set_cookie("session_id", session_id)
    return out


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
