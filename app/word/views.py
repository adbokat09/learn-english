from flask import Blueprint, jsonify, request, session, g
from app.config.db import db
from app.user.views import set_user_from_session
from app.word.models import WordSet, Word

bp = Blueprint('word', __name__, url_prefix='/words')


# @bp.before_app_request
@bp.before_request
def auth_required():
    set_user_from_session()
    if not g.user:
        return jsonify({'error': 'Authentication required'}), 401


@bp.route('word-sets/', methods=['POST'])
def create_word_set():
    data = request.get_json()
    name = data['name']
    user_id = g.user.id
    word_set = WordSet(name=name, author_id=user_id)
    db.session.add(word_set)
    db.session.commit()

    return jsonify({'id': word_set.id, 'name': word_set.name}), 201


@bp.route('word-sets/', methods=['GET'])
def get_word_sets():
    user_id = g.user.id
    word_sets = WordSet.query.filter_by(author_id=user_id).all()
    return jsonify({'objects': [{'id': word_set.id, 'name': word_set.name} for word_set in word_sets]})


@bp.route('word-sets/<int:id>', methods=['DELETE'])
def delete_word_set(id):
    user_id = g.user.id
    word_set = WordSet.query.filter_by(author_id=user_id, id=id).first()
    if not word_set:
        return jsonify({'error': f'word set with {id=} not found for this user'}), 404
    db.session.delete(word_set)
    db.session.commit()
    return '', 204


@bp.route('word-sets/<int:id>', methods=['PUT', 'PATCH'])
def update_word_set(id):
    data = request.get_json()
    name = data['name']

    user_id = g.user.id
    word_set = WordSet.query.filter_by(author_id=user_id, id=id).first()
    if not word_set:
        return jsonify({'error': f'word set with {id=} not found for this user'}), 404
    word_set.name = name
    db.session.add(word_set)
    db.session.commit()

    return jsonify({'id': word_set.id, 'name': word_set.name}), 200


@bp.route('/word-sets/<int:word_set_id>/words', methods=["POST"])
def create_word(word_set_id):
    data = request.get_json()
    word = data['word']
    # transcription = data['transcription']
    definition = data['definition']

    user_id = g.user.id

    word_set = WordSet.query.filter_by(author_id=user_id, id=word_set_id).first()
    if not word_set:
        return jsonify({'error': f'word set with {word_set_id=} not found for this user'}), 404

    word_obj = Word(word=word, definition=definition) # transcription
    db.session.add(word_obj)
    word_set.words.append(word_obj)

    db.session.commit()

    return jsonify({'id': word_obj.id, 'word': word_obj.word,
                    'definition': word_obj.definition}), 201  #'transcription': word_obj.transcription,


@bp.route('/word-sets/<int:word_set_id>/words/<int:word_id>', methods=["DELETE"])
def delete_word(word_set_id, word_id):
    user_id = g.user.id
    word_set = WordSet.query.filter_by(author_id=user_id, id=word_set_id).first()
    if not word_set:
        return jsonify({'error': f'word set with {word_set_id=} not found for this user'}), 404

    word = Word.query.filter_by(id=word_id).first()
    if not word:
        return jsonify({'error': f'word with {word_id=} not found'}), 404

    word_set.words.remove(word)
    db.session.commit()

    return '', 204
