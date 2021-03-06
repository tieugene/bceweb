#!/usr/bin/env python3
import os
import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bceweb import create_app
application = create_app()

if __name__ == '__main__':
    create_app().run()
