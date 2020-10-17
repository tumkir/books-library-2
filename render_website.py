import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

with open("books_data.json", "r") as my_file:
    books_data_json = my_file.read()

books_data = json.loads(books_data_json)


def on_reload():
    template = env.get_template('template.html')
    rendered_page = template.render(books=books_data)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


on_reload()

server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')
