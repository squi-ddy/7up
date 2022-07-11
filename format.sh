isort .
black --line-length 120 .
flake8 --exclude ./venv .
mypy .