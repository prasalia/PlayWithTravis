#!bin/sh
export CHANGELOG=`git --no-pager log $TRAVIS_COMMIT_RANGE --no-merges --pretty=format:"%h - %s%n"`
bundle exec fastlane mytest changeText:"$CHANGELOG"