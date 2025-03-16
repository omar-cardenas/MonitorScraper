from flask import Flask, render_template
import sqlite3
from dataclasses import dataclass

@dataclass
class Monitor:
    name: str
    resolution: str
    panel_type: str
    brand: str
    price: str
    url: str
    image_src: str


app = Flask(__name__)

@app.route('/')
def index():
    monitors = fetchMonitors()
    print(monitors)

    return render_template('index.html', monitors = monitors)
@app.route('/display/<type>/<resolution>')
def display(type, resolution):
    print(type, resolution)
    monitors = fetchMonitors(type, resolution)
    print(monitors)

    return render_template('index.html', monitors = monitors)

def get_monitors_result(sql: str) -> list[Monitor]:
    db = sqlite3.connect("monitors.db")
    query_result = db.execute(sql)
    monitors = []
    for row in query_result:
        # skip product id
        name = row[1].split(";")[0]
        monitor = Monitor(name, row[2], row[3], row[4], row[5], row[6], row[7])
        monitors.append(monitor)

    db.close()
    return monitors

def fetchMonitors(type=None, resolution = None) -> list[Monitor]:
    monitors = None
    if type and resolution:
        print("running fetch with parameters")
        sql = f"SELECT * from monitors WHERE RESOLUTION = '{resolution}' AND PANEL_TYPE = '{type}' ORDER BY PRICE;"
        monitors = get_monitors_result(sql)
    else:
        sql = 'SELECT * from monitors ORDER BY PRICE;'
        monitors = get_monitors_result(sql)
    if len(monitors) >= 8:
        monitors = monitors[0:8]

    return monitors




if __name__ == '__main__':
    app.run(debug=True)