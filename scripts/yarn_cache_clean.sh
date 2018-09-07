#!/usr/bin/env bash

TRAVIS_COMMIT="37236fb38745fee9a7fd25e687d5c2246739ad46"
TRAVIS_COMMIT_RANGE="37236fb38745fee9a7fd25e687d5c2246739ad46..dbd1a30f4c57b157c98925d508b6edc5486e1cd2"


echo $TRAVIS_COMMIT
echo $TRAVIS_COMMIT_RANGE

rev="$TRAVIS_COMMIT..HEAD^"

if [ "$TRAVIS_COMMIT_RANGE" == "" ];
then
  set rev=$TRAVIS_COMMIT_RANGE
fi

echo $rev

git diff-tree --no-commit-id --name-only -r $rev
git diff-tree --no-commit-id --name-only -r $rev | grep -q yarn.lock

