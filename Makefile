install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

uninstall:
	python3 -m pip uninstall hexlet_code-0.1.0-py3-none-any.whl

run:
	python3 manage.py runserver

migrations:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate

test:
	python3 manage.py test