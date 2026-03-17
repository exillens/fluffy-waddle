# Импорт
import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, \
    QListWidget, QStackedWidget, QMessageBox, QListWidgetItem
from PyQt6.QtCore import Qt

# ШАГ 1 Подключиться к БД
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


# Функция загрузки рецептов
def load_recipes():
    recipe_list.clear()  # Очистка существующего списка рецептов
    cursor.execute("SELECT id, name FROM recipes")  # Выполнение SQL-запроса

    for row in cursor.fetchall():  # Для каждого ряда результата запроса...
        recipe_list.addItem(f"{row[1]} (ID: {row[0]})")  # Создание записи


# Функция добавления ингредиентов
def add_ingredient():
    name = ingredient_name_input.text().strip()  # Получение имени ингредиента
    amount = ingredient_amount_input.text().strip()  # Получение количества ингредиента

    if name and amount:  # Если оба значения (name и amount) заполнены...
        ingredients_list.addItem(f"{name} - {amount}")  # Добавление нового элемента в список
        ingredient_name_input.clear()  # Очистка поля для ввода
        ingredient_amount_input.clear()  # Очистка поля для ввода


# Функция просмотра рецепта
def show_recipe(item):
    selected = item.text()  # Получение названия рецепта
    recipe_id = int(selected.split("(ID: ")[1].rstrip(")"))  # Извлечение ID

    cursor.execute("SELECT name, ingredients, steps FROM recipes WHERE id=?", (recipe_id,))  # Выполнение SQL-запроса
    recipe = cursor.fetchone()  # Выполнение SQL-запроса

    # Вывод рецепта
    if recipe:  # Если репецт существует...
        recipe_details_label.setText(f"<h2>{recipe[0]}</h2>")  # Название рецепта крупным заголовком
        ingredients_html = "<br>".join(recipe[1].split("\n")) if recipe[1] else ""  # Ингредиенты разбиваются по строкам
        steps_html = "<br>".join(recipe[2].split("\n")) if recipe[2] else ""  # Шаги также аналогично разбиваются
        recipe_details_ingredients.setText(
            "<b>Ингредиенты:</b><br>" + ingredients_html)  # Информация выводится в соответствующие виджеты интерфейса
        recipe_details_steps.setText(
            "<b>Шаги:</b><br>" + steps_html)  # Информация выводится в соответствующие виджеты интерфейса

    stack.setCurrentIndex(2)  # Переход на страницу с деталями рецепта


# Функция добавления нового рецепта
def add_recipe():
    name = recipe_name_input.text().strip()  # Получение названия рецепта
    steps = recipe_steps_input.toPlainText().strip()  # Получение шагов приготовления

    # Собираем ингредиенты из списка
    ingredients = []  # Пустой список для сбора ингредиентов

    for i in range(ingredients_list.count()):  # Для каждого ингредиента
        item = ingredients_list.item(i)  # Берём очередной элемент из списка ингредиентов
        ingredients.append(item.text())  # Получаем текст ингредиента и добавляем его в наш список
    ingredients_text = "\n".join(ingredients)  # Объединяем все собранные ингредиенты в одну строку

    # Формируем SQL-запрос на добавление рецепта в базу данных
    cursor.execute("INSERT INTO recipes (name, ingredients, steps) VALUES (?, ?, ?)",
                   (name, ingredients_text, steps))
    conn.commit()  # Сохраняем сделанные изменения в базе данных

    recipe_name_input.clear()  # Чистим поле ввода
    ingredients_list.clear()  # Удаляем все ингредиенты из списка
    recipe_steps_input.clear()  # Чистим поле ввода
    load_recipes()  # Обновляем список рецептов
    stack.setCurrentIndex(0)  # Меняем текущую страницу на главную


# Создание основного окна
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Библиотека рецептов')  # Заголовок окна
window.resize(500, 400)  # Размер окна

# Подготовка
stack = QStackedWidget()
main_layout = QVBoxLayout()

