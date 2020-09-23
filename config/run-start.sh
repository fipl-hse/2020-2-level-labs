export PYTHONPATH="$(pwd)/lab_1:$(pwd)/lab_2:$(pwd)/lab_3:$(pwd)/lab_4:$(pwd):${PYTHONPATH}"
echo "Running start.py checks..."

LABS=$(cat config/labs.txt)

for lab in $LABS; do
	echo "Running start.py checks for lab #${lab}"

  START_PY_FILE=$(cat lab_"${lab}"/start.py)
  python3 config/start_py_test.py --start_py_content "$START_PY_FILE"

done
