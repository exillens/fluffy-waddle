import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl

#создать окно

app = QApplication(sys.argv)
window = QWidget()
window.resize(900,700)



audio_output = QAudioOutput()
media_player = QMediaPlayer()
video_widget = QVideoWidget()

media_player.setAudioOutput(audio_output)
media_player.setVideoOutput(video_widget)

video_widget.resize(800,600)


layout = QVBoxLayout()

layout.addWidget(video_widget)



video = QUrl.fromLocalFile("videoo.mp4")

media_player.setSource(video)

media_player.play()


window.setLayout(layout)



window.show()

app.exec()