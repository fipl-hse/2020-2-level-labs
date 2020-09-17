

echo Running lint
WAS_FAILED=0

PYTHONPATH="$(pwd)/lab_1:$(pwd)/lab_2:$(pwd)/lab_3:$(pwd)/lab_4:$(pwd):${PYTHONPATH}"
export PYTHONPATH

if ! python3 -m pylint ./**/*.py; then
  WAS_FAILED=1
fi
done

if [[ $WAS_FAILED -eq 1 ]]; then
	echo Lint failed
	exit 1
fi
