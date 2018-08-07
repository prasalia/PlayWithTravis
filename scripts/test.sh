#!bin/sh
export VERSION_NUMBER="1.25"
unset VERSION_NUMBER
if [ -n "$VERSION_NUMBER" ]; then
    echo "in"
    echo $VERSION_NUMBER
    #git tag -af v$VERSION_NUMBER-$TRAVIS_BUILD_NUMBER $TRAVIS_COMMIT -m "Release Tag created by TravisCI"
    #git push --no-verify --delete origin v$VERSION_NUMBER-$TRAVIS_BUILD_NUMBER
    #git push --no-verify origin v$VERSION_NUMBER-$TRAVIS_BUILD_NUMBER
fi