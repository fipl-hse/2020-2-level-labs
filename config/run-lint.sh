export PYTHONPATH="$(pwd):lab_1:$(pwd):lab_2:$(pwd):lab_3:$(pwd):lab_4:$(pwd):${PYTHONPATH}"

echo 'Running lint check...'
MINIMUM_LEVEL=7

lint_output=$(pylint ./**/*.py)
lint_parser_exit=$(python3 config/lint_level.py --lint-output "$lint_output" --lint-level $MINIMUM_LEVEL)

exit $lint_parser_exit
