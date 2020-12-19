"""Language Flashcard application"""

from flask import Flask, render_template
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///flashcards')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# connect_db(app)

# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'JohnathonAppleseed452')

# db.create_all()

@app.route('/')
def get_main_page():
    """Returns the main page"""

    return render_template('main.html')