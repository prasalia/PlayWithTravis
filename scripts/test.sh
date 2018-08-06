#!bin/sh
export TRAVIS_BRANCH="release/v1.35"
export RC_BRANCH_PATTERN="^\"?release\/[vV][0-9]+\.[0-9]+\"?$"
if [ $TRAVIS_BRANCH == "develop" ] || [ $TRAVIS_BRANCH == "master" ] || [[ $TRAVIS_BRANCH =~ $RC_BRANCH_PATTERN ]];
then
    echo "1"
else
    echo "2"
fi