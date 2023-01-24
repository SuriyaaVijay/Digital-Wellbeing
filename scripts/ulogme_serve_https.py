
"""
ulogme_serve_https.py - simple HTTP server supporting SSL.

- Replace fpem with the location of your .pem server file ('server.pem' by default).
- The default port is 8443.

Usage: python ulogme_serve_https.py


From https://www.piware.de/2011/01/creating-an-https-server-in-python/ and https://stackoverflow.com/a/22436756/5889533
"""
from __future__ import print_function   # Python 2 compatibility
from __future__ import absolute_import  # Python 2 compatibility

import sys
import os
import os.path
import ssl
import socket
from subprocess import check_output
try:
    import http.server as http_server
except ImportError:
    import SimpleHTTPServer as http_server  # Python 2 compatibility

# Local imports
from ulogme_serve import printc, CustomHandler
from notify import notify


# Utility functions
default_fpem = "server.pem"
default_fpem_path = os.path.join("..", "render", default_fpem)


def generate_certificate(fpem=default_fpem_path):
    """ Use openssl command line (ugly) to generate a SSL certificate: 4096 bits, valid 10 years. See the code for more details."""
    print("Generating the SSL certificate to {} in the current directory ({}) ...".format(fpem, os.getcwd()))
    args = [
        "openssl",
        "req",
        "-newkey rsa:4096",
        "-x509",
        "-keyout {}".format(fpem),
        "-out {}".format(fpem),
        "-days 3650",  # Only valid 10 years!
        "-nodes"
    ]
    print("Executing '{}' ...".format(' '.join(args)))
    print(check_output(' '.join(args), shell=True))


if __name__ == "__main__":
    httpd = None  # Make sure the variable exist, or the finally: case below can mess up

    # Port setting
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
        assert PORT > 2024 or PORT == 443, "Error, you should not ask to use a PORT reserved by the system (<= 2024)"
    else:
        PORT = 443
        # PORT = 8443

    # Address setting
    if len(sys.argv) > 2:
        IP = str(sys.argv[2])
    else:
        # IP = "ulogme"  # IP address to use by default
        IP = "localhost"  # IP address to use by default

    # Certificate setting
    if len(sys.argv) > 3:
        myfpem = str(sys.argv[3])
    else:
        myfpem = default_fpem_path

    if not os.path.isfile(myfpem):
        printc("<red>The SSL certificate<reset> file <black>{}<reset> is not present, trying to generate it with a 'openssl' command ...".format(myfpem))
        generate_certificate(myfpem)
    printc("<green>Using the SSL certificate<reset> from the information in the file <black>{}<reset> ...".format(myfpem))

    # Serve render/ folder, not current folder
    os.chdir(os.path.join("..", "render"))

    try:
        httpd = http_server.HTTPServer((IP, PORT), CustomHandler)
        httpd.socket = ssl.wrap_socket(httpd.socket, certfile=myfpem, server_side=True)
        sa = httpd.socket.getsockname()
        IP, PORT = sa[0], sa[1]
        printc("<green>Serving uLogMe<reset> on a HTTPS server, see it locally on '<u><black>https://{}:{}<reset><U>' ...".format(IP, PORT))
        notify("Serving <b>uLogMe</b> on a <i>HTTPS</i> server, see it locally on 'https://{}:{}' ...".format(IP, PORT), icon="terminal")  # DEBUG
        httpd.serve_forever()
    except socket.error as e:
        if e.errno == 98:
            printc("<red>The port {} was already used ...<reset>".format(PORT))
            printc("Try again in some time (about 1 minute on Ubuntu), or launch the script again with another port: '<black>$ ulogme_serve_https.py {}<reset>' ...".format(PORT + 1))
        else:
            printc("<red>Error, ulogme_serve.py was interrupted, giving:<reset>")
            printc("<red>Exception:<reset> ", e)
    except KeyboardInterrupt:
        printc("\n<red>You probably asked to interrupt<reset> the '<black>ulogme_serve.py<reset>' HTTPS server ...")
    finally:
        try:
            if httpd is not None:
                printc("\n<yellow>Closing the HTTPS server<reset> (address '<black>{}<reset>', port '<black>{}<reset>') ...".format(IP, PORT))
                httpd.server_close()
        except Exception as e:
            printc("<red>The HTTPS server<reset> (address '<black>{}<reset>', port '<black>{}<reset>') <red>might not have been closed<reset> ...".format(IP, PORT))
            printc("<red>Exception:<reset> e =", e)
