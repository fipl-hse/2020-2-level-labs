export PYTHONPATH="$(pwd)/lab_1:$(pwd)/lab_2:$(pwd)/lab_3:$(pwd)/lab_4:$(pwd):${PYTHONPATH}"

echo ''
echo 'Running lint check...'
LABS=$(cat config/labs.txt)

for lab in $LABS; do
	echo "Running lint for lab #${lab}"

  TARGET_SCORE=$(cat lab_"${lab}"/target_score.txt)

	lint_output=$(pylint lab_"${lab}")
  python3 config/lint_level.py --lint-output "$lint_output" --target-score $TARGET_SCORE
done

