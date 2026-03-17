from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import QTimer
import sys

# Переменные
text = "В чащах юга жил бы цитрус? Да, но фальшивый экземпляр!"  # Текст для ввода
time_left = 60  # Оставшееся время
timer_active = False  # Флаг активности таймера


# Функция запуска теста
def start_test():
    global time_left, timer_active  # Обращение к глобальным переменным
    input_line.setEnabled(True)  # Активация поля для ввода
    input_line.clear()  # Очистка поля для ввода

    # Установка значений по умолчанию
    time_left = 60
    timer_active = True

    # Показываем текст после начала теста
    text_label.setVisible(True)

    timer.start(1000)  # Обновление таймера
    start_button.setText("Тест активен...")  # Обновление текста стартовой кнопки
    start_button.setEnabled(False)  # Блокировка стартовой кнопки
    finish_button.setEnabled(True)  # Активация кнопки завершения


# Функция обновления таймера
def update_timer():
    global time_left, timer_active  # Обращение к глобальным переменным

    time_left -= 1  # Уменьшаем оставшееся время на единицу каждую секунду
    timer_label.setText(f"Оставшееся время: {time_left} сек.")  # Обновление надписи

    # Остановка таймера
    if time_left == 0:  # Если время истекло ...
        timer_active = False  # Обновляем флаг
        finish_test()  # Запуск функции подсчета результатов


# Функция завершения теста
def finish_test():
    global timer_active  # Обращение к глобальной переменной
    if timer_active:  # Если таймер активен...
        timer.stop()  # Останавливаем таймер
        timer_active = False  # Обновляем флаг
        input_line.setEnabled(False)  # Запрещаем ввод
        finish_button.setEnabled(False)  # Блокировка кнопки завершения
        calculate_results()  # Запуск функции подсчета результатов


# Функция подсчета результатов
def calculate_results():
    typed_text = input_line.text().strip()  # Получение введенного текста
    correct_text = text[:len(typed_text)]  # Получение эталона

    # Подсчет правильных символов
    correct = sum(1 for i in range(len(correct_text)) if correct_text[i] == typed_text[i])
    words = len(typed_text.split())  # Определение количества написанных слов

    # Расчет показателей скорости печати
    cpm = correct * (60 / (60 - time_left))  # Среднее количество правильно введённых символов в минуту
    wpm = words * (60 / (60 - time_left))  # Средняя скорость ввода слов в минуту

    # Отображение результатов
    cpm_label.setText(f"Символы в минуту: {int(cpm)}")
    wpm_label.setText(f"Слов в минуту: {int(wpm)}")

    # Повторный запуск теста
    start_button.setText("Начать заново")  # Изменяем текст кнопки начала
    start_button.setEnabled(True)  # Изменяем текст кнопки начала
    start_button.clicked.disconnect()  # Старый сигнал удаляется
    start_button.clicked.connect(reset_test)  # Активация функции сброса


# Функция сброса теста
def reset_test():
    input_line.setEnabled(False)  # Блокировка поля ввода
    input_line.clear()  # Очистка поля для ввода

    # Откат интерфейса
    cpm_label.setText("Символы в минуту: 0")
    wpm_label.setText("Слов в минуту: 0")
    timer_label.setText(f"Оставшееся время: {time_left} сек.")

    text_label.setVisible(False)  # Скрываем текст-задание

    start_button.clicked.disconnect()  # Старый сигнал удаляется
    start_button.clicked.connect(start_test)  # Привязка к функции старта


# Создание основного окна
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Тренажёр скорости печати")  # Заголовок окна
window.resize(700, 400)  # Размер окна

# Создаем вертикальный компоновщик
layout = QVBoxLayout()

# Создаем второстепенные компоновщики
stats_layout = QHBoxLayout()
button_layout = QHBoxLayout()

# Создаем интерфейс
text_label = QLabel(text)
input_line = QLineEdit()
timer_label = QLabel(f"Оставшееся время: {time_left} сек.")
cpm_label = QLabel("Символы в минуту: 0")
wpm_label = QLabel("Слов в минуту: 0")
start_button = QPushButton("Начать тест")
finish_button = QPushButton("Завершить тест")

# Настройки интерфейса
text_label.setVisible(False)  # Текст скрыт по умолчанию
input_line.setEnabled(False)  # Ввод недоступен по умолчанию
finish_button.setEnabled(False)  # Кнопка неактивна до начала теста

# Установка компоновщика
window.setLayout(layout)

# Добавляем элементы интерфейса
layout.addWidget(QLabel("Введите следующий текст:"))
layout.addWidget(text_label)
layout.addWidget(input_line)
stats_layout.addWidget(timer_label)
stats_layout.addWidget(cpm_label)
stats_layout.addWidget(wpm_label)
layout.addLayout(stats_layout)  # Установка второстепенного компоновщика
button_layout.addWidget(start_button)
button_layout.addWidget(finish_button)
layout.addLayout(button_layout)  # Установка второстепенного компоновщика

# Назначаем действия кнопкам
start_button.clicked.connect(start_test)
finish_button.clicked.connect(finish_test)

# Создаем таймер
timer = QTimer()
timer.timeout.connect(update_timer)

# Отображение окна
window.show()

# Запуск главного цикла приложения
app.exec()