from flask import Flask
app = Flask(__name__)
from flask import render_template

@app.route('/')
def hello():
    gps_coords = []
    with open('../run/detected_gps_coords.txt', 'r') as open_file:
        for line in open_file.readlines():
            line = line.strip('\n')
            line = line.strip()
            coords = line.split(',')
            lat_coord = float(coords[0])
            lng_coord = float(coords[1])
            gps_coords.append([lat_coord, lng_coord])

    return render_template('hello.html', coords=gps_coords)
