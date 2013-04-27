SETTINGS_FILE="settings.py"
export OCTOMARK_TESTING_MODE=on

all: prepare test local-migrate-forward

prepare:
	@pip install -r development.txt

clean:
	find . -name *.pyc -delete

test-kind:
	@OCTOMARKS_SETTINGS_MODULE="tests.settings" PYTHONPATH="$(PYTHONPATH)" \
		nosetests --nologcapture --logging-clear-handlers --stop --verbosity=2 -s tests/$(kind)

unit:
	@make test-kind kind=unit
functional:
	@make test-kind kind=functional

acceptance:
	@lettuce

test: unit functional acceptance


shell:
	@PYTHONPATH=$(PYTHONPATH) ./bin/flaskd shell

deploy: test
	@git push --force heroku master
	@heroku run "/app/.heroku/python/bin/alembic -c alembic.prod.ini upgrade head"
	@make release
	@make migrate-forward

local-migrate-forward:
	@alembic upgrade head

local-migrate-back:
	@alembic downgrade -1

migrate-back:
	@heroku run "/app/.heroku/python/bin/alembic -c alembic.prod.ini downgrade -1"

migrate-forward:
	@heroku run "/app/.heroku/python/bin/alembic -c alembic.prod.ini upgrade head"

release:
	@heroku config:set RELEASE=`git rev-parse HEAD`

run:
	@./bin/flaskd run
