import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QFileDialog
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl


def load_track():
    file, _ = QFileDialog.getOpenFileName(
        window,
        "Загрузить трек",
        "",
        "Audio Files (*.mp3)"
    )
    if file:
        track_name = file.split("/")[-1]
        track_list.addItem(track_name)
        track_paths.append(file)

def play_track():
    selected_index = track_list.currentRow()
    if selected_index >= 0:
        file_path = track_paths[selected_index]
        media_player.setSource(QUrl.fromLocalFile(file_path))
        media_player.play()

def stop_track():
    media_player.stop()

def previous_track():
    current_index = track_list.currentRow()
    if current_index > 0:
        track_list.setCurrentRow(current_index - 1)
        play_track()

def next_track():
    current_index = track_list.currentRow()
    if current_index < track_list.count() - 1:
        track_list.setCurrentRow(current_index + 1)
        play_track()

def rewind_5s():
    position = media_player.position()
    new_position = max(0, position - 5000)
    media_player.setPosition(new_position)

def fast_forward_5s():
    position = media_player.position()
    new_position = position + 5000
    media_player.setPosition(new_position)

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Аудиоплеер')
window.resize(500, 400)

hlayout = QHBoxLayout()
layout = QVBoxLayout()
window.setLayout(layout)

media_player = QMediaPlayer()
audio_output = QAudioOutput()
media_player.setAudioOutput(audio_output)

load_button = QPushButton('Загрузить музыку')
play_button = QPushButton('Воспроизвести')
stop_button = QPushButton('Стоп')
prev_track_button = QPushButton('Предыдущий трек')
next_track_button = QPushButton('Следующий трек')

rewind_button = QPushButton('← 5с')
fast_forward_button = QPushButton('5с →')


load_button.clicked.connect(load_track)
play_button.clicked.connect(play_track)
stop_button.clicked.connect(stop_track)
prev_track_button.clicked.connect(previous_track)
next_track_button.clicked.connect(next_track)
rewind_button.clicked.connect(rewind_5s)
fast_forward_button.clicked.connect(fast_forward_5s)

track_list = QListWidget()
track_paths = []

hlayout.addWidget(rewind_button)          
hlayout.addWidget(track_list)         
hlayout.addWidget(fast_forward_button)  
layout.addWidget(load_button)
layout.addLayout(hlayout)          
layout.addWidget(play_button)
layout.addWidget(stop_button)
layout.addWidget(prev_track_button)
layout.addWidget(next_track_button)

window.show()
app.exec()
