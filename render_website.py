import json
from math import ceil
from os import makedirs

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

with open('books_data.json', 'r') as my_file:
    books_data_json = my_file.read()


books_data = json.loads(books_data_json)

number_of_books_on_page = 10
books_data_chunked = chunked(books_data, number_of_books_on_page)
page_counts = ceil(len(books_data) / number_of_books_on_page)


def on_reload():
    template = env.get_template('template.html')
    makedirs('pages', exist_ok=True)
    for current_page, books_on_page in enumerate(books_data_chunked, start=1):
        books_on_page_two_column = chunked(books_on_page, 2)
        rendered_page = template.render(books_on_page=books_on_page_two_column, page_counts=page_counts, current_page=current_page)
        with open(f'pages/index{current_page}.html', 'w', encoding='utf8') as file:
            file.write(rendered_page)


on_reload()

server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')
