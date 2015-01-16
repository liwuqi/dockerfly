#!/bin/env python
# -*- coding: utf-8 -*-

"""dockerfly toolbox

Usage:
  dockerflyrun    daemon <ip> <port>

Options:
  -h --help                 Show this screen.
  --version                 Show version.
  --dockerflyd=<ip:port>    Set dockerflyd ip and port [default: 127.0.0.1:5123]

Example:
    start dockerfld         dockerflyrun    daemon 0.0.0.0 5123
"""

from docopt import docopt

import include
from dockerfly.settings import dockerfly_version
from dockerfly.bin.dockerflyd import rundaemon
from dockerfly.ui.servers import runweb

def main():
    arguments = docopt(__doc__, version=dockerfly_version)

    if arguments['daemon']:
        print arguments['<ip>'], arguments['<port>']
        rundaemon(arguments['<ip>'], arguments['<port>'])

    if arguments['web']:
        print arguments['<ip>'], arguments['<port>'], arguments['--dockerflyd']
        runweb(arguments['<ip>'], arguments['<port>'], arguments['--dockerflyd'])

if __name__ == '__main__':
    main()
