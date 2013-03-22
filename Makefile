SETTINGS_FILE="settings.py"
PYTHONPATH=".:./modules/yipit-static-assets"

run:
	@PYTHONPATH=$(PYTHONPATH) ./bin/merchantd

setup: settings modules deps

settings:
	@cd merchants && \
		[ -e $(SETTINGS_FILE) ] || ln -s $(SETTINGS_FILE).sample $(SETTINGS_FILE)

modules:
	@mkdir -p modules && cd modules && \
	if [ -d yipit-static-assets/.git ]; then \
		cd yipit-static-assets && git pull; \
	else \
		git clone git@github.com:Yipit/yipit-static-assets.git; \
	fi

deps:
	@pip install -r requirements.txt


clean:
	find . -name *.pyc -delete

test:
	MERCHANTS_SETTINGS_MODULE="tests.settings" PYTHONPATH="$(PYTHONPATH)" \
		nosetests --stop --verbosity=2 -s tests

shell:
	@PYTHONPATH=$(PYTHONPATH) ./bin/merchantd shell

.PHONY: modules
