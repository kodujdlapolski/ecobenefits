#!/usr/bin/env python3

from eco import server
from eco import config


if __name__ == '__main__':
    server.app.run(host=config.HOST, port=config.PORT)
