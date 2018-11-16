#!/bin/bash

LASTCOMMIT=`git --no-pager log -n 1 --no-merges --pretty=format:"%s"`;
if [ -z $MOCK_ENV ] && [ -z $PROD_BUILD ];
then   
  if echo $LASTCOMMIT | grep -i "\[env:mock\]";
  then
    echo "[env:mock] found in the last commit message. Setting MOCK_ENV to true";
    export MOCK_ENV="true";
    export PROD_BUILD="false";
  elif echo $LASTCOMMIT | grep -i "\[env:prod\]";
  then
    echo "[env:prod] found in the last commit message. Setting PROD_BUILD to true";
    export MOCK_ENV="false";
    export PROD_BUILD="true";
  fi;
fi;
if [ -z $SSL_UNPIN ];
then   
  if echo $LASTCOMMIT | grep -i "\[type:pinned\]";
  then
    echo "[type:pinned] found in the last commit message. Setting SSL_UNPIN to false";
    export SSL_UNPIN="false";
  elif echo $LASTCOMMIT | grep -i "\[type:unpinned\]";
  then
    echo "[type:unpinned] found in the last commit message. Setting SSL_UNPIN to true";
    export SSL_UNPIN="true";
  fi;
fi;


  