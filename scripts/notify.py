#!/usr/bin/env python3

"""
Defines one useful function notify() to (try to) send a desktop notification.
"""

from __future__ import print_function   # Python 2 compatibility
from __future__ import absolute_import  # Python 2 compatibility

from webbrowser import open as openTab
from os import getcwd
from os.path import exists, join
from glob import glob
from random import choice
from subprocess import Popen


# WARNING Unused callback function for the notifications
def open_the_ulogme_page(notification, label, args=("localhost", 8124)):
    """ Open the http://{}:{}/ URL in a new tab of your favorite browser. """
    print("notify.notify(): open_the_ulogme_page callback function ...")
    print("open_the_ulogme_page(): notification = {}, label = {}, args = {} ...".format(notification, label, args))
    IP, PORT = args
    ulogme_url = "http://{}:{}/".format(IP, PORT)
    print("notify.notify(): Calling 'open(ulogme_url, new=2, autoraise=True)' ...")
    return openTab(ulogme_url, new=2, autoraise=True)


# Constants for the program
PROGRAM_NAME = "uLogMe server (ulogme_serve.py)"
ICON_PATH = join("..", "scripts", "icons", "pikachu.png")
ICON_PATHS = glob(join("..", "scripts", "icons", "*.png"))


def choose_icon(random=True):
    """ Choose a random icon. """
    if random:
        iconpath = choice(ICON_PATHS)
    else:
        iconpath = ICON_PATH
    # print("iconpath =", iconpath)  # DEBUG
    return iconpath


# Define the icon loaded function
try:
    from gi import require_version
    require_version('GdkPixbuf', '2.0')
    from gi.repository import GdkPixbuf

    def load_icon(random=True):
        """ Load and open a random icon. """
        iconpath = choose_icon(random=random)
        # Loading the icon...
        if exists(iconpath):
            # Use GdkPixbuf to create the proper image type
            iconpng = GdkPixbuf.Pixbuf.new_from_file(iconpath)
        else:
            iconpng = None
        # print("iconpng =", iconpng)  # DEBUG
        return iconpng

except ImportError:
    print("\nError, gi.repository.GdkPixbuf seems to not be available, so notification icons will not be available ...")
    print("On Ubuntu, if you want notification icons to work, install the 'python-gobject' and 'libnotify-bin' packages.")
    print("(For more details, cf. 'http://www.devdungeon.com/content/desktop-notifications-python-libnotify')")

    def load_icon(random=True):
        print("Fake icon, random = {}.".format(random))  # DEBUG
        return None


# Trying to import gi.repository.Notify
has_Notify = False
try:
    from gi import require_version
    require_version('Notify', '0.7')
    from gi.repository import Notify
    # One time initialization of libnotify
    Notify.init(PROGRAM_NAME)
    has_Notify = True
except ImportError:
    print("\nError, gi.repository.Notify seems to not be available, so notification will not be available ...")
    print("On Ubuntu, if you want notifications to work, install the 'python-gobject' and 'libnotify-bin' packages.")
    print("(For more details, cf. 'http://www.devdungeon.com/content/desktop-notifications-python-libnotify')")


# Define the first notify function, with gi.repository.Notify
def notify_gi(body, summary=PROGRAM_NAME,
        icon="random", addCallback=False,
        IP="localhost", PORT=8124,  # FIXED use this in ulogme_serve.py
        timeout=5  # In seconds
    ):
    """
    Send a notification, with gi.repository.Notify.

    - icon can be "dialog-information", "dialog-warn", "dialog-error". By default it is set to the 'pikachu.png' image
    """
    try:
        # Trying to fix a bug:
        # g-dbus-error-quark: GDBus.Error:org.freedesktop.DBus.Error.ServiceUnknown: The name :1.5124 was not provided by any .service files (2)
        Notify.init(PROGRAM_NAME)

        if icon and icon != "random":
            notification = Notify.Notification.new(
                summary,  # Title of the notification
                body,     # Optional content of the notification
                icon      # WARNING Should not indicate it here
            )
        else:
            notification = Notify.Notification.new(
                summary,  # Title of the notification
                body      # Optional content of the notification
            )

            if icon == "random":
                # Add a Pikachu icom to the notification
                # Why Pikachu? ALWAYS PIKACHU! http://www.lsv.ens-cachan.fr/~picaro/
                iconpng = load_icon(random=True)
                if iconpng is not None:
                    # Use the GdkPixbuf image
                    notification.set_icon_from_pixbuf(iconpng)
                    notification.set_image_from_pixbuf(iconpng)

        # Lowest urgency (LOW, NORMAL or CRITICAL)
        notification.set_urgency(Notify.Urgency.LOW)

        # add duration, lower than 10 seconds (5 second is enough).
        notification.set_timeout(timeout * 1000)

        # DONE add a callback that open the browser tab/page on uLogMe when clicked on it
        # The notification will have a button that says "View uLogMe page".
        if addCallback:
            notification.add_action(
                "action_click",
                "View uLogMe page",
                open_the_ulogme_page,
                (IP, PORT)  # Arguments given to open_the_ulogme_page
            )

        # Actually show the notification on screen
        notification.show()
        return 0

    # Ugly! XXX Catches too general exception
    except Exception as e:
        print("\nnotify.notify(): Error, notify.notify() failed, with this exception")
        print(e)
        return -1


