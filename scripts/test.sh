#!bin/sh
export CHANGELOG=`git --no-pager log $TRAVIS_COMMIT_RANGE --pretty=format:"%h - %s\n"`
echo $CHANGELOG