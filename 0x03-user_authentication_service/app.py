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
        Auth.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
