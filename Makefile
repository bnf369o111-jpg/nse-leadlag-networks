data:
	python src/data/download.py
	python src/data/clean.py

test:
	pytest -q