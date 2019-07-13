clean: clean-eggs clean-build
	@find . -iname '*.pyc' -delete
	@find . -iname '*.pyo' -delete
	@find . -iname '*~' -delete
	@find . -iname '*.swp' -delete
	@find . -iname '__pycache__' -delete

clean-eggs:
	@find . -name '*.egg' -print0|xargs -0 rm -rf --
	@rm -rf .eggs/

clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info

collectstatic:
	python jsonbox-api/manage.py collectstatic

lint:
	pipenv run pre-commit install && pipenv run pre-commit run -a -v

pyformat:
	pipenv run black .

test:
	pipenv run pytest -x -s jsonbox-api

check-dead-fixtures:
	pipenv run pytest --dead-fixtures jsonbox-api

install:
	pipenv install --dev
