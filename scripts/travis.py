#!/usr/bin/env python2.7
import json
import requests
import base64
import os

if __name__ == '__main__':

    revision = ''
    if os.environ.get('TRAVIS_COMMIT_RANGE') and os.environ['TRAVIS_COMMIT_RANGE'] != '':
        revision = os.environ['TRAVIS_COMMIT_RANGE'].replace('...', '..')
    elif os.environ.get('TRAVIS_COMMIT') and os.environ['TRAVIS_COMMIT'] != '':
        revision = '%s..^HEAD' % (os.environ['TRAVIS_COMMIT'])

    print revision


RAVIS_COMMIT="2b8600b"
#TRAVIS_COMMIT_RANGE="c896cfd8f603...6da1a4e53295"
echo $TRAVIS_COMMIT
echo $TRAVIS_COMMIT_RANGE

rev="$TRAVIS_COMMIT..HEAD^"

if [ "$TRAVIS_COMMIT_RANGE" != "" ]
then
  rev=$TRAVIS_COMMIT_RANGE
fi

echo $rev

git diff-tree --no-commit-id --name-only -r $rev
if `git diff-tree --no-commit-id --name-only -r $rev | grep -q yarn.lock` 
then
    echo "running yarn cache clean"
fi

