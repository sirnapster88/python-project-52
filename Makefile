install:
	uv sync

build:
	./build.sh

create-venv:
	uv venv

activate-venv:
	source .venv/bin/activate

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic

start:
	uv run python manage.py runserver

render-start:
	uv run python manage.py migrate
	uv run gunicorn task_manager.wsgi
	