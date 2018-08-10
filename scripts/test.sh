#!/usr/bin/env bash
BBB="release/v1.35"
echo $BBB
if [[ $BBB =~ ^release.*$ ]]; then echo "match"; fi
#then
#    echo "match";
#else
#    echo "no match";
#fi