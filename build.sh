#!/usr/bin/env bash

remove_artifacts() {
  rm -rf ./dist
  rm -rf ./build
  rm -rf ./*.egg-info
}

if [[ $1 == "test" ]]; then
  repository=testpypi
else
  repository=pypi
fi

echo env: ${repository}

remove_artifacts

# config file $HOME/.pypirc
pipenv run python setup.py bdist_wheel
pipenv run twine upload --repository ${repository} dist/*

remove_artifacts

read -p "Press enter to continue"
