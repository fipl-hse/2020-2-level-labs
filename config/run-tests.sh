export PYTHONPATH="$(pwd)/lab_1:$(pwd)/lab_2:$(pwd)/lab_3:$(pwd)/lab_4:$(pwd):${PYTHONPATH}"

echo Running tests
WAS_FAILED=0
LABS=$(cat config/labs.txt)

echo "$LABS"

for lab in $LABS; do
	echo "Running tests for lab #${lab}"
	if ! python3 -m unittest discover -p *_test.py -s lab_"${lab}";  then
    	WAS_FAILED=1
	fi
done

if [[ $WAS_FAILED -eq 1 ]]; then
	echo Tests failed
	exit 1
fi
