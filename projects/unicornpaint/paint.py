#!/usr/bin/env python

import os
import stat
import threading
import time
from sys import exit

try:
    from flask import Flask, render_template
except ImportError:
    exit("This script requires the flask module\nInstall with: sudo pip install flask")

import unicornhathd

PORT = 8000

unicornhathd.rotation(0)

width,height=unicornhathd.get_shape()

control_panel = """
    <table cellspacing="0" cellpadding="0" border-collapse="collapse">"""

for y in range(height):
    control_panel += '<tr>'
    for x in range(width):
        control_panel += '<td data-x="' + str(x) + '" data-y="' + str(y) + '" data-hex="000000" style="background-color:#000000;"></td>'
    control_panel += '</tr>'

control_panel += '</table><div class="mc"></div>'

control_panel += """
    <ul class="tools">
        <li data-tool="paint" class="paint selected"><span class="fa fa-paint-brush"></span></li>
        <li data-tool="pick" class="pick"><span class="fa fa-eyedropper"></span></li>
        <li data-tool="lighten" class="lighten"><span class="fa fa-adjust"></span> Lighten</li>
        <li data-tool="darken" class="darken"><span class="fa fa-adjust"></span> Darken</li>
    </ul>"""


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('painthathd.html')

@app.route('/save/<filename>')
def save(filename):
    try:
        os.mkdir('saves/')
    except OSError:
        pass
    try:
        data = unicornhathd.get_pixels()
        data = repr(data)
        data = data.replace('array', 'list')
        print(filename, data)
        file = open('saves/' + filename + '.py', 'w')
        file.write("""#!/usr/bin/env python
import unicornhathd
import signal

unicornhathd.rotation(0)

pixels = {}

for x in range(unicornhathd.WIDTH):
    for y in range(unicornhathd.HEIGHT):
        r, g, b = pixels[x][y]
        unicornhathd.set_pixel(x, y, r, g, b)

unicornhathd.show()

print("\\nShowing: {}\\nPress Ctrl+C to exit!")

signal.pause()
""".format(data, filename))
        file.close()
        os.chmod('saves/' + filename + '.py', 0o777 | stat.S_IEXEC)

        return("ok" + str(unicornhathd.get_pixels()))
    except AttributeError:
        print("Unable to save, please update")
        print("unicornhathdhathd library!")
        return("fail")

@app.route('/clear')
def clear():
    s = threading.Thread(None,unicornhathd.clear)
    s.start()
    return "ok"

@app.route('/show')
def show():
    s = threading.Thread(None,unicornhathd.show)
    s.start()
    return "ok"

@app.route('/pixel/<x>/<y>/<r>/<g>/<b>')
def set_pixel(x, y, r, g, b):
    x, y, r, g, b = int(x), int(y), int(r), int(g), int(b)
    unicornhathd.set_pixel(unicornhathd.WIDTH - 1 - x, y, r, g, b)
    return "ok"

if __name__ == "__main__":
    unicornhathd.brightness(0.5)
    app.run(host='0.0.0.0', port=PORT, debug=True)
