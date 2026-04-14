import json

from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape


def on_reload():
    env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
    )

    template = env.get_template('template.html')

    with open("meta_data.json", "r", encoding="utf8") as my_file:
        books_json = my_file.read()
    books = json.loads(books_json)

    rendered_page = template.render(
        books=books,   
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    print("Site rebuilt")

on_reload()

server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')