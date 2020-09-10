echo Running tests
WAS_FAILED=0
LABS=$(cat config/labs.txt)

echo "$LABS"

for lab in $LABS; do
	echo "Running tests for lab #${lab}"
	pushd lab_"${lab}" || exit 1
	if ! python3 -m unittest discover -p *_test.py;  then
    	WAS_FAILED=1
	fi
	popd || exit 1
done

if [[ $WAS_FAILED -eq 1 ]]; then
	echo Tests failed
	exit 1
fi
