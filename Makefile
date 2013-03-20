SETTINGS_FILE="settings.py"


run:
	@./bin/merchantd

setup: settings modules deps

settings:
	@cd merchants && \
		[ -e $(SETTINGS_FILE) ] || ln -s $(SETTINGS_FILE).sample $(SETTINGS_FILE)

modules:
	@mkdir -p modules && cd modules && \
	if [ -d yipit-static-assets/.git ]; then \
		cd yipit-static-assets && git pull; \
	else \
		git clone https://github.com/Yipit/yipit-static-assets.git; \
	fi

deps:
	@pip install -r requirements.txt


clean:
	find . -name *.pyc -delete



.PHONY: modules
