"""Language Flashcard application"""

from flask import Flask, render_template, redirect, session, g, abort, flash
from models import db, connect_db, User, UserLanguage, Word
from sqlalchemy.exc import IntegrityError
from forms import UserForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY',
    'JohnathonAppleseed452'
)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql:///flashcards'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

CURR_USER_KEY = "curr_user"
DEFAULT_USER_LANGUAGE = 'EN'


############################
# Helper functions

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.username


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


############################
# Generic User Interactions

@app.route('/')
def get_main_page():
    """Returns the main page"""

    return render_template('main.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup_user():
    """Lets a user signup"""

    form = UserForm()

    if form.validate_on_submit():
        try:
            user = User.register(
                username=form.username.data,
                password=form.password.data
            )

            user_language = UserLanguage(
                user=user.username,
                language=DEFAULT_USER_LANGUAGE
            )

            db.session.add(user)
            db.session.add(user_language)
            db.session.commit()

            do_login(user)

            return redirect('/')

        except IntegrityError:
            flash('Username already taken', 'danger')
            return render_template('signup.html', form=form)
        except Exception as exc:
            print(type(exc))
            print(exc.args)
            print(exc)
            abort(404)
    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Lets a user login"""

    form = UserForm()

    if form.validate_on_submit():
        try:
            user = User.authenticate(
                username=form.username.data,
                password=form.password.data
            )

            if user:
                do_login(user)
                return redirect('/')
            else:
                flash('Invalid username or password', 'danger')
                return render_template('login.html', form=form)

        except Exception as exc:
            print(type(exc))
            print(exc.args)
            print(exc)
            abort(404)
    else:
        return render_template('login.html', form=form)


@app.route('/logout')
def logout_user():
    """Handle logout of user."""

    do_logout()
    flash('Logged out', 'success')
    return redirect('/login')


############################
# Specific user interactions

@app.route('/user')
def get_user_page():
    """Gets the main page for the logged in user"""
    if not g.user:
        flash('Access unauthorized', 'danger')
        return redirect('/')
    
    return render_template('user.html', default_language=DEFAULT_USER_LANGUAGE)

@app.route('/user/<string:language>')
def get_language_page(language):
    """Gets the main page for the specific language"""
    pass


@app.route('/language/add', methods=['GET', 'POST'])
def add_language():
    """Adds a new language to the user"""
    pass


@app.route('/<string:language>/add', methods=['GET', 'POST'])
def add_word():
    """Adds a new word to the language"""
    pass
