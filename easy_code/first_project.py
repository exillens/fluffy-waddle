from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, \
    QStackedWidget, QMessageBox
from PyQt6.QtCore import Qt, QTimer
import sys

# Создание приложения
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Pomodoro Timer")
window.resize(700, 400)

# Переменные для хранения состояния
pomodoro_time = 25 * 60  # 25 минут в секундах
short_break_time = 5 * 60  # 5 минут
long_break_time = 15 * 60  # 15 минут
pomodoro_count = 0
current_phase = "работа"
remaining_time = pomodoro_time
is_running = False
cycles_before_long_break = 4

# Создаем таймер
timer = QTimer()

# Создаем стек виджетов
main_layout = QVBoxLayout()
stack = QStackedWidget()

# ГЛАВНАЯ СТРАНИЦА
main_page = QWidget()
layout = QVBoxLayout(main_page)

menu = QLabel('POMODORO TIMER')
menu.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
maint_start = QPushButton('Начать работу')
main_settings = QPushButton('Настройки')

menu.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

layout.addWidget(menu)
layout.addWidget(maint_start)
layout.addWidget(main_settings)
layout.addStretch()

# СТРАНИЦА "Начать"
start = QWidget()
startV_layout = QVBoxLayout(start)

# Информационная панель
phase_label = QLabel("Текущая фаза: Работа")
time_label = QLabel("25:00")
time_label.setStyleSheet("font-size: 48px; font-weight: bold; margin: 20px;")
time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

count_label = QLabel("Выполнено помидоров: 0")

# Кнопки управления
startH_layout = QHBoxLayout()

start_button = QPushButton("Старт")
pause_button = QPushButton("Пауза")
reset_button = QPushButton("Сброс")
back_button = QPushButton("Меню")

startH_layout.addWidget(start_button)
startH_layout.addWidget(pause_button)
startH_layout.addWidget(reset_button)
startH_layout.addWidget(back_button)

startV_layout.addWidget(phase_label)
startV_layout.addWidget(time_label)
startV_layout.addWidget(count_label)
startV_layout.addLayout(startH_layout)
startV_layout.addStretch()

# СТРАНИЦА "НАСТРОЙКИ"
settings = QWidget()
settingsV_layout = QVBoxLayout(settings)

settings_label = QLabel("Настройки таймера")
settings_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
settings_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

# Поля для ввода
pomodoro_layout = QHBoxLayout()
pomodoro_label = QLabel("Длительность помидора (минуты):")
pomodoro_input = QLineEdit("25")
pomodoro_layout.addWidget(pomodoro_label)
pomodoro_layout.addWidget(pomodoro_input)

short_break_layout = QHBoxLayout()
short_break_label = QLabel("Короткий перерыв (минуты):")
short_break_input = QLineEdit("5")
short_break_layout.addWidget(short_break_label)
short_break_layout.addWidget(short_break_input)

long_break_layout = QHBoxLayout()
long_break_label = QLabel("Длинный перерыв (минуты):")
long_break_input = QLineEdit("15")
long_break_layout.addWidget(long_break_label)
long_break_layout.addWidget(long_break_input)

# Кнопки настроек
settings_buttons_layout = QHBoxLayout()
save_button = QPushButton("Сохранить")
back_settings_button = QPushButton("Меню")
settings_buttons_layout.addWidget(save_button)
settings_buttons_layout.addWidget(back_settings_button)

settingsV_layout.addWidget(settings_label)
settingsV_layout.addLayout(pomodoro_layout)
settingsV_layout.addLayout(short_break_layout)
settingsV_layout.addLayout(long_break_layout)
settingsV_layout.addLayout(settings_buttons_layout)
settingsV_layout.addStretch()

# Добавляем страницы в стек
stack.addWidget(main_page)
stack.addWidget(start)
stack.addWidget(settings)

main_layout.addWidget(stack)
window.setLayout(main_layout)


# Функции для работы таймера
def update_display():
    global remaining_time, current_phase
    minutes = remaining_time // 60
    seconds = remaining_time % 60
    time_label.setText(f"{minutes:02d}:{seconds:02d}")

    if current_phase == "работа":
        phase_label.setText("Текущая фаза: Работа")
    elif current_phase == "короткий перерыв":
        phase_label.setText("Текущая фаза: Короткий перерыв")
    else:
        phase_label.setText("Текущая фаза: Длинный перерыв")


def update_timer():
    global remaining_time, current_phase, pomodoro_count, is_running

    if remaining_time > 0:
        remaining_time -= 1
        update_display()
    else:
        timer.stop()

        if current_phase == "работа":
            pomodoro_count += 1
            count_label.setText(f"Выполнено помидоров: {pomodoro_count}")

            if pomodoro_count % cycles_before_long_break == 0:
                current_phase = "длинный перерыв"
                remaining_time = long_break_time
                msg = QMessageBox()
                msg.setText("Время длинного перерыва!")
                msg.exec()
            else:
                current_phase = "короткий перерыв"
                remaining_time = short_break_time
                msg = QMessageBox()
                msg.setText("Время короткого перерыва!")
                msg.exec()
        else:
            current_phase = "работа"
            remaining_time = pomodoro_time
            msg = QMessageBox()
            msg.setText("Перерыв закончен! Время работать!")
            msg.exec()

        update_display()
        is_running = False


def start_timer():
    global is_running
    if not is_running:
        is_running = True
        timer.start(1000)


def pause_timer():
    global is_running
    is_running = False
    timer.stop()


def reset_timer():
    global is_running, current_phase, remaining_time
    is_running = False
    timer.stop()
    current_phase = "работа"
    remaining_time = pomodoro_time
    update_display()


def save_settings():
    global pomodoro_time, short_break_time, long_break_time, remaining_time

    try:
        pomodoro_time = int(pomodoro_input.text()) * 60
        short_break_time = int(short_break_input.text()) * 60
        long_break_time = int(long_break_input.text()) * 60

        reset_timer()

        msg = QMessageBox()
        msg.setText("Настройки сохранены!")
        msg.exec()
    except ValueError:
        msg = QMessageBox()
        msg.setText("Пожалуйста, введите корректные числа!")
        msg.exec()


def go_to_menu():
    global is_running
    is_running = False
    timer.stop()
    stack.setCurrentIndex(0)


# Подключение сигналов
timer.timeout.connect(update_timer)

# Навигация
maint_start.clicked.connect(lambda: stack.setCurrentIndex(1))
main_settings.clicked.connect(lambda: stack.setCurrentIndex(2))
back_button.clicked.connect(go_to_menu)
back_settings_button.clicked.connect(go_to_menu)

# Управление таймером
start_button.clicked.connect(start_timer)
pause_button.clicked.connect(pause_timer)
reset_button.clicked.connect(reset_timer)

# Настройки
save_button.clicked.connect(save_settings)

# Отображение окна
window.show()

# Запуск приложения
sys.exit(app.exec())