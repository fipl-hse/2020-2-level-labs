export PYTHONPATH="$(pwd)/lab_1:$(pwd)/lab_2:$(pwd)/lab_3:$(pwd)/lab_4:$(pwd):${PYTHONPATH}"
echo "Running plagiarism check..."

python3 config/pr_crawler.py --lab 1

python3 config/plagiarism_check.py --source-file lab_1/main.py --others-dir tmp
