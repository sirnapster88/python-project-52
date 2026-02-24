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
	uvsync
	uv pip install -r requirements.txt
	uv run python manage.py migrate
	gunicorn task_manager.wsgi
	