# СТРАНИЦА "Все рецепты"
all_recipes_page = QWidget()  # Создание страницы
all_recipes_layout = QVBoxLayout()  # Создание вертикальной (основной) компоновки

# Виджеты страницы
recipe_list = QListWidget()
add_recipe_button = QPushButton("Добавить рецепт")

# Добавление виджетов на страницу
all_recipes_layout.addWidget(recipe_list)
all_recipes_layout.addWidget(add_recipe_button)

# Установка компановки
all_recipes_page.setLayout(all_recipes_layout)

# Подключение кнопок
recipe_list.itemClicked.connect(show_recipe)
add_recipe_button.clicked.connect(lambda: stack.setCurrentIndex(1))

# СТРАНИЦА "Добавление рецепта"
add_recipe_page = QWidget()  # Создание страницы
add_recipe_layout = QVBoxLayout()  # Создание вертикальной (основной) компоновки
ingredient_input_layout = QHBoxLayout()  # Создание горизонтальной (второстепенной) компоновки

# Виджеты страницы
recipe_name_input = QLineEdit()
ingredient_name_input = QLineEdit()
ingredient_amount_input = QLineEdit()
add_ingredient_button = QPushButton("Добавить")
ingredients_list = QListWidget()
recipe_steps_input = QTextEdit()
save_button = QPushButton("Сохранить рецепт")
back_button = QPushButton("Назад к списку")

# Плейсхолдеры
recipe_name_input.setPlaceholderText("Название рецепта")
ingredient_name_input.setPlaceholderText("Ингредиент (например: Молоко)")
ingredient_amount_input.setPlaceholderText("Количество (например: 200 мл)")
recipe_steps_input.setPlaceholderText("Шаги приготовления")

# Добавление виджетов на страницу
add_recipe_layout.addWidget(recipe_name_input)
ingredient_input_layout.addWidget(ingredient_name_input)
ingredient_input_layout.addWidget(ingredient_amount_input)
ingredient_input_layout.addWidget(add_ingredient_button)
add_recipe_layout.addLayout(ingredient_input_layout)  # Установка компановки
add_recipe_layout.addWidget(ingredients_list)
add_recipe_layout.addWidget(recipe_steps_input)
add_recipe_layout.addWidget(save_button)
add_recipe_layout.addWidget(back_button)

# Установка компановки
add_recipe_page.setLayout(add_recipe_layout)

# Подключение кнопок
add_ingredient_button.clicked.connect(add_ingredient)
save_button.clicked.connect(add_recipe)
back_button.clicked.connect(lambda: stack.setCurrentIndex(0))

# СТРАНИЦА "Просмотр рецепта"
view_recipe_page = QWidget()  # Создание страницы
view_recipe_layout = QVBoxLayout()  # Создание вертикальной компоновки

# Виджеты страницы
recipe_details_label = QLabel()
recipe_details_ingredients = QLabel()
recipe_details_steps = QLabel()
back_to_list_button = QPushButton("Назад к списку")

# Добавление виджетов на страницу
view_recipe_layout.addWidget(recipe_details_label)
view_recipe_layout.addWidget(recipe_details_ingredients)
view_recipe_layout.addWidget(recipe_details_steps)
view_recipe_layout.addWidget(back_to_list_button)

# Установка компановки
view_recipe_page.setLayout(view_recipe_layout)

# Подключение кнопок
back_to_list_button.clicked.connect(lambda: stack.setCurrentIndex(0))

# Добавляем страницы в стек
stack.addWidget(all_recipes_page)
stack.addWidget(add_recipe_page)
stack.addWidget(view_recipe_page)

# Установка компановки
window.setLayout(main_layout)

# main_layout.addWidget(stack)

# Добавляем QStackedWidget на основную страницу
window.layout().addWidget(stack)

# Отображение окна
window.show()
load_recipes()

# Запуск главного цикла приложения
app.exec()
