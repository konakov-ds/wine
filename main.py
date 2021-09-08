from collections import defaultdict
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
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

wine_data = pd.read_excel('wine3.xlsx')
wine_data.fillna('', inplace=True)
wine_dict = defaultdict(list)

for wine_item in wine_data.values:
    wine_dict[wine_item[0]].append(
        {'Картинка': wine_item[4],
         'Категория': wine_item[0],
         'Название': wine_item[1],
         'Сорт': wine_item[2],
         'Цена': wine_item[3],
         'Акция': wine_item[5]
         }
    )

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    wine_shop_lifetime=f'{shop_lifetime} {year_incline}',
    wine_dict=wine_dict
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()