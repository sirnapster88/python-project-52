install:
	uv sync

build:
	./build.sh

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic

start:
	uv run python manage.py runserver

render-start:
	gunicorn task_manager.wsgi
	uv pip install -r requirements.txt
	uv run python manage.py migrate