# Define the second notify function, with a subprocess call to 'notify-send'
def notify_cli(body, summary=PROGRAM_NAME,
        icon="random", addCallback=False,
        IP="localhost", PORT=8124,  # XXX unused here, notify-send does not accept callback functions
        timeout=5  # In seconds
    ):
    """
    Send a notification, with a subprocess call to 'notify-send'.
    """
    if addCallback:
        print("Warning: addCallback = True but notify-send does not accept callback functions (for IP = {}, PORT = {}).".format(IP, PORT))  # DEBUG
    try:
        print("notify.notify(): Trying to use the command line program 'notify-send' ...")
        if icon == "random":
            icon = join(getcwd(), choose_icon(random=True))
        if icon:
            Popen(["notify-send", "--expire-time=%s" % (timeout * 1000), "--icon=%s" % (icon), summary, body])
            print("notify.notify(): A notification have been sent, with summary = '%s', body = '%s', expire-time='%s' and icon='%s'." % (summary, body, timeout * 1000, icon))
        else:
            Popen(["notify-send", "--expire-time=%s" % (timeout * 1000), summary, body])
            print("notify.notify(): A notification have been sent, with summary = '%s', body = '%s' and expire-time='%s'." % (summary, body, timeout * 1000))
        return 0
    # Ugly! XXX Catches too general exception
    except Exception as e:
        print("\nnotify.notify(): notify-send : not-found ! Returned exception is %s." % e)
        return -1


# Define the unified notify.notify() function
def notify(body, summary=PROGRAM_NAME,
        icon="random", addCallback=False,
        IP="localhost", PORT=8124,  # FIXED use this in ulogme_serve.py
        timeout=5  # In seconds
    ):
    # print("Notification: '{}', from '{}' with icon '{}'.".format(body, summary, icon))  # DEBUG
    if not has_Notify:
        print("notify.notify(): Warning, desktop notification from Python seems to not be available ...")
        return notify_cli(body, summary=summary, icon=icon, IP=IP, PORT=PORT, timeout=timeout, addCallback=addCallback)
    try:
        return_code = notify_gi(body, summary=summary, icon=icon, IP=IP, PORT=PORT, timeout=timeout, addCallback=addCallback)
        if return_code < 0:
            return_code = notify_cli(body, summary=summary, icon=icon, IP=IP, PORT=PORT, timeout=timeout, addCallback=addCallback)
    except Exception:
        return_code = notify_cli(body, summary=summary, icon=icon, IP=IP, PORT=PORT, timeout=timeout, addCallback=addCallback)
    return return_code


if __name__ == "__main__":
    # notify_gi("Test body Test body Test body ! From 'notify_gi(...)', with icon=terminal ...", icon="terminal")
    # notify_gi("Test body Test body Test body ! From 'notify_gi(...)', with random Pokémon icon ...")
    # notify_cli("Test body Test body Test body ! From 'notify_cli(...)', with icon=terminal ...", icon="terminal")
    # notify_cli("Test body Test body Test body ! From 'notify_cli(...)', with random Pokémon icon ...")
    notify("Test body Test body Test body ! From 'notify(...)', with icon=terminal ...", icon="terminal")
    notify("Test body Test body Test body ! From 'notify(...)', with no icon ...", icon=None)
    notify("Test body Test body Test body ! From 'notify(...)', with random Pokémon icon ...")
