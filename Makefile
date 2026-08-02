.PHONY: install run clean build docker test lint

PYTHON := python3
PIP := $(PYTHON) -m pip

install:
	$(PIP) install --upgrade pip --break-system-packages || $(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt --break-system-packages || $(PIP) install -r requirements.txt

run:
	$(PYTHON) main.py

clean:
	rm -rf __pycache__ */__pycache__ *.pyc *.pyo
	rm -rf .pytest_cache build dist *.egg-info w0rm_gpt.egg-info
	rm -rf main.cpython-*.so _main_wrapper.py
	rm -f token.key wormgpt_config.json
	find . -type d -name "__pycache__" -exec rm -rf {} + || true

build:
	$(PIP) install build wheel --break-system-packages || $(PIP) install build wheel
	$(PYTHON) -m build --wheel --sdist
	@echo "Build complete: dist/"

# Build executable with PyInstaller (optional)
exe:
	$(PIP) install pyinstaller --break-system-packages || $(PIP) install pyinstaller
	pyinstaller --onefile --name wormgpt main.py
	@echo "Executable at dist/wormgpt"

docker:
	docker build -t worm-gpt:2.0 .

test:
	$(PYTHON) -c "import main; print('Import OK'); f=main.Functions; print('Encrypt/Decrypt:', f.Decryptdata(f.Encryptdata('test-sk')) )"

lint:
	$(PYTHON) -m py_compile main.py update.py
	@echo "Lint OK"

all: install test
