#!/bin/bash
set -o nounset  # Stricter mode

[ -f color.sh ] && . color.sh

# Constants
readonly LANGUAGE=en
readonly LANG=en_US.utf8

# Configuration variables
POLLING_INTERVAL=10
COMPRESS_LOG_FILE=false  # DONE is it supported by my version of the UI? Yes

readonly MODIFIER_KEYS="$(xmodmap -pk | grep -iE '\b(shift_[lr]|alt_[lr]|control_[lr]|caps_lock)\b' | cut -f 1 | xargs | tr ' ' '|')"

# Shared memory, instead of a temporary file: more secure, and quicker
readonly HELPER_FILE=/dev/shm/keyfreqraw


mkdir -p ../logs
last_log_file=""


# First message to inform that the script was started correctly
echo -e "${green}$0 has been started successfully.${reset}"
nb_virtual_kb=$(xinput | grep 'slave  keyboard' | grep -o 'id=[0-9]*' | cut -d= -f2 | wc -l)
nb_real_kb=$(xinput | grep 'keyboard.*slave.*keyboard' | grep -c -v 'Virtual')
echo -e "  - It will ${red}constantly${reset} record the keyboard(s) of your laptop (currently there seems to be ${black}${nb_virtual_kb}${reset} virtual keyboard(s) and ${black}${nb_real_kb}${reset} real keyboard(s))."
echo -e "  - It will work in time window of ${red}$POLLING_INTERVAL${reset} seconds."
[ $COMPRESS_LOG_FILE = true ] && echo -e "  - It will regularly compress the log files."
echo

# Start the main loop
while true; do
    # check each possible keyboard
    keyboardIds=$(xinput | grep 'slave  keyboard' | grep -o 'id=[0-9]*' | cut -d= -f2)
    # and grep only the updated ones
    filesToGrep=''
    for kbd_id in $keyboardIds; do
        fileName="${HELPER_FILE}.$kbd_id"
        { (stdbuf -o0 timeout -s 10 "$POLLING_INTERVAL" xinput test "$kbd_id" 2>/dev/null `# Grab key events for $POLLING_INTERVAL seconds` \
            | grep press 2>/dev/null `# Filter out only press events (I am getting doubled release events for some reason)` \
            | tr -dc '0-9\n' `# Keep only keycodes` \
            | grep -vE "$MODIFIER_KEYS" `# Remove modifier keys` \
            | tr -c '\n' '0' `# Replace keycodes with 0 for added security` \
            ) > "$fileName"; } &
        filesToGrep+="$fileName "
    done

    wait


    # Count number of key release events
    num=$(cat $filesToGrep | wc -l)

    # Append unix time stamp and the number into file
    log_file="../logs/keyfreq_$(python3 rewind7am.py).txt"
    # Only print and log if $num > 0
    if [ "${num:-0}" -gt 0 ]; then
        echo -e "Logged ${yellow}key frequency${reset}: \tat ${magenta}$(date)${reset}, ${green}$(printf "%5i " "${num}")${reset} key release events, written to '${black}${log_file}${reset}'"
        echo "$(date +%s) $num"  >> "$log_file"
    fi


    if [ "$last_log_file" != "$log_file" ]; then
        # Optionally compress the log file (remove extraneous 0 key counts)
        if [ $COMPRESS_LOG_FILE = true ] && [ -s "$last_log_file" ]; then
            grep -s -v " 0$" -A 1 -B 1 "$last_log_file" \
                | sort -u \
                | grep -s -v "^\-\-$" > "${last_log_file}.compressed"
            echo "${blue}Compressing keyfreq log file${reset}: ${yellow}$(ls -hsx ${last_log_file}*)${reset}"
            mv -f -- "${last_log_file}.compressed" "$last_log_file"
        fi
        # Create symlink to most recent log file everytime it changes its name,
        # so we can use something like "tail -F ../logs/keyfreq_today.txt"
        ln -s -f "$(basename "$log_file")" "../logs/keyfreq_today.txt"
        last_log_file="$log_file"
        # XXX I don't use this feature, but alright
    fi
done

