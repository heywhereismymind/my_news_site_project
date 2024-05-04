# Начало работы с проектом:
> Клонировать репозиторий с GitHub

```
git clone https://github.com/heywhereismymind/my_news_site_project.git
```
> Перейти в созданную директорию проекта:
```
cd nywebsite
```
> Создать и активировать виртуальное окружение:
```
python -m venv venv
source venv/bin/activate
```
> Установить все необходимые зависимости из файла requirements.txt
```
pip install requirements.txt
```
> Выполнить миграции:
```
python manage.py makemigration
python manage.py migrate
```
> Запустить проект:
```
python manage.py runserver
```
> Запустить Redis:
```
docker run --rm --name redis -p 6379:6379 redis
```
