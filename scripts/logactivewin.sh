#!/bin/bash

[ -f color.sh ] && . color.sh

readonly LANGUAGE=en
readonly LANG=en_US.utf8

waittime="2"   

type xprintidle 2>/dev/null >/dev/null || echo -e "${red}WARNING: 'xprintidle' not installed${reset}, idle time detection will not be available (screen saver / lock screen detection only) ...\nPlease install 'xprintidle' with the following command:\nsudo apt install xprintidle"

function get_idle_time() {
    type xprintidle 2>/dev/null >/dev/null && echo $(( $(timeout -s 9 1 xprintidle) / 1000 )) || echo 0
}


mkdir -p ../logs
last_write="0"
lasttitle=""


# First message to inform that the script was started correctly
echo -e "${green}$0 has been started successfully.${reset}"
echo -e "  - It will ${red}constantly${reset} record the title of the active window of your graphical environment."
echo -e "  - It will work in time window of ${red}$waittime${reset} seconds."
echo


# Start the main loop
while true
do
	islocked=false
	# Try to figure out which Desktop Manager is running and set the
	# screensaver commands accordingly.
	if [[ X"$GDMSESSION" == X'xfce' ]]; then
		# Assume XFCE folks use xscreensaver (the default).
		type xscreensaver-command 2>/dev/null >/dev/null
		if [ "X$?" = "X0" ]; then
			islocked=true
			screensaverstate="$(xscreensaver-command -time | cut -f2 -d: | cut -f2-3 -d' ')"
			if [[ "$screensaverstate" =~ "screen non-blanked" ]]; then
				islocked=false
			fi
		fi
	elif [[ X"$GDMSESSION" == X'ubuntu' || X"$GDMSESSION" == X'ubuntu-2d' || X"$GDMSESSION" == X'gnome-shell' || X"$GDMSESSION" == X'gnome-classic' || X"$GDMSESSION" == X'gnome-fallback' ]]; then
		# Assume the GNOME/Ubuntu folks are using gnome-screensaver.
		type gnome-screensaver-command 2>/dev/null >/dev/null
		if [ "X$?" = "X0" ]; then
			screensaverstate="$(gnome-screensaver-command -q 2>/dev/null | grep -o "[^ ]*active")"
			if [[ "$screensaverstate" = active ]]; then
				islocked=true
			fi
		fi
	elif [[ X"$GDMSESSION" == X'cinnamon' ]]; then
		type cinnamon-screensaver-command 2>/dev/null >/dev/null
		if [ "X$?" = "X0" ]; then
			screensaverstate="$(cinnamon-screensaver-command -q 2>/dev/null | grep -o "[^ ]*active")"
			if [[ "$screensaverstate" = active ]]; then
				islocked=true
			fi
		fi
	elif [[ X"$XDG_SESSION_DESKTOP" == X'KDE' ]]; then
		type qdbus 2>/dev/null >/dev/null
		if [ "X$?" = "X0" ]; then
			islocked="$(qdbus org.kde.screensaver /ScreenSaver org.freedesktop.ScreenSaver.GetActive)"
		fi
	else
		# If we can't find the screensaver, assume it's missing.
		islocked=false
	fi

	if [ "$islocked" = true ]; then
		curtitle="__LOCKEDSCREEN"  # Special tag
	else
		id="$(xdotool getactivewindow)"
		curtitle="$(xdotool getwindowname "${id}")"
	fi

    was_awaken=false

    # First technic
    suspended_at="$(grep "Freezing user space processes ... *$" /var/log/TOTOkern.log 2>/dev/null | tail -n 1 | awk ' { print $1 " " $2 " " $3 } ' || echo "")"
    if [ -z "$suspended_at" ]; then
        # Second technic
        suspended_at="$(grep -E ': (performing suspend|Awake)' /var/log/TOTOpm-suspend.log 2>/dev/null | tail -n 2 | tr '\n' '|' | sed -rn 's/^(.*): performing suspend.*\|.*: Awake.*/\1/p' || echo "")"
    fi
    if [ -n "$suspended_at" ]; then
        # echo -e "${red}suspended_at = ${suspended_at}${reset} ..."  # DEBUG
        if date -d "$suspended_at" +%s 2>/dev/null >/dev/null ; then
            suspended_at="$(date -d "$suspended_at" +%s)"
            # XXX add 30 seconds, just to be sure that the laptop was indeed asleep at that time
            suspended_at=$((suspended_at + 30))
            if [ "$suspended_at" -ge "$last_write" ]; then
                echo -e "${red}Suspend occured after last event${reset}, '${black}was_awaken${reset}' = true ...${reset}"
                was_awaken=true
            fi
        else
            suspended_at="0"
            was_awaken=false
        fi
    fi

	perform_write=false
	# if window title changed, perform write
	if [[ X"$lasttitle" != X"$curtitle" || $was_awaken = true ]]; then
		perform_write=true
	fi

	T="$(date +%s)"
	if echo "$curtitle" | grep "\(privée\|InPrivate\|Private\|Incognito\)" 2>/dev/null >/dev/null
	then
		echo -e "${red}Not logged private window title ...${reset}"
		curtitle=""
	fi;

	# log window switch if appropriate
	if [ "$perform_write" = true ] && [ -n "$curtitle"  ]; then
        # Get rewind time, day starts at 7am and ends at 6:59am next day
        rewind7am=$(python3 ./rewind7am.py)
        # One logfile daily
        log_file="../logs/window_${rewind7am}.txt"
        # If computer was just awaken, log suspend event unless it happened before 7am
        if [ $was_awaken = true ] && [ "${suspended_at:-0}" -ge "$rewind7am" ]; then
            echo "$suspended_at __SUSPEND" >> "$log_file"
		fi
		echo "$T $curtitle" >> "$log_file"
		echo -e "Logged ${yellow}window title${reset}: \tat ${magenta}$(date)${reset}, \ttitle '${green}$curtitle${reset}', written to '${black}$log_file${reset}'"
		last_write="$T"
	fi

	lasttitle="$curtitle"  # swap
	sleep "$waittime"  # sleep
done
