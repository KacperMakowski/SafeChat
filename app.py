import os

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'sekretny-klucz-domyslny-do-testow')
socketio = SocketIO(app)

users = {}
history = []

# Renderuje główny widok czatu po udanym zalogowaniu
@app.route('/chat')
def chat():

    return render_template('chat.html')

# Renderuje stronę startową (formularz logowania)
@app.route('/')
def index():

    return render_template('login.html')

# Obsługuje dołączenie nowego użytkownika: zapisuje go w pamięci, informuje innych i przesyła nowemu stan pokoju
@socketio.on('join')
def handle_join(nickname, publicKey):
    # Zapis nowego użytkownika
    users[request.sid] = {'nickname': nickname, 'publicKey': publicKey} # Dodaje nowego użytkownika do słownika 'users', mapując jego Session ID na dane (nick, klucz publiczny)

    print(f"Dołączył: {nickname} (ID: {request.sid})")

    # Serwer wysyła dane do innych użytkowników
    new_user_data = {
        'sid': request.sid,
        'nickname': nickname,
        'publicKey': publicKey
    }
    emit('user_joined', new_user_data, broadcast=True, include_self=False)

    # Serwer wysyła dane pozostałych użytkowników
    others = {
        data['nickname']: data['publicKey']
        for sid, data in users.items() if sid != request.sid
    }

    emit('current_users', others)

    emit('update_history', history)

# Pełni rolę pośrednika. Przekazuje zaszyfrowany klucz AES od jednego klienta do konkretnego odbiorcy (Target SID).
@socketio.on('send_key_to_user')
def handle_send_key(data):
    target_sid = data['target_sid']
    encrypted_key = data['encrypted_key']

    print(f"[Serwer] Przekazuję zaszyfrowany klucz AES do użytkownika: {target_sid}")

    emit('receive_key', {'key': encrypted_key}, room=target_sid)

# Odbiera zaszyfrowaną wiadomość wraz z wektorem inicjującym (IV) i nickiem użytkownika
@socketio.on('message')
def handle_message(message):

    sender_nick = users[request.sid]['nickname']
    print(f"[Serwer] {sender_nick} wysłał wiadomość: {message}")

    # Dodaje wiadomość do historii
    history.append({'nickname': sender_nick, 'message': message})

    # Jeżeli historia jest > 10 to usuwa 1. element
    if len(history) > 10:
        history.pop(0)

    # Rozsyła zaktualizowaną, pełną listę historii wiadomości do wszystkich podłączonych użytkowników
    emit("update_history", history, broadcast=True)

# Obsługuje rozłączenie klienta (zamknięcie karty/utrata sieci). Usuwa go z listy i powiadamia resztę.
@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in users:
        nickname = users[request.sid]['nickname']
        print(f"Rozłączył się: {nickname} (ID: {request.sid})")

        del users[request.sid]

        emit('user_left', nickname, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)