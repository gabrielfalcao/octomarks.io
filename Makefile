SETTINGS_FILE="settings.py"

all:
	@PYTHONPATH=$(PYTHONPATH) ./bin/gbookmarksd

setup: settings deps

settings:
	@cd gbookmarks && \
		[ -e $(SETTINGS_FILE) ] || ln -s $(SETTINGS_FILE).sample $(SETTINGS_FILE)

deps:
	@pip install -r requirements.txt

clean:
	find . -name *.pyc -delete

test:
	GBOOKMARKS_SETTINGS_MODULE="tests.settings" PYTHONPATH="$(PYTHONPATH)" \
		nosetests --stop --verbosity=2 -s tests

shell:
	@PYTHONPATH=$(PYTHONPATH) ./bin/gbookmarksd shell


%:
	@PYTHONPATH=$(PYTHONPATH) ./bin/gbookmarksd $@
