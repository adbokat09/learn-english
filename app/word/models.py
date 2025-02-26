from app.config.db import db


class Word(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word = db.Column(db.String(255), nullable=False)
    # transcription = db.Column(db.String(255), nullable=False)
    definition = db.Column(db.Text, nullable=False)
    photo_link = db.Column(db.String(255), nullable=True)
    word_sets = db.relationship('WordSet', secondary='word_to_word_set', back_populates='words', lazy=True)

    def __str__(self):
        return f'Word {self.id}, {self.word}'


class WordSet(db.Model):
    __tablename__ = 'word_sets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    words = db.relationship('Word', secondary='word_to_word_set', back_populates='word_sets', lazy=True)


word_to_word_set = db.Table(
    'word_to_word_set',
    db.Column('word_id', db.Integer, db.ForeignKey('words.id')),
    db.Column('word_set_id', db.Integer, db.ForeignKey('word_sets.id'))

)