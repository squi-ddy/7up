echo Running ISort...
isort .
echo

echo Running Black...
black --line-length 120 .
echo

echo Running Flake8...
flake8 --exclude ./venv .
echo