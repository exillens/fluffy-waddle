# Импорт
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl


total_water = 0
goal = 2000
new_goal = 0

#создать окно

app = QApplication(sys.argv)
window = QWidget()
window.resize(900,700)

layout = QVBoxLayout()
goal_layout = QHBoxLayout()
layout.addLayout(goal_layout)


input_layout = QHBoxLayout()
layout.addLayout(input_layout)



title_lable = QLabel("Введите объем воды (мл): ")
total_lable = QLabel(f"Выпито воды сегодня: {total_water}/{goal}")
goal_input = QLineEdit()
goal_input.setPlaceholderText("Введи свою цель (по умолчанию: 2000мл): ")
water_input = QLineEdit()
water_input.setPlaceholderText("Например 200мл: ")

set_goal_button = QPushButton()
add_button = QPushButton()
reset_button = QPushButton()

progress_bar = QProgressBar()

#добавим наши виджеты в окно
layout.addWidget(title_lable)
goal_layout.addWidget(goal_input)
goal_layout.addWidget(set_goal_button)
input_layout.addWidget(water_input)
input_layout.addWidget(add_button)
layout.addWidget(progress_bar)
layout.addWidget(total_lable)
layout.addWidget(reset_button)



window.setLayout(layout)
window.show()

app.exec()