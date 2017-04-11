set -o errexit
set -o pipefail

echo "Running unit tests..."
virtualenv bottlenecks_venv
source bottlenecks_venv/bin/activate

# install python packages
easy_install -U setuptools
easy_install -U pip
pip install -r requirements/verify.txt

# unit tests
/bin/bash ./verify.sh

deactivate
