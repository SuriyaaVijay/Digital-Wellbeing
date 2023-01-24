#!/usr/bin/env python3
from __future__ import print_function   # Python 2 compatibility
from __future__ import absolute_import  # Python 2 compatibility

import sys
import os
import subprocess
import cgi
import socket
try:
    import socketserver
except ImportError:                      
    import SocketServer as socketserver  
try:
    import http.server as http_server
except ImportError:
    import SimpleHTTPServer as http_server  # Python 2 compatibility

# Import a printc function to use ANSI colors in the stdout output
try:
    try:
        from ansicolortags import printc
    except ImportError:
        print("Optional dependancy (ansicolortags) is not available, using regular print function.")
        print("  You can install it with : 'pip install ansicolortags' (or sudo pip)...")
        from ANSIColors import printc
except ImportError:
    print("Optional dependancy (ANSIColors) is not available, using regular print function.")
    print("  You can install it with : 'pip install ANSIColors-balises' (or sudo pip)...")

    def printc(*a, **kw):
        """ Fake function printc.

        ansicolortags or ANSIColors are not installed...
        Install ansicolortags from pypi (with 'pip install ansicolortags')
        """
        print(*a, **kw)


# Local imports
from export_events import updateEvents
from rewind7am import rewindTime, ppDay, ppTime
from notify import notify


# Convenience functions

def writenote(note, time_=None):
    """ From https://github.com/karpathy/ulogme/issues/48"""
    cmd = ["../scripts/note.sh"]
    if time_ is not None:
        cmd.append(str(time_))
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    if not isinstance(note, bytes):
        note = note.encode('utf-8')
        # FIXED TypeError: 'str' does not support the buffer interface
    process.communicate(input=note)
    process.wait()
    notify("<b>uLogMe</b> created a note, with content '<i>{}</i>' and time '<i>{!s}</i>'.".format(note, time_))
    printc("<green>uLogMe created a note<reset>, with content '<black>{}<reset>' and time '<magenta>{!s}<reset>'.".format(note, time_))

def writeblog(name_f, time_=None):
    """ From https://github.com/karpathy/ulogme/issues/48"""
    cmd = ["../scripts/blog.sh", name_f]
    if time_ is not None:
        cmd.append(str(time_))
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    process.wait()
    notify("<b>uLogMe</b> created a blog, on file {}, and time '<i>{!s}</i>'.".format(name_f, time_))
    printc("<green>uLogMe created a blog<reset>, on file {} and time '<magenta>{!s}<reset>'.".format(name_f, time_))


