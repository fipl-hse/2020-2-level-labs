export PYTHONPATH="$(pwd):lab_1:$(pwd):lab_2:$(pwd):lab_3:$(pwd):lab_4:$(pwd):${PYTHONPATH}"

echo 'Running lint check...'
MINIMUM_LEVEL=7
FAILED=0

lint_output=$(pylint ./**/*.py)
score=$(echo "$lint_output" | grep -oP "Your code has been rated at \d+.\d+" | grep -oP "\d+")
readarray -t score <<< "$score"

if [[ $score -lt $MINIMUM_LEVEL ]]; then
  echo "Lint Check FAILED!"
  FAILED=1
  echo ''
  echo 'Lint Check Output:'
  echo "$lint_output"
fi

if [[ $FAILED -ne 0 ]]; then
  exit 1
fi

if [[ $score -ne 10 ]]; then
  echo ''
  echo 'Lint check passed but there are things to improve:'
  echo "$lint_output"
  exit 0
fi