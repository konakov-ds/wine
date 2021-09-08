from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
import pandas as pd

def year_incline(year):
    if year % 100 > 4 or year % 100 == 0:
        return 'лет'
    elif year % 10 == 1:
        return 'год'
    else:
        return 'года'


shop_lifetime = datetime.now().year - 1920
year_incline = year_incline(shop_lifetime)

wine_data = pd.read_excel('wine.xlsx').values

wine_items = [{'brand': i[0], 'grape_type': i[1], 'price': i[2], 'img': f'images/{i[3]}'} for i in wine_data]

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    wine_shop_lifetime=f'{shop_lifetime} {year_incline}',
    wine_items=wine_items
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
