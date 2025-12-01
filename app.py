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
    users[request.sid] = {'nickname': nickname, 'publicKey': publicKey} # Tworzymy element słownika w tablicy users (dla każdego SID przypisujemy nickname i RES public key

    print(f"Dołączył: {nickname} (ID: {request.sid})")
    # 2. Powiadamiamy innych użytkowników o nowym (z SID, żeby mogli mu wysłać klucz)
    new_user_data = {
        'sid': request.sid,
        'nickname': nickname,
        'publicKey': publicKey
    }
    emit('user_joined', new_user_data, broadcast=True, include_self=False)
    # 3. Przygotowujemy listę obecnych dla nowego użytkownika
    others = {
        data['nickname']: data['publicKey']
        for sid, data in users.items() if sid != request.sid
    }

    # Rozesłanie informacji o pozostałych użytkownikach dla nowego użytkownika
    emit('current_users', others)

    emit('update_history', history)


@socketio.on('send_key_to_user')
def handle_send_key(data):
    # Odbieramy od "Dawcy"
    target_sid = data['target_sid']
    encrypted_key = data['encrypted_key']

    print(f"[Serwer] Przekazuję zaszyfrowany klucz AES do użytkownika: {target_sid}")

    # Przekazujemy do "Biorcy" (bezpośrednio do jego pokoju/sid)
    emit('receive_key', {'key': encrypted_key}, room=target_sid)

@socketio.on('message')
def handle_message(message, current_nickname):
    print(f"[Serwer] {current_nickname} wysłał wiadomość: {message}")
    history.append({'nickname': current_nickname, 'message': message})

    emit("update_history", history, broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in users:
        nickname = users[request.sid]['nickname']
        print(f"Rozłączył się: {nickname} (ID: {request.sid})")

        # Usuwamy użytkownika z pamięci serwera
        del users[request.sid]

        # Powiadamiamy innych, żeby usunęli go ze swojej listy GUI
        emit('user_left', nickname, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)