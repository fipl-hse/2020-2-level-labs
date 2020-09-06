echo running tests
WAS_FAILED=0
LABS=$(cat config/labs.txt)
echo "$LABS"

for lab in $LABS; do
	echo "Running tests for lab #${lab}"
	if ! python3 -m unittest discover -p *_test.py -s lab_"${lab}";  then
    	WAS_FAILED=1
	fi
done

if [[ "$WAS_FAILED" ]]; then
	echo tests failed
	return 1
fi