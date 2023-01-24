#!/bin/bash

set -o pipefail
set -eu

# Use https://bitbucket.org/lbesson/bin/src/master/.color.sh to add colors in Bash scripts
echo "WARNING If you don't see colors correctly, remove the 'color.sh' file in 'uLogMe/scripts' to remove the colors, or modify it to suit your need (if you have a light background for instance)."  # See https://github.com/Naereen/uLogMe/issues/17
[ -f ~/bin/.color.sh ] && . ~/bin/.color.sh

echo -e "${yellow}Starting '${black}ulogme_tmux.sh'${reset} ..."

if [ -L "${BASH_SOURCE[0]}" ]; then
    # We have a symlink... how to deal with it?
    cd "$( dirname "$(readlink -f "${BASH_SOURCE[0]}")" )"
else
    cd "$( dirname "${BASH_SOURCE[0]}" )"
fi;

# XXX assume runing inside a tmux session
if [ "X${TMUX}" = "X" ]; then
    echo -e "${red}This script ${black}${0}${red} has to be run inside a tmux session.${reset}"
    exit 1
fi

port="${1:-8443}"  # Default is port=8124
IP="${2:-localhost}"
protocol="${3:-https}"

# Reference tmux man page (eg. https://linux.die.net/man/1/tmux)
# start a new window,
# name it ulogme
tmux new-window -a -n 'uLogMe' "tmux split-window -d \"./ulogme_serve.sh ${port} ${IP} ${protocol} | tee /tmp/ulogme_serve_$$.log\" ; ./ulogme_data.sh | tee /tmp/ulogme_data_$$.log"
# launch './ulogme_data.sh' in first one
# split it half
# launch './ulogme_serve.sh' in second one

sleep 12
# return to current tab at the end
tmux last-window
