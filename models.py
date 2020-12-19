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

    words = db.relationship('Word', cascade="all, delete-orphan")

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


class Word(db.Model):
    """Foreign language morphemes, ideally base form of words"""

    __tablename__ = 'words'
    __table_args__ = (db.UniqueConstraint('user', 'word', 'pronunciation'),)

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user = db.Column(db.String(),
                     db.ForeignKey('users.username'),
                     nullable=False)
    word = db.Column(db.String(), nullable=False)
    pronunciation = db.Column(db.String(), nullable=False)

    synonyms = db.relationship('Synonym', cascade="all, delete-orphan")


class Synonym(db.Model):
    """English language synonyms, i.e. any plausible translation for the given word"""

    __tablename__ = 'synonyms'

    synonym = db.Column(db.String(), primary_key=True)
    word_id = db.Column(db.Integer(),
                        db.ForeignKey('words.id'),
                        primary_key=True)
