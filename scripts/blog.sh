#!/bin/bash
# blog.sh for https://github.com/Naereen/uLogMe/
# MIT Licensed, https://lbesson.mit-license.org/
#
# allows the user to simply record a blog, saves it together with unix time in ../logs/blog_...
# Use https://bitbucket.org/lbesson/bin/src/master/.color.sh to add colors in Bash scripts
[ -f color.sh ] && . color.sh

cd "$( dirname "${BASH_SOURCE[0]}" )"

# mkdir -p ../logs/

# # read -r -p "Enter blog: " n

# if [ -z "$1" ]; then
#     T="$(date +%s)" # default to current time
# else
#     T="$1"  # argument was provided, use it!
# fi

# logfile="../logs/blog_$(python3 ./rewind7am.py "$T").txt"
# echo "$T $n" >> "$logfile"
# echo -e "Logged ${yellow}blog${reset}: ${magenta}$T${reset} ${green}$n${reset} into '${black}$logfile${reset}'"

logfile="$1"
CP "$logfile" /tmp/
# time="$2"
time="$(date "+%A %d %B %Y")"

# TODO: grep for lines 'TODO' and append them in ~/TODO.md with ## date, if ## date not present and if line not present
todos="${HOME:-~}/TODO.md"
header_line="## TODO: $time #uLogMe"
if ( grep -- "$header_line" "$todos" &>/dev/null); then
    echo -e "'${black}${header_line}${reset}' ${white}already in ${u}${todos}${reset}${white}"
else
    echo -e "${green}Adding '${white}${header_line}${reset}' to ${u}${todos}${reset}${white}"
    echo -e "\n${header_line}" >> "${todos}"
fi

while IFS= read -r line; do
    # echo -e "${red}Found line: $line${white}"  # DEBUG
    todo_line="$(echo "${line}" | grep 'TODO')"
    if [ "X${todo_line}" != "X" ]; then
        echo -e "${blue}Found TODO line:${white} ${line}${white}"  # DEBUG
        if ( grep -- "${todo_line}" "${todos}" &>/dev/null ); then
            echo -e "${red}Not a new todo_line...${white}"  # DEBUG
        else
            echo -e "${green}Found new todo_line:${white} ${todo_line}${white}"  # DEBUG
            # first, remove 2 leading spaces
            # then, transform "- TODO" into "- [ ] TODO" so I can mark them as done in VSCode, using Alt+D
            echo "$todo_line" | sed 's/^  //' | sed 's/- TODO/- [ ] TODO/' >> "$todos"
        fi
    fi
done < "$logfile"
