# Foodgram

### Описание проекта:
Foodgram представляет собой платформу для публикования рецептов блюд.
Рецепты можно добавлять в избранное и список покупок.
Проект реализован на основе Django, используя Django REST Framework для создания API.
 
### Как запустить проект:

1. Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone git@github.com:BadChemist/foodgram-project-react.git
cd foodgram-project-react
```

2. Создать и активировать виртуальное окружение:

```bash
python3 -m venv env
```

- Если у вас Linux/MacOS:

```bash
source env/bin/activate
```

- Если у вас Windows:

```bash
source env/scripts/activate
```

3. Обновить pip и установить зависимости из файла requirements.txt:

```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Выполнить миграции:

```bash
python3 manage.py migrate
```

5. Запустить проект:

```bash
python3 manage.py runserver
```

### Импорт ингредиентов:

Загрузить список ингредиентов в базу данных проекта можно с помощью команды:

```bash
python manage.py loadingredients
```
