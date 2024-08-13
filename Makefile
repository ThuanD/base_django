.PHONY: init update-deps secret_key static migrate cache test run-hooks run gunicorn shell
init:
	poetry install --no-root --all-extras

update-deps:
	poetry update

secret_key:
	poetry run python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

static:
	poetry run python manage.py collectstatic --no-input

migrate:
	poetry run python manage.py migrate

cache:
	poetry run python manage.py createcachetable

test:
	poetry run coverage run --source='.' manage.py test --settings=app.settings.local_test
	poetry run coverage html

run-hooks:
	poetry run pre-commit run --all-files --show-diff-on-failure

run:
	poetry run python manage.py runserver

gunicorn:
	poetry run gunicorn app.wsgi:application -b 0.0.0.0:8000 --timeout 300 --reload

shell:
	poetry run python manage.py shell_plus
