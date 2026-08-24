pip = .venv/bin/pip
python = .venv/bin/python
flake8 = .venv/bin/flake8
mypy = .venv/bin/mypy

.PHONY: install run debug clean lint lint-strict

install:
	python3 -m venv .venv
	$(pip) install -r requirements.txt

run:
	$(python) main.py

debug:
	$(python) -m pdb main.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	$(flake8) . --exclude=.venv
	$(mypy) . --warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--exclude='^\.venv/'

lint-strict:
	$(flake8) . --exclude=.venv
	$(mypy) . --strict --exclude='^\.venv/'