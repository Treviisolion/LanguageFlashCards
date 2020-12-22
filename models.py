"""Models for Language Flashcards"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Users"""

    __tablename__ = 'users'

    username = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String(), nullable=False)

    languages = db.relationship('UserLanguage', cascade='all, delete-orphan')

    @classmethod
    def register(cls, username, password):
        """Registers user with hashed password and returns new user"""

        hashed = bcrypt.generate_password_hash(password)
        hashed = hashed.decode('utf8')
        return cls(username=username, password=hashed)

    @classmethod
    def authenticate(cls, username, password):
        """If valid user and password pair provided returns authenticated user info, else returns False"""

        user = User.query.get(username)
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class UserLanguage(db.Model):
    """The languages that the user is practicing, plus English as the default one to translate into"""

    __tablename__ 'languages'
    __table_args__ = (db.UniqueConstraint('user', 'language'),)

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user = db.Column(
        db.String(),
        db.ForeignKey('users.username'),
        nullable=False
    )
    language = db.Column(db.String(3), nullable=False)

    words = db.relationship('Word', cascade='all, delete-orphan')


class Word(db.Model):
    """Language morphemes, ideally base form of words"""

    __tablename__ = 'words'
    __table_args__ = (db.UniqueConstraint('user', 'word'),)

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    language = db.Column(
        db.Integer(),
        db.ForeignKey('languages.id'),
        nullable=False
    )
    word = db.Column(db.String(), nullable=False)
    pronunciations = db.Column(db.String(), nullable=False) # Multiple pronunciations are separated by comma delimited values

    pronunciations = db.Relationship(
        'Pronuciation',
        cascade='all, delete-orphan'
    )
    translations = db.relationship(
        'Word',
        secondary='translations',
        primaryjoin=(Translation.word == id),
        secondaryjoin=(Translation.translation == id)
    )
    translation_for = db.relationship(
        'Word',
        secondary='translations',
        primaryjoin=(Translation.translation == id),
        secondaryjoin=(Translation.word == id)
    )


class Translation(db.Model):
    """Translations, i.e. any plausible translation for the given word"""

    __tablename__ = 'translations'

    word = db.Column(
        db.Intger(),
        db.ForeignKey('words.id', ondelete='cascade'),
        primary_key=True
    )
    translation = db.Column(
        db.Integer(),
        db.ForeignKey('words.id', ondelete='cascade'),
        primary_key=True
    )
