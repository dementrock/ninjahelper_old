#!/usr/bin/env python

from ninjahelper import app
from ninjahelper.helper import rlistdir
import os

extra_files = filter(lambda x: not (x.endswith('swp') or x.endswith('swo')), rlistdir('ninjahelper'))

if __name__ == '__main__':
    if app.debug:
        os.system('compass compile ninjahelper/static')
        app.run(debug=True, use_debugger=True, extra_files=extra_files)
    else:
        app.run(host='0.0.0.0')
