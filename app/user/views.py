import functools

from flask import Blueprint, jsonify, request, session, g
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from app.config.db import db
from app.auth.models import User
from app.auth.views import validate_password, validate_email

bp = Blueprint('user', __name__, url_prefix='/user')


def set_user_from_session():
    user_id = session.get('user_id')
    g.user = User.query.filter_by(id=user_id).first()


@bp.before_app_request
def auth_required():
    set_user_from_session()
    if not g.user:
        return jsonify({'error': 'Authentication required'}), 401



@bp.route('/change-nickname', methods={'PATCH'})
def change_nickname():
    data = request.json
    new_nickname = data['nickname']
    password = data['password']

    if not check_password_hash(g.user.password, password):
        return jsonify({'error': 'You are not authorized to perform this action'}), 403

    try:
        g.user.nickname = new_nickname
        db.session.add(g.user)
        db.session.commit()
    except IntegrityError:
        return jsonify({'error': 'Nickname already exists'}), 400

    return jsonify({'id': g.user.id, "email": g.user.email, 'nickname': g.user.nickname})


@bp.route('/change-email', methods={'PATCH'})
def change_email():
    data = request.json
    try:
        new_email = data['email']
        password = data['password']
    except KeyError:
        return jsonify({'error': 'Field `email` and `password` is required'}), 400

    try:
        validate_email(new_email)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    if not check_password_hash(g.user.password, password):
        return jsonify({'error': 'You are not authorized to perform this action'}), 403

    try:
        g.user.email = new_email
        db.session.add(g.user)
        db.session.commit()
    except IntegrityError:
        return jsonify({'error': 'Email already exists'}), 400

    return jsonify({'id': g.user.id, "email": g.user.email, 'nickname': g.user.nickname})


@bp.route('/change-password', methods={'PATCH'})
def change_password():
    data = request.json
    try:
        new_password = data['new_password']
        password = data['password']
    except KeyError:
        return jsonify({'error': 'Field `password` and `new_password` is required'}), 400

    try:
        validate_password(password)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    if not check_password_hash(g.user.password, password):
        return jsonify({'error': 'You are not authorized to perform this action'}), 403

    g.user.password = generate_password_hash(new_password)
    db.session.add(g.user)
    db.session.commit()

    return jsonify({'id': g.user.id, "email": g.user.email, 'nickname': g.user.nickname})


# password >= 6 elements