# Custom handler
class CustomHandler(http_server.SimpleHTTPRequestHandler):
    """ Custom handler for the http_server:

    - handles the GET by default,
    - handles some POST request as an API: /refresh, /addnote, /blog.
    """
    def __init__(self, *args):
        self.rootdir = os.getcwd()
        super(CustomHandler, self).__init__(*args)

    def do_GET(self):
        """Default behavior for the GET."""
        http_server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        """Custom behavior for the POST."""
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": self.headers["Content-Type"]
            }
        )
        result = "NOT_UNDERSTOOD"

        if self.path == "/refresh":
            # Recompute jsons.
            # We have to pop out to root from render directory temporarily. It's a little ugly
            refresh_time = int(form.getvalue("time"))
            if refresh_time > 0:
                printc("<green>Refreshing the view of uLogMe<reset>, for the day '<magenta>{}<reset>' ...".format(ppDay(refresh_time)))
                # notify("Refreshing the view of <b>uLogMe</b>, for the day '<i>{}</i>' ...".format(ppDay(refresh_time)))
            else:
                printc("<green>Refreshing the view of uLogMe<reset>, for the overview page ...")
                # notify("Refreshing the view of <b>uLogMe</b>, for the overview page ...")
            # FIXME add a command line option to enable/disable the refresh notifications
            os.chdir(self.rootdir)  # pop out
            updateEvents()  # defined in export_events.py
            os.chdir(os.path.join("..", "render"))  # pop back to render directory
            result = "OK"

        if self.path == "/addnote":
            # add note at specified time and refresh
            note = form.getvalue("note")
            note_time = form.getvalue("time")
            printc("<green>Adding a note in uLogMe<reset>, with content '<blue>{}<reset>' and time '<magenta>{!s}<reset>' ...".format(note, ppTime(int(note_time))))
            notify("Adding a note in <b>uLogMe</b>, with content '<i>{}</i>' and time '<i>{!s}</i>' ...".format(note, ppTime(int(note_time))), icon="note")
            os.chdir(self.rootdir)  # pop out
            writenote(note, note_time)
            updateEvents()  # defined in export_events.py
            os.chdir(os.path.join("..", "render"))  # go back to render
            result = "OK"

        if self.path == "/blog":
            # add note at specified time and refresh
            post = form.getvalue("post")
            if post is None:
                post = ""
            post_time = int(form.getvalue("time"))
            printc("<green>Adding a blog post in uLogMe<reset>, with content '<blue>{}<reset>' and time '<magenta>{!s}<reset>' ...".format(post, ppDay(int(post_time))))
            notify("Adding a blog post in <b>uLogMe</b>, with content '<i>{}</i>' and time '<i>{!s}</i>' ...".format(post, ppDay(int(post_time))), icon="note")  # DEBUG
            os.chdir(self.rootdir)  # pop out
            # trev = rewindTime(post_time)
            # print("trev =", trev)  # DEBUG
            # FIXED no need for these python lines, if the blog.sh script writes the note itself
            name_f = os.path.join("..", "logs", "blog_%d.txt" % (post_time, ))
            with open(name_f, "w") as f:
                f.write(post)
            # TODO: grep for lines 'TODO' and append them in ~/TODO.md with ## date, if ## date not present and if line not present
            writeblog(name_f, time_=post_time)
            updateEvents()  # defined in export_events.py
            os.chdir(os.path.join("..", "render"))  # go back to render
            result = "OK"

        # This part has to be done manually
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        try:  # We have a bytes, as in Python2
            self.wfile.write(result)
        except TypeError:  # We have a string, as in Python3
            self.wfile.write(bytes(result, "utf8"))


if __name__ == "__main__":
    httpd = None  # Make sure the variable exist, or the finally: case below can mess up

    # Port settings
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
        assert PORT > 2024, "Error, you should not ask to use a PORT reserved by the system (<= 2024)"
    else:
        PORT = 8124

    # Address settings
    if len(sys.argv) > 2:
        IP = str(sys.argv[2])
    else:
        IP = "localhost"  # IP address to use by default

    # Serve render/ folder, not current folder
    os.chdir(os.path.join("..", "render"))

    try:
        httpd = socketserver.ThreadingTCPServer((IP, PORT), CustomHandler)
        printc("<green>Serving uLogMe<reset> on a HTTP server, see it locally on '<u><black>http://{}:{}<reset><U>' ...".format(IP, PORT))
        notify("Serving <b>uLogMe</b> on a <i>HTTP</i> server, see it locally on 'http://{}:{}' ...".format(IP, PORT), icon="terminal")  # DEBUG
        httpd.serve_forever()
    except socket.error as e:
        if e.errno == 98:
            printc("<red>The port {} was already used ...<reset>".format(PORT))
            printc("Try again in some time (about 1 minute on Ubuntu), or launch the script again with another port: '<black>$ ulogme_serve.py {}<reset>' ...".format(PORT + 1))
        else:
            printc("<red>Error, ulogme_serve.py was interrupted, giving:<reset>")
            printc("<red>Exception:<reset> ", e)
            # print("Exception: dir(e) =", dir(e))  # DEBUG
    except KeyboardInterrupt:
        printc("\n<red>You probably asked to interrupt<reset> the '<black>ulogme_serve.py<reset>' HTTP server ...")
    finally:
        try:
            if httpd is not None:
                printc("\n<yellow>Closing the HTTP server<reset> (address '<black>{}<reset>', port '<black>{}<reset>') ...".format(IP, PORT))
                httpd.server_close()
        except Exception as e:
            printc("<red>The HTTP server<reset> (address '<black>{}<reset>', port '<black>{}<reset>') <red>might not have been closed<reset> ...".format(IP, PORT))
            printc("<red>Exception:<reset> e =", e)
