export PYTHONPATH="$(pwd)/lab_1:$(pwd)/lab_2:$(pwd)/lab_3:$(pwd)/lab_4:$(pwd):${PYTHONPATH}"
echo "Running tests..."
WAS_FAILED=0
LABS=$(cat config/labs.txt)

echo "Current scope: $LABS"

for lab in $LABS; do
	echo "Running tests for lab #${lab}"

	TARGET_SCORE=$(cat lab_"${lab}"/target_score.txt)
	if [[ ${TARGET_SCORE} == 10 && ${lab} == 2 ]]; then
	  gdown https://drive.google.com/uc?id=1MJLg8H6SfAoBnOUHqxIRvanSWNb1vm3B -O lab_2/data.txt
	  gdown https://drive.google.com/uc?id=1dETiLw3yYCLf1R729xlLiCbUZGPBhCYr -O lab_2/data_2.txt
	fi

	TARGET_TESTS=config/lab_"${lab}"/target_tests_"${TARGET_SCORE}".txt

	while read test_file_name || [[ -n $test_file_name ]]
	do
	  echo "Running tests from $test_file_name"
	  if ! python3 -m unittest lab_"${lab}"/$test_file_name;  then
    	WAS_FAILED=1
	  fi
	done <<< "$(cat "$TARGET_TESTS")"
done

if [[ $WAS_FAILED -eq 1 ]]; then
	echo "Tests failed."
	exit 1
fi
