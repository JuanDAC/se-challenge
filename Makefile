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

# Crear el entorno virtual
venv:
	python -m venv $(VENV_NAME)

# Activar el entorno virtual (solo instrucción, no se ejecuta automáticamente)
activate-venv:
	@echo "Activa el entorno virtual con: source $(VENV_NAME)/Scripts/activate (en macOS/Linux) o .\\$(VENV_NAME)\\Scripts\\activate (en Windows)"

# Instalar las dependencias del archivo requirements.txt
install-deps: venv
	$(PIP) install -r $(REQUIREMENTS_FILE)

# Volcar las dependencias actuales al archivo requirements.txt
freeze-deps:
	$(PIP) freeze > $(REQUIREMENTS_FILE)

# Ejecutar la aplicación en local con recarga automática
run-dev: venv install-deps
	$(UVICORN) $(MAIN_APP) --host $(HOST) --port $(PORT) --reload

# Ejecutar la aplicación en local sin recarga automática
run: venv install-deps
	$(UVICORN) $(MAIN_APP) --host $(HOST) --port $(PORT)

# Ejecutar las pruebas con pytest
test: venv install-deps
	$(PYTEST)

# Ejecutar las pruebas con cobertura
test-cov: venv install-deps
	$(PYTEST) --cov=. --cov-report term-missing

# Formatear el código con black
format: venv install-deps
	$(PIP) install --upgrade black
	black .

# Analizar el código con flake8
lint: venv install-deps
	$(PIP) install --upgrade flake8
	flake8 .

# Ejecutar formateo y linting
check: format lint

# Tareas relacionadas con Terraform (solo ejemplos, debes adaptarlos a tu configuración de GCP)
terraform-init:
	terraform init

terraform-plan:
	terraform plan

terraform-apply:
	terraform apply -auto-approve

terraform-destroy:
	terraform destroy -auto-approve

.PHONY: venv activate-venv install-deps freeze-deps run run-dev test test-cov format lint check terraform-init terraform-plan terraform-apply terraform-destroy