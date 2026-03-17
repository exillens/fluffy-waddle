# clicker_pyqt6_stack.py
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QProgressBar, QLabel, QStackedWidget, QGridLayout
)
from PyQt6.QtCore import Qt

def create_page(page_index):
    """
    Создает страницу с тремя кликерами и кнопкой сброса для этой страницы.
    Возвращает сам виджет страницы и список прогресс-баров этой страницы.
    """
    page = QWidget()
    layout = QVBoxLayout(page)

    title = QLabel(f"Страница {page_index + 1}")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(title)

    grid = QGridLayout()
    progress_bars = []

    # Для разнообразия шагов увеличения используем разные значения,
    # зависящие от номера кликера и страницы
    for i in range(3):
        step = 5 + (i + 1) * (5 + page_index * 2)  # варьируем шаг
        btn = QPushButton(f"Кликер {i + 1} (+{step}%)")
        pbar = QProgressBar()
        pbar.setRange(0, 100)
        pbar.setValue(0)

        # Привязываем обработчик к кнопке; используем аргументы по умолчанию,
        # чтобы избежать проблемы с поздней привязкой переменных в lambda
        btn.clicked.connect(lambda checked=False, pb=pbar, st=step: pb.setValue(min(100, pb.value() + st)))

        grid.addWidget(btn, i, 0)
        grid.addWidget(pbar, i, 1)

        progress_bars.append(pbar)

    layout.addLayout(grid)

    # Кнопка сброса прогресса для этой страницы
    reset_btn = QPushButton("Обнулить прогресс на странице")
    def reset_page():
        for pb in progress_bars:
            pb.setValue(0)
    reset_btn.clicked.connect(reset_page)
    layout.addWidget(reset_btn)

    return page, progress_bars

def main():
    app = QApplication(sys.argv)

    # Основное окно
    window = QWidget()
    window.setWindowTitle("Кликер с QStackedWidget (без ООП)")
    main_layout = QVBoxLayout(window)

    # Стек виджетов
    stacked = QStackedWidget()
    pages_progress = []  # сохраняем прогресс-бары всех страниц, если нужно

    for idx in range(3):
        page, pbars = create_page(idx)
        stacked.addWidget(page)
        pages_progress.append(pbars)

    main_layout.addWidget(stacked)

    # Навигация между страницами
    nav_layout = QHBoxLayout()

    prev_btn = QPushButton("Previous")
    next_btn = QPushButton("Next")

    def go_prev():
        cur = stacked.currentIndex()
        stacked.setCurrentIndex((cur - 1) % stacked.count())

    def go_next():
        cur = stacked.currentIndex()
        stacked.setCurrentIndex((cur + 1) % stacked.count())

    prev_btn.clicked.connect(go_prev)
    next_btn.clicked.connect(go_next)

    nav_layout.addWidget(prev_btn)

    # Кнопки для прямого перехода на страницу 1, 2, 3
    for i in range(3):
        btn = QPushButton(f"Страница {i + 1}")
        btn.clicked.connect(lambda checked=False, idx=i: stacked.setCurrentIndex(idx))
        nav_layout.addWidget(btn)

    nav_layout.addWidget(next_btn)

    main_layout.addLayout(nav_layout)

    # Глобальная кнопка обнуления всех прогрессов (если нужна)
    global_reset_btn = QPushButton("Обнулить все прогрессы")
    def reset_all():
        for page_pbars in pages_progress:
            for pb in page_pbars:
                pb.setValue(0)
    global_reset_btn.clicked.connect(reset_all)
    main_layout.addWidget(global_reset_btn)

    window.resize(480, 320)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()