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
    oled_monitors = get_oled()
    lcd_monitors = get_LCD()

    print(oled_monitors)
    print(lcd_monitors)

    return render_template('index.html', oled_monitors = oled_monitors, lcd_monitors = lcd_monitors)


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


def get_oled() -> list[Monitor]:

    qhd_monitors = get_monitors_result("SELECT * FROM monitors WHERE RESOLUTION = '1440' AND PANEL_TYPE = 'OLED' ORDER BY PRICE;")
    uhd_monitors = get_monitors_result("SELECT * FROM monitors WHERE RESOLUTION = '2160' AND PANEL_TYPE = 'OLED' ORDER BY PRICE;")
    oled_monitors = [qhd_monitors[0], qhd_monitors[1], uhd_monitors[0], uhd_monitors[1]]
    return oled_monitors

def get_LCD() -> list[Monitor]:

    fhd_monitors = get_monitors_result("SELECT * FROM monitors WHERE RESOLUTION = '1080' AND PANEL_TYPE = 'LCD' ORDER BY PRICE;")
    qhd_monitors = get_monitors_result("SELECT * FROM monitors WHERE RESOLUTION = '1440' AND PANEL_TYPE = 'LCD' ORDER BY PRICE;")
    uhd_monitors = get_monitors_result("SELECT * FROM monitors WHERE RESOLUTION = '2160' AND PANEL_TYPE = 'LCD' ORDER BY PRICE;")
    lcd_monitors = [fhd_monitors[0],fhd_monitors[1], qhd_monitors[0], qhd_monitors[1], uhd_monitors[0], uhd_monitors[1]]
    return lcd_monitors



if __name__ == '__main__':
    app.run(debug=True)