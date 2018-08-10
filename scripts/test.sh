
export TRAVIS_TAG="v1.40-trial"
export TRAVIS_PATTERN="^\"?[vV][0-9]+\.[0-9]+(-trial)?\"?$"
if [[ $TRAVIS_TAG =~ $TRAVIS_PATTERN ]];
then
    echo "1"
else
    echo "2"
fi