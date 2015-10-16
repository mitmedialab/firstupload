#!/usr/bin/env python

from app import app
import os

#app.config.from_pyfile('config.py')
if os.environ.get("DEBUG"):
    app.run(debug = True)
else:
	app.run()
