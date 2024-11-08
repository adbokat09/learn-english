import functools

from flask import Blueprint, jsonify, request, session, g
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from app.config.db import db
from app.auth.models import User
from string import ascii_lowercase, ascii_uppercase

bp = Blueprint('auth', __name__, url_prefix='/auth')


def validate_password(password):
    if len(password) < 6:
        raise ValueError('Invalid password')


def validate_email(email):
    if '@' not in email:
        raise ValueError('Invalid email')


@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    try:
        validate_password(data['password'])
        validate_email(data['email'])
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    user = User(
        email=data['email'],
        nickname=data['nickname'],
        password=generate_password_hash(data['password'])
    )
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify({'error': 'User with email or nickname already exists'}), 400
    session['user_id'] = user.id
    return jsonify({'id': user.id, "email": user.email, 'nickname': user.nickname})


@bp.route('/login', methods={'POST'})
def login():
    data = request.json
    try:
        nickname = data['nickname']
        password = data['password']
    except KeyError:
        return jsonify({'error': 'nickname and password are required'}), 400
    user = User.query.filter_by(nickname=nickname).first()
    if not (user and check_password_hash(user.password, password)):
        return jsonify({'error': 'Invalid nickname or password'}), 404
    session['user_id'] = user.id
    return jsonify({'id': user.id, "email": user.email, 'nickname': user.nickname})

