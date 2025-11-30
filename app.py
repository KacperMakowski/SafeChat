from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

users = {}
history = []

@app.route('/chat')
def chat():

    return render_template('chat.html')

@app.route('/')
def index():

    return render_template('login.html')

@socketio.on('connect')
def handle_connect():
    emit('update_history', history)

@socketio.on('join')
def handle_join(nickname):
    users[request.sid] = {'nickname': nickname}
    print(f"Dołączył: {nickname} (ID: {request.sid})")
    emit('update_history', history)

@socketio.on('message')
def handle_message(message, current_nickname):
    print(f"Serwer: Klient wysłał wiadomość: {message}")
    history.append(message)
    print(f"Historia wiadomości:\n{history}")

    emit("update_history", history, current_nickname, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)