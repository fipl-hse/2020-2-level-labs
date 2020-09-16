echo Running tests
WAS_FAILED=0
LABS=$(cat config/labs.txt)

echo "$LABS"

for lab in $LABS; do
	echo "Running tests for lab #${lab}"

	TARGET_SCORE=$(cat lab_"${lab}"/target_score.txt)
	TARGET_TESTS=lab_"${lab}"/target_tests_"${TARGET_SCORE}".txt

	cat "$TARGET_TESTS" | while read test_file_name || [[ -n $test_file_name ]]
	do
	  echo "Running tests from $test_file_name"
	  if ! python3 -m unittest lab_"${lab}"/$test_file_name;  then
    	WAS_FAILED=1
	  fi
	done
done

if [[ $WAS_FAILED -eq 1 ]]; then
	echo "Tests failed."
	exit 1
fi
