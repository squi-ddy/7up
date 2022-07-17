echo Running ISort...
isort .
echo

echo Running Black...
black --line-length 120 .
echo

echo Running Flake8...
flake8 --exclude ./venv .
echo

echo Running MyPy...
mypy src/
echo

echo Running pytest...
pytest --benchmark-autosave
echo