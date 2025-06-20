from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import random
from weather import get_weather_forecast
from db import db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

from models import User, Question

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            weather_data = get_weather_forecast(city)
    return render_template('index.html', weather=weather_data)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        nickname = request.form['nickname']
        password = request.form['password']
        confirm = request.form['confirm']
        if User.query.filter_by(nickname=nickname).first():
            flash("Login già in uso.")
            return redirect(url_for('register'))
        if password != confirm:
            flash("Le password non corrispondono.")
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(password)
        user = User(name=name, nickname=nickname, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Registrazione completata. Ora puoi effettuare il login.")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nickname = request.form['nickname']
        password = request.form['password']
        user = User.query.filter_by(nickname=nickname).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash("Login effettuato con successo.")
            return redirect(url_for('quiz'))
        flash("Credenziali errate.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logout effettuato.")
    return redirect(url_for('index'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    score = user.score or 0

    if request.method == 'POST':
        question_id = int(request.form['question_id'])
        selected = request.form.get('option')
        question = Question.query.get(question_id)
        if question.correct_answer == selected:
            user.score = (user.score or 0) + 1
            db.session.commit()
        return redirect(url_for('quiz'))

    question = random.choice(Question.query.all())
    options = [question.correct_answer] + question.incorrect_answers.split(',')
    random.shuffle(options)
    return render_template('quiz.html', question=question, options=options, score=score)

@app.route('/leaderboard')
def leaderboard():
    users = User.query.order_by(User.score.desc()).limit(10).all()
    return render_template('leaderboard.html', users=users)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
