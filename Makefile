PYTHON_VERSION = 3.12
VENV_NAME = venv
PIP = $(VENV_NAME)/Scripts/pip
PYTHON = $(VENV_NAME)/Scripts/python
PYTEST = $(VENV_NAME)/Scripts/pytest
UVICORN = $(VENV_NAME)/Scripts/uvicorn
REQUIREMENTS_FILE = requirements.txt
MAIN_APP = main:app
HOST = 0.0.0.0
PORT = 8000
FIND = find . -type f -name

# Create the virtual environment
venv:
	python -m venv $(VENV_NAME)

# Activate the virtual environment (instruction only, does not execute automatically)
activate-venv:
	@echo "Activate the virtual environment with: source $(VENV_NAME)/Scripts/activate (on macOS/Linux) or .\\$(VENV_NAME)\\Scripts\\activate (on Windows)"

# Install dependencies from requirements.txt
install-deps: venv
	$(PIP) install -r $(REQUIREMENTS_FILE)

# Dump current dependencies to requirements.txt
freeze-deps:
	$(PIP) freeze > $(REQUIREMENTS_FILE)

# Run the app locally with auto-reload
run-dev: venv install-deps
	$(UVICORN) $(MAIN_APP) --host $(HOST) --port $(PORT) --reload

# Run the app locally without auto-reload
run: venv install-deps
	$(UVICORN) $(MAIN_APP) --host $(HOST) --port $(PORT)

# Run tests with pytest
test: venv install-deps
	$(PYTEST)

# Run tests with coverage
test-cov: venv install-deps
	$(PYTEST) --cov=. --cov-report term-missing

# Format code with black
format: venv install-deps
	$(PIP) install --upgrade black
	black . --exclude=$(VENV_NAME)

# Lint code with flake8
lint: venv install-deps
	$(PIP) install --upgrade flake8
	flake8 . --exclude=$(VENV_NAME)

# Run formatting and linting
check: format lint

# Clean up temporary and junk files
clean:
	@echo "Cleaning temporary and junk files..."
	$(FIND) "__pycache__" -delete
	$(FIND) "*.pyc" -delete
	$(FIND) "*.log" -delete
	$(FIND) ".pytest_cache" -type d -exec rm -rf {} +
	rm -rf $(VENV_NAME)
	@echo "Cleanup completed."

# Terraform-related tasks (examples only, adapt to your GCP setup)
terraform-init:
	terraform init

terraform-plan:
	terraform plan

terraform-apply:
	terraform apply -auto-approve

terraform-destroy:
	terraform destroy -auto-approve

.PHONY: venv activate-venv install-deps freeze-deps run run-dev test test-cov format lint check terraform-init terraform-plan terraform-apply terraform-destroy