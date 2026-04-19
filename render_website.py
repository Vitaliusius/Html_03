import json
import os
import math

from environs import env
from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked
from dotenv import load_dotenv


PATH_TO_LIBRARY = env.str("PATH_TO_LIBRARY")


def on_reload():
    os.makedirs("pages", exist_ok=True)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(["html"])
    )
    template = env.get_template("template.html")
    with open(PATH_TO_LIBRARY, "r", encoding="utf8") as my_file:
        books = json.load(my_file)
    books = list(chunked(books, 2))
    pages = list(chunked(books, 10))
    for i, page in enumerate(pages, 1):
        rendered_page = template.render(
            books=page,
            pages_count=math.ceil(len(pages)),
            current_page=i
            )
        with open(f"pages/index{i}.html", "w", encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == "__main__":
    load_dotenv()
    on_reload()
    server = Server()
    server.watch("template.html", on_reload)
    server.serve(root=".")
