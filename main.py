from collections import defaultdict
from datetime import datetime
from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler

import pandas as pd
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)
shop_age = datetime.now().year - 1920
path = 'wine3.xlsx'


def get_valid_name_for_year(year):
    if year % 100 > 4 or year % 100 == 0:
        return 'лет'
    elif year % 10 == 1:
        return 'год'
    else:
        return 'года'


def get_dictionary_for_template(path):
    wine_table = pd.read_excel(path)
    wine_table.fillna('', inplace=True)

    wine = defaultdict(list)

    for category, *wine_item in wine_table.values:
        wine[category].append(
            {wine_field: value for wine_field, value in zip(wine_table.columns[1:], wine_item)}
        )

    return wine


def main():
    year_valid = get_valid_name_for_year(shop_age)
    wine = get_dictionary_for_template(path)

    template = env.get_template('template.html')
    rendered_page = template.render(
        wine_shop_age=f'{shop_age} {year_valid}',
        wine=wine
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()