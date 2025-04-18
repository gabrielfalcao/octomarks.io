SETTINGS_FILE="settings.py"
export OCTOMARK_TESTING_MODE=on

all: prepare test local-migrate-forward

prepare:
	@pip install -r development.txt

clean:
	find . -name *.pyc -delete

test-kind:
	@OCTOMARKS_DB=mysql://root@localhost/gb_test OCTOMARKS_SETTINGS_MODULE="tests.settings" PYTHONPATH="$(PYTHONPATH)" \
		nosetests --nologcapture --logging-clear-handlers --stop --verbosity=2 -s tests/$(kind)

unit:
	@make test-kind kind=unit
functional:
	@make test-kind kind=functional

acceptance:
	@lettuce --tag=-later

test: unit functional acceptance


shell:
	@PYTHONPATH=$(PYTHONPATH) ./bin/flaskd shell

deploy: test
	@git push --force heroku master
	@heroku run "/app/.heroku/python/bin/alembic -c alembic.prod.ini upgrade head"
	@make release
	@make migrate-forward

local-migrate-forward:
	@[ "$(reset)" == "yes" ] && echo "drop database gb;create database gb" | mysql -uroot || echo "Running new migrations..."
	@alembic upgrade head

local-migrate-back:
	@alembic downgrade -1

production-dump.sql:
	@printf "Getting production dump... "
	@mysqldump -u gbookmarks --password='b00k@BABY' -h mysql.gabrielfalcao.com gbookmarks > production-dump.sql
	@echo "OK"
	@echo "Saved at production-dump.sql"

migrate-back:
	@heroku run "/app/.heroku/python/bin/alembic -c alembic.prod.ini downgrade -1"

migrate-forward:
	@heroku run "/app/.heroku/python/bin/alembic -c alembic.prod.ini upgrade head"

release:
	@heroku config:set RELEASE=`git rev-parse HEAD`

run:
	@./bin/flaskd run
