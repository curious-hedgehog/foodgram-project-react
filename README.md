# praktikum_new_diplom

### Описание проекта:
Проект Foodgram представляет собой платформу для сбора отзывов пользователей на различные произведения, такие как книги, фильмы и музыка. Пользователи могут оставлять отзывы, ставить оценки и комментировать произведения. Проект реализован на основе Django, используя Django REST Framework для создания API.


### Как запустить проект:

1. Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone https://github.com/PepegaBoss/api_yamdb.git
cd api_yamdb
```

2. Создать и активировать виртуальное окружение:

```bash
python3 -m venv env
```

- Если у вас Linux/macOS:

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

### Загрузка данных из CSV-файлов:

Чтобы загрузить данные из CSV-файлов в базу данных проекта, выполните следующие шаги:

1. Убедитесь, что вы находитесь в корневой директории проекта `api_yamdb`.

2. Запустите команду загрузки данных из CSV-файлов с помощью следующей команды в терминале:

```bash
python manage.py load_data
```