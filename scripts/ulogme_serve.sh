#!/bin/bash

# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -o pipefail
set -eu

# Use https://bitbucket.org/lbesson/bin/src/master/.color.sh to add colors in Bash scripts
echo "WARNING If you don't see colors correctly, remove the 'color.sh' file in 'uLogMe/scripts' to remove the colors, or modify it to suit your need (if you have a light background for instance)."  # See https://github.com/Naereen/uLogMe/issues/17
[ -f color.sh ] && . color.sh

echo -e "${yellow}Starting '${black}ulogme_serve.sh${reset}' ..."

cd "$( dirname "${BASH_SOURCE[0]}" )"

# Options
port="${1:-8443}"  # Default is port=8124
IP="${2:-localhost}"
protocol="${3:-https}"

url="${protocol}://${IP}:${port}/"

# WARNING this is very specific to firefox!
if pidof firefox >/dev/null; then
	echo -e "${yellow}Opening${reset} '${black}${url}${reset}' in your favorite browser ..."
	firefox -new-tab "${url}" &
	# xdg-open "${url}" &  # Generic on Linux
	# open "${url}" &      # Generic on Mac
	# XXX this should be a better and cross-platform way to do it
	# python -m webbrowser -t "${url}"
else
	echo -e "${red}Firefox is not running${reset}, by default the uLogMe page will not be opened ...${reset}"
	echo -e "('${black}${url}${reset}' is only opened in a new tab if your Firefox is already running)."
fi

# Then run the HTTPS or HTTP server
if [ X"$protocol" = X"https" ]; then
    echo -e "${green}Calling${reset} '${black}python3 ulogme_serve_https.py ${port} ${IP}${reset}' ..."
    python3 ./ulogme_serve_https.py "${port}" "${IP}"
else
    echo -e "${green}Calling${reset} '${black}python3 ulogme_serve.py ${port} ${IP}${reset}' ..."
    python3 ./ulogme_serve.py "${port}" "${IP}"
fi
