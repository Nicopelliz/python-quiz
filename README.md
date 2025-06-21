# 🌤️ Flask Weather & Quiz App

Un'applicazione web sviluppata con Flask che combina previsioni meteo e quiz interattivi. Gli utenti possono registrarsi, fare login, consultare il meteo di una città e mettere alla prova le proprie conoscenze tramite quiz a risposta multipla.

## 🔧 Funzionalità

### 🏠 Home Page
- Campo per l'inserimento del nome di una città
- Tabella con le **previsioni del tempo per 3 giorni** (oggi, domani, dopodomani)
- Ogni giorno mostra:
  - Nome del giorno (lunedì, martedì, ecc.)
  - Data
  - Temperatura diurna
  - Temperatura notturna

### 📝 Pagina di Registrazione
- Campo **login** (verifica dell’unicità del login nel database)
- Campo **password**
- Campo **conferma password**
- Campo **nickname** (verifica dell’unicità del nickname)

### 🔐 Pagina di Login
- Campo **login**
- Campo **password**

### ❓ Pagina Quiz
- Visualizza il **punteggio totale** del giocatore (collegato al proprio account)
- Una domanda alla volta
- 4 opzioni di risposta
- Le domande vengono presentate **in ordine casuale**, **infinite volte**

### 🏆 Classifica Quiz
- Visualizza i **nickname** dei giocatori registrati
- Visualizza i **punteggi** ottenuti nei quiz

---

## 🧭 Navigazione

Ogni pagina presenta un **intestazione con menu** dinamico:

- **Home** (sempre visibile)
- **Registrazione** (visibile solo se l'utente non è loggato)
- **Login** (visibile solo se l'utente non è loggato)
- **Logout** (visibile solo se l'utente è loggato)
- **Quiz** (visibile solo se l'utente è loggato)

---

## 👣 Piè di pagina

Ogni pagina include un piè di pagina con il **nome dello sviluppatore**.

---

## 📦 Requisiti (esempi)
- Python 3.x
- Flask
- SQLite3
- OpenWeatherMap API (o altro servizio meteo supportato)

---

## 🛠️ Avvio rapido

```bash
git clone https://github.com/nicopelliz/python-quiz.git
cd python-quiz
pip install -r requirements.txt
flask run
