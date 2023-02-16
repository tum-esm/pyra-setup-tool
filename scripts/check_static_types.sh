set -o errexit

echo "Removing old mypy cache"
rm -rf .mypy_cache 

echo "Checking run.py"
mypy run.py