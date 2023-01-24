#!/bin/bash

set -o pipefail
set -eu

# Use https://bitbucket.org/lbesson/bin/src/master/.color.sh to add colors in Bash scripts
echo "WARNING If you don't see colors correctly, remove the 'color.sh' file in 'uLogMe/scripts' to remove the colors, or modify it to suit your need (if you have a light background for instance)."  # See https://github.com/Naereen/uLogMe/issues/17
[ -f color.sh ] && . color.sh

cd "$( dirname "${BASH_SOURCE[0]}" )"

echo "Starting ./keyfreq.sh to log keys..."
./keyfreq.sh &
echo "Okay, we have started ./keyfreq.sh to log keys..."

echo "Starting ./logactivewin.sh to log keys..."
./logactivewin.sh
# echo "Okay, we have started ./logactivewin.sh to log keys..."
