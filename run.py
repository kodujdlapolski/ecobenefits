#!/usr/bin/env python3

from eco import config, server

if __name__ == '__main__':
    server.app.run(host=config.HOST, port=config.PORT)
