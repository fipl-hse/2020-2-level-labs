export PYTHONPATH="$(pwd):lab_1:$(pwd):lab_2:$(pwd):lab_3:$(pwd):lab_4:$(pwd):${PYTHONPATH}"

echo ''
echo 'Running lint check...'
MINIMUM_LEVEL=10

lint_output=$(pylint ./**/*.py)
python3 config/lint_level.py --lint-output "$lint_output" --lint-level $MINIMUM_LEVEL
