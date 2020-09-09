echo Running tests
WAS_FAILED=0
LABS=$(cat config/labs.txt)

if [[ -z ${LABS} ]]; then
  echo Skipping tests
  exit 0
fi

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
