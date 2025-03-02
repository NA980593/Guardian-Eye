from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os

import random
from string import ascii_letters
from flask_socketio import SocketIO, join_room, leave_room, send
from chat_screener import isMessageSuspicious

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Configuring SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guardians.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(65), unique = True, nullable = False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



@app.route('/')
@app.route('/home')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('home_page.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/whatToDo')
def whatToDo():
    return render_template('whatToDo.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    user = User.query.filter_by(username=username).first()
    em = User.query.filter_by(email = email).first()
    if user and em and user.check_password(password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return render_template('home_page.html', error='Invalid username or password.')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    em = User.query.filter_by(email = email).first()
    if user:
        flash('Username already exists')
        return render_template('home_page.html', error='Username already exists.')
    if em:
        flash('Email already exists')
        return render_template('home_page.html', error = 'Email already exists.')
    if em and user:
        flash('Either your Username or Email exists already')
    else:
        new_user = User(username=username, email = email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


socketio = SocketIO(app)

# A mock database to persist data
rooms = {}

# ...
def generate_room_code(length: int, existing_codes: list[str]) -> str:
    return "fruitsnacks"

# Home Route
@app.route('/chat', methods=["GET", "POST"])
def chathome():
    session.clear()
    if request.method == "POST":
        name = request.form.get('name')
        create = request.form.get('create', False)
        code = request.form.get('code')
        join = request.form.get('join', False)
        if not name:
            return render_template('chathome.html', error="Name is required", code=code)
        if create != False:
            room_code = generate_room_code(6, list(rooms.keys()))
            new_room = {
                'members': 0,
                'messages': []
            }
            rooms[room_code] = new_room
        if join != False:
            # no code
            if not code:
                return render_template('chathome.html', error="Please enter a room code to enter a chat room", name=name)
            # invalid code
            if code not in rooms:
                return render_template('chathome.html', error="Room code invalid", name=name)
            room_code = code
        session['room'] = room_code
        session['name'] = name
        return redirect(url_for('room'))
    else:
        return render_template('chathome.html')
# ...

# Room route
@app.route('/room')
def room():
    room = session.get('room')
    name = session.get('name')
    if name is None or room is None or room not in rooms:
        return redirect(url_for('home'))
    messages = rooms[room]['messages']
    return render_template('room.html', room=room, user=name, messages=messages)


# Connect Websocket Event
...
@socketio.on('connect')
def handle_connect():
    name = session.get('name')
    room = session.get('room')
    if name is None or room is None:
        return
    if room not in rooms:
        leave_room(room)
    join_room(room)
    send({
        "sender": "",
        "message": f"{name} has entered the chat"
    }, to=room)
    rooms[room]["members"] += 1
...

# Message Websocket Event
...
@socketio.on('message')
def handle_message(payload):
    room = session.get('room')
    name = session.get('name')
    if room not in rooms:
        return
    print(isMessageSuspicious(payload["message"]))
    message = {
        "sender": name,
        "message": payload["message"]
    }
    send(message, to=room)
    rooms[room]["messages"].append(message)
...

# Disconnect Websocket Event
...
@socketio.on('disconnect')
def handle_disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)
    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
        send({
        "message": f"{name} has left the chat",
        "sender": ""
    }, to=room)
...


if __name__ in '__main__':
    # Create a db and table
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)