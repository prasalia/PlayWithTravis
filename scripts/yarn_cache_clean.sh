#!/usr/bin/env bash




echo $TRAVIS_COMMIT
echo $TRAVIS_COMMIT_RANGE

rev="$TRAVIS_COMMIT..HEAD^"

if [ "$TRAVIS_COMMIT_RANGE" != "" ]
then
  rev=$TRAVIS_COMMIT_RANGE
fi

echo $rev
git --no-pager log -n 5
git diff-tree --no-commit-id --name-only -r $rev
if git diff-tree --no-commit-id --name-only -r $rev | grep -q yarn.lock 
then
    echo "running yarn cache clean"
fi

