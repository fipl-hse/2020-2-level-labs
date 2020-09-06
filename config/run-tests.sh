echo running tests
WAS_FAILED=false
LABS=`cat config/labs.txt`
echo "$LABS"

for i in $LABS; do
	echo "Running tests for lab #$i"
	if ! python3 -m unittest discover -p *_test.py -s lab_${i};  then
    	WAS_FAILED=true
	fi
done

if [ "$WAS_FAILED" = true ]; then
	echo tests failed
	return 1
fi