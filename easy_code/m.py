import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QFileDialog
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
window.resize(400, 300)  

layout = QVBoxLayout()
window.setLayout(layout)

media_player = QMediaPlayer()
audio_output = QAudioOutput()
media_player.setAudioOutput(audio_output)

load_button = QPushButton('загрузить музыку')
play_button = QPushButton('воспроизвести')
stop_button = QPushButton('стоп')
next_button = QPushButton('вперед')
back_button = QPushButton('назад')

# Новые кнопки
prev_track_button = QPushButton('Предыдущий трек')
next_track_button = QPushButton('Следующий трек')
rewind_button = QPushButton('Перемотка назад на 5с')
fast_forward_button = QPushButton('Перемотка вперёд на 5с')

load_button.clicked.connect(load_track)
play_button.clicked.connect(play_track)
stop_button.clicked.connect(stop_track)
prev_track_button.clicked.connect(previous_track)
next_track_button.clicked.connect(next_track)
rewind_button.clicked.connect(rewind_5s)
fast_forward_button.clicked.connect(fast_forward_5s)

track_list = QListWidget()
track_paths = []

layout.addWidget(load_button)
layout.addWidget(track_list)
layout.addWidget(play_button)
layout.addWidget(stop_button)
layout.addWidget(prev_track_button)      
layout.addWidget(next_track_button)         
layout.addWidget(rewind_button)             
layout.addWidget(fast_forward_button)      

window.show()

app.exec()
