echo 'Running Lint Check'
MINIMUM_LEVEL=9
FAILED=0

lint_output=$(pylint ./**/*.py)
echo "$lint_output"
score=$(echo "$lint_output" | grep -oP "Your code has been rated at \d+.\d+" | grep -oP "\d+")
echo "$score"
readarray -t score <<<"$score"
echo "$score"

if [[ $score -lt $MINIMUM_LEVEL ]]; then
  echo "Lint Check FAILED!"
  FAILED=1
  echo 'Lint Check Output:'
  echo "$lint_output"
fi

if [[ $FAILED -ne 0 ]]; then
  exit 1
fi

if [[ $score -ne 10 ]]; then
  echo 'Lint check passed but there are things to improve:'
  echo "$lint_output"
  exit 0
fi