export PYTHONPATH="$(pwd)/lab_1:$(pwd)/lab_2:$(pwd)/lab_3:$(pwd)/lab_4:$(pwd):${PYTHONPATH}"
echo "Running start.py checks..."

LABS=$(cat config/labs.txt)
WAS_FAILED=0

for lab in $LABS; do
	echo "Running start.py checks for lab #${lab}"

	if ! python3 lab_"${lab}"/start.py;  then
    	WAS_FAILED=1
	  fi

	if [[ $WAS_FAILED -eq 1 ]]; then
	echo "start.py fails while running"
	echo "Check for start.py file for lab #${lab} failed."
	exit 1
  fi

  echo "Check calling lab #${lab} passed"

  START_PY_FILE=$(cat lab_"${lab}"/start.py)
  python3 config/check_start_content.py --start_py_content "$START_PY_FILE"
done
