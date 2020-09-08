echo running check
WAS_FAILED=false
LABS=`cat config/labs.txt`
echo "$LABS"

for i in $LABS; do
	echo "$i"
	if ! python3 config/plagiarism_check.py --source-dir lab_${i}/ --others-dir tmp/lab_${i};  then
    	WAS_FAILED=true
	fi
done

if [ "$WAS_FAILED" = true ]; then
	echo plagiarism failed
	return 1
fi