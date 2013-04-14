SETTINGS_FILE="settings.py"

all:
	@PYTHONPATH=$(PYTHONPATH) ./bin/flaskd

setup: settings deps

settings:
	@cd gbookmarks && \
		[ -e $(SETTINGS_FILE) ] || ln -s $(SETTINGS_FILE).sample $(SETTINGS_FILE)

deps:
	@pip install -r requirements.txt

clean:
	find . -name *.pyc -delete

test-kind:
	@GBOOKMARKS_SETTINGS_MODULE="tests.settings" PYTHONPATH="$(PYTHONPATH)" \
		nosetests --logging-clear-handlers --stop --verbosity=2 -s tests/$(kind)

unit:
	@make test-kind kind=unit
functional:
	@make test-kind kind=functional

test: unit, functional


shell:
	@PYTHONPATH=$(PYTHONPATH) ./bin/flaskd shell

deploy:
	@git push heroku master
	@heroku alembic -c alembic.prod.ini upgrade head
	@make release

release:
	@heroku config:set RELEASE=`git rev-parse HEAD`

%:
	@PYTHONPATH=$(PYTHONPATH) ./bin/flaskd $@
