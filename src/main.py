#import sys
#sys.path.append('/usr/lib/python2.7/site-packages')

import socket
from app import app

if __name__ == "__main__":
    try:
        app.run(socket.gethostbyname(socket.gethostname()))

    except Exception as e:
        print(e)