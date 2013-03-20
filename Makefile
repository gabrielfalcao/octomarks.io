run:
	@./bin/merchantd

setup: setup_modules setup_python_requirements

setup_modules:
	@mkdir -p modules
	@cd modules && git clone https://github.com/Yipit/yipit-static-assets.git

setup_python_requirements:
	@pip install -r requirements.txt
