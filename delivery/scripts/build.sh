#!/bin/bash

PYTHON=$(command -v python3.9)
VENV_FOLDER=$HOME/kilt_venv
ACTIVATE_SCRIPT="$VENV_FOLDER"/bin/activate
SCRIPT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_FOLDER="$SCRIPT_FOLDER/../.."
DOCKER_USER="docker"
USER=$(whoami)

echo "***************************************"
echo "* Deleting old virtualenv, if present *"
echo "***************************************"

if [ -n "$VIRTUAL_ENV" ]; then
  if typeset -F | grep -q deactivate; then
    echo "Deactivating virtualenv"
    deactivate
  else
    echo "Error: cannot deactivate virtualenv; invoke this script with \"source $0\""
    exit 1
  fi
fi
if [ -n "$(ls -A "${VENV_FOLDER:?}")" ]; then
   echo "Deleting virtualenv"
   rm -R "${VENV_FOLDER:?}"
fi

echo "************************************"
echo "* Creating new virtual environment *"
echo "************************************"

$PYTHON -m venv "$VENV_FOLDER"

# Activate virtual environment
# shellcheck source="ACTIVATE_SCRIPT"
source "$ACTIVATE_SCRIPT"

echo "**********************************"
echo "* Installing global dependencies *"
echo "**********************************"
pip install --upgrade pip==22.3.1
pip install --upgrade setuptools==65.5.1
pip install --upgrade wheel==0.38.3
pip install -r $ROOT_FOLDER/requirements.txt
if [ "$USER" != "$DOCKER_USER" ]; then
  pip install -r $ROOT_FOLDER/requirements-dev.txt
fi

echo "*****************************"
echo "* Installing Python package *"
echo "*****************************"

cd "$ROOT_FOLDER"
pip install .
exit_code=$?
if [ $exit_code != 0 ]; then
	exit $exit_code
fi

echo "*****************************"
echo "* Installed Python packages *"
echo "*****************************"

pip freeze --all

echo "*****************"
echo "* Running tests *"
echo "*****************"

python setup.py test
