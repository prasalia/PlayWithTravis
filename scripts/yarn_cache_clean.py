#!/usr/bin/env python2.7
""" Script to clean the yarn cache
"""

from os import environ
from subprocess import check_output, CalledProcessError

if __name__ == '__main__':

    revision = ''
    fileschanged = ''
    
    if environ.get('TRAVIS_COMMIT_RANGE') and environ['TRAVIS_COMMIT_RANGE'] != '':
        revision = environ['TRAVIS_COMMIT_RANGE'].replace('...', '..')
    elif environ.get('TRAVIS_COMMIT') and environ['TRAVIS_COMMIT'] != '':
        revision = '%s..^HEAD' % (environ['TRAVIS_COMMIT_RANGE'])

    cmd = 'git diff-tree --no-commit-id --name-only -r %s' % (revision)
    try:
        print 'Getting a list of files changed in revision range: %s' % (revision)
        fileschanged = (check_output(cmd, shell = True)).split()
    except CalledProcessError:
        print 'Error: Unable to retrieve the list of changed files'    

    #if 'yarn.lock' in fileschanged(revision):
    if 'yarn.lock' in fileschanged:
        print 'Detected a change in yarn.lock. Cleaning existing yarn cache'
        try:
            check_output('yarn cache clean', shell = True)
        except CalledProcessError as ex:
            print 'Error: Unable to clear Yarn cache'
            print ex.output
    else:
        print "No yarn.lock file changed detected"


    