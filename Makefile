install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

uninstall:
	python3 -m pip uninstall hexlet_code-0.1.0-py3-none-any.whl

migrations:
	poetry run python3 manage.py makemigrations

migrate:
	poetry run python3 manage.py migrate

collect:
	poetry run python3 manage.py collectstatic

run:
	poetry run python3 manage.py runserver 8080

test:
	poetry run python3 manage.py test

lint:
	poetry run flake8 labels
	poetry run flake8 statuses
	poetry run flake8 task_manager
	poetry run flake8 tasks
	poetry run flake8 users