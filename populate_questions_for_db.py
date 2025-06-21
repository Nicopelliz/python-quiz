import json
from flask import Flask
from db import db
from models import Question
from config import Config

# Configura l'app Flask
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Percorso del file JSON (nella stessa cartella)
FILENAME = 'nlp_quiz_questions.json'


def load_questions_from_file():
    with open(FILENAME, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with app.app_context():
        for item in data:
            q = Question(
                text=item['question'],
                correct_answer=item['correct'],
                incorrect_answers=','.join(item['wrong'])
            )
            db.session.add(q)
        db.session.commit()
        print(f"Inserite {len(data)} domande nel database.")

if __name__ == '__main__':
    load_questions_from_file()
