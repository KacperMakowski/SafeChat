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


@socketio.on('join')
def handle_join(nickname, publicKey):
    users[request.sid] = {'nickname': nickname, 'publicKey': publicKey}
    print(f"Dołączył: {nickname} (ID: {request.sid}\n{publicKey})")
    emit('update_history', history)

@socketio.on('message')
def handle_message(message, current_nickname):
    print(f"[Serwer] {current_nickname} wysłał wiadomość: {message}")
    history.append({'nickname': current_nickname, 'message': message})

    emit("update_history", history, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)