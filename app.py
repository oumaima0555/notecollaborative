from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

notes = {}  # room -> note content

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    if room not in notes:
        notes[room] = ''
    emit('note_update', notes[room], room=room)

@socketio.on('update_note')
def on_update(data):
    room = data['room']
    content = data['content']
    notes[room] = content
    emit('note_update', content, room=room, skip_sid=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)