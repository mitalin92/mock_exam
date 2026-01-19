check:
	uv pip install -r requirements.txt
	ruff format .
	ruff check .
	mypy .
	pre-commit run --all-files

ingest-logs:
	python src/usecases/ingest_logs.py