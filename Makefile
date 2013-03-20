run:
	@./bin/merchantd

setup: setup_modules setup_python_requirements

setup_modules:
	@mkdir -p modules && cd modules && \
	if [ -d yipit-static-assets/.git ]; then \
		cd yipit-static-assets && git pull; \
	else \
		git clone https://github.com/Yipit/yipit-static-assets.git; \
	fi

setup_python_requirements:
	@pip install -r requirements.txt
