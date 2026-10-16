.PHONY: setup test bench live clean
setup:
	pip install -r requirements.txt && pip install -e .
test:
	PYTHONPATH=src pytest -q
bench:
	PYTHONPATH=src python benchmarks/run_all.py --live --out results/summary.json
clean:
	rm -rf results/* __pycache__ .pytest_cache
