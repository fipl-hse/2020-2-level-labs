export PYTHONPATH="$(pwd)/lab_1:$(pwd)/lab_2:$(pwd)/lab_3:$(pwd)/lab_4:$(pwd):${PYTHONPATH}"
echo "Running plagiarism check..."

echo "${TRAVIS_PULL_REQUEST}"
echo "${TRAVIS_PULL_REQUEST}"
echo "${TRAVIS_PULL_REQUEST}"

python3 config/pr_crawler.py --lab 1 --current-pr "${TRAVIS_PULL_REQUEST}"

python3 config/plagiarism_check.py --source-file lab_1/main.py --others-dir tmp
