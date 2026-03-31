import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
                             QVBoxLayout, QWidget, QHBoxLayout, QDialog,
                             QDialogButtonBox)
from PyQt6.QtCore import Qt


class BoosterDialog(QDialog):
    def __init__(self, booster_name, cost, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Купить бустер {booster_name}")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        label = QLabel(f"Купить бустер {booster_name} за {cost} монет?")
        layout.addWidget(label)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Yes |
                                   QDialogButtonBox.StandardButton.No)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)


class StoryDialog(QDialog):
    def __init__(self, message, buttons_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Сюжет")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()

        label = QLabel(message)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        button_layout = QHBoxLayout()
        for text in buttons_text:
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, t=text: self.on_button_click(t))
            button_layout.addWidget(btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.result = None

    def on_button_click(self, text):
        self.result = text
        self.accept()


class ClickerGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.coins = 0
        self.boosters = {1: False, 5: False, 10: False}
        self.total_clicks = 0
        self.showed_stories = set()
        self.boost1_unlocked = False
        self.boost5_unlocked = False
        self.boost10_unlocked = False

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Кликер - Путь к бабушке")
        self.setFixedSize(400, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        # Монеты за клик (ПЕРЕМЕЩЕНО В САМЫЙ ВЕРХ)
        self.click_value_label = QLabel("За клик: 1 монета")
        self.click_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.click_value_label.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #FFD700; background-color: rgba(0,0,0,0.1); padding: 10px; border-radius: 10px;")
        layout.addWidget(self.click_value_label)

        # Количество монет
        self.coins_label = QLabel("Монеты: 0")
        self.coins_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.coins_label.setStyleSheet("font-size: 24px; font-weight: bold; color: gold;")
        layout.addWidget(self.coins_label)

        # Кнопка кликер
        self.click_button = QPushButton("КЛИК!")
        self.click_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 32px;
                font-weight: bold;
                border: none;
                border-radius: 15px;
                padding: 20px;
            }
            QPushButton:pressed {
                background-color: #45a049;
            }
        """)
        self.click_button.clicked.connect(self.on_click)
        layout.addWidget(self.click_button)

        # Сброс прогресса
        self.reset_button = QPushButton("Сброс прогресса")
        self.reset_button.clicked.connect(self.reset_progress)
        layout.addWidget(self.reset_button)

        # Контейнер для бустеров
        self.boosters_container = QWidget()
        self.boosters_layout = QHBoxLayout()
        self.boosters_container.setLayout(self.boosters_layout)
        layout.addWidget(self.boosters_container)

        # Изначально скрываем контейнер бустеров
        self.boosters_container.hide()

        self.central_widget.setLayout(layout)
        self.update_boosters_display()
        self.update_click_value_display()

    def get_click_value(self):
        """Вычисляет текущее значение клика"""
        click_value = 1
        if self.boosters[1]:
            click_value += 1
        if self.boosters[5]:
            click_value += 5
        if self.boosters[10]:
            click_value += 10
        return click_value

    def update_click_value_display(self):
        """Обновляет отображение монет за клик"""
        click_value = self.get_click_value()
        self.click_value_label.setText(f"За клик: {click_value} монет")

    def on_click(self):
        click_value = self.get_click_value()

        self.coins += click_value
        self.total_clicks += 1
        self.coins_label.setText(f"Монеты: {self.coins}")
        self.update_click_value_display()

        self.check_story_events()

    def check_story_events(self):
        if self.total_clicks == 5 and 5 not in self.showed_stories:
            self.show_story("Привет, твой персонаж отправляется до бабушки!", ["Продолжить"])
            self.showed_stories.add(5)

        elif self.total_clicks == 15 and 15 not in self.showed_stories:
            self.show_story("Ты шел по тропинке и на тебя напал дракон!\nЧтобы отбиться добей до 40 кликов",
                            ["Попытаться скрыться от дракона"])
            self.showed_stories.add(15)

        elif self.total_clicks == 40 and 40 not in self.showed_stories:
            self.boost1_unlocked = True
            self.show_story("Поздравляю, вы одолели дракона!\nТеперь доступен буст +1 за 25 монет",
                            ["Продолжить"])
            self.update_boosters_display()
            self.showed_stories.add(40)

        elif self.total_clicks == 90 and 90 not in self.showed_stories:
            dialog = self.show_story("Не устал кликать?", ["Не устал", "Устал"])
            if dialog.result == "Устал":
                self.show_story("Но ты же до сих пор кликаешь :)", ["Кликать дальше"])
            self.showed_stories.add(90)

        elif self.total_clicks == 100 and 100 not in self.showed_stories:
            self.boost5_unlocked = True
            self.show_story("Теперь доступен буст +5 за 50 монет!", ["Продолжить"])
            self.update_boosters_display()
            self.showed_stories.add(100)

        elif self.total_clicks == 150 and 150 not in self.showed_stories:
            self.boost10_unlocked = True
            self.show_story("Теперь доступен буст +10 за 100 монет!", ["Продолжить"])
            self.update_boosters_display()
            self.showed_stories.add(150)

        elif self.total_clicks == 300 and 300 not in self.showed_stories:
            self.show_story("УРА! Вы дошли до бабушки!", ["Конец игры"])
            self.reset_progress()
            self.showed_stories.add(300)

    def show_story(self, message, buttons_text):
        dialog = StoryDialog(message, buttons_text, self)
        dialog.exec()
        return dialog

    def update_boosters_display(self):
        # Очищаем layout
        while self.boosters_layout.count():
            child = self.boosters_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Добавляем кнопки только разблокированных бустеров
        if self.boost1_unlocked:
            self.boost1_btn = QPushButton("Буст+1: нет")
            self.boost1_btn.clicked.connect(lambda: self.buy_booster(1, 25))
            self.boosters_layout.addWidget(self.boost1_btn)

        if self.boost5_unlocked:
            self.boost5_btn = QPushButton("Буст+5: нет")
            self.boost5_btn.clicked.connect(lambda: self.buy_booster(5, 50))
            self.boosters_layout.addWidget(self.boost5_btn)

        if self.boost10_unlocked:
            self.boost10_btn = QPushButton("Буст+10: нет")
            self.boost10_btn.clicked.connect(lambda: self.buy_booster(10, 100))
            self.boosters_layout.addWidget(self.boost10_btn)

        # Обновляем состояние купленных бустеров
        if hasattr(self, 'boost1_btn'):
            self.boost1_btn.setText("Буст+1: " + ("есть" if self.boosters[1] else "нет"))
            self.boost1_btn.setEnabled(not self.boosters[1])

        if hasattr(self, 'boost5_btn'):
            self.boost5_btn.setText("Буст+5: " + ("есть" if self.boosters[5] else "нет"))
            self.boost5_btn.setEnabled(not self.boosters[5])

        if hasattr(self, 'boost10_btn'):
            self.boost10_btn.setText("Буст+10: " + ("есть" if self.boosters[10] else "нет"))
            self.boost10_btn.setEnabled(not self.boosters[10])

        # Показываем контейнер если есть хотя бы один бустер
        self.boosters_container.setVisible(
            self.boost1_unlocked or self.boost5_unlocked or self.boost10_unlocked
        )

        # Обновляем отображение кликов после изменения бустеров
        self.update_click_value_display()

    def buy_booster(self, boost_value, cost):
        if self.coins < cost:
            self.show_story(f"Недостаточно монет! Нужно {cost}", ["OK"])
            return

        dialog = BoosterDialog(f"+{boost_value}", cost, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.coins -= cost
            self.boosters[boost_value] = True
            self.coins_label.setText(f"Монеты: {self.coins}")
            self.update_boosters_display()

    def reset_progress(self):
        self.coins = 0
        self.total_clicks = 0
        self.boosters = {1: False, 5: False, 10: False}
        self.showed_stories = set()
        self.boost1_unlocked = False
        self.boost5_unlocked = False
        self.boost10_unlocked = False
        self.coins_label.setText("Монеты: 0")
        self.update_boosters_display()


def main():
    app = QApplication(sys.argv)
    game = ClickerGame()
    game.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()