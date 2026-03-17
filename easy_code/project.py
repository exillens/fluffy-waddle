import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget, QStackedWidget, QMessageBox, QListWidgetItem
from PyQt6.QtCore import Qt

conn = sqlite3.connect("recipes.db")
cursor = conn.cursor()
cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ingredients TEXT,
            steps TEXT
        )
    """)


conn.commit()

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('кликеры') # Заголовок окна
window.resize(500, 400) # Размер окна

# Подготовка
stack = QStackedWidget()
main_layout = QVBoxLayout()


