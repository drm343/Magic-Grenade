#!/usr/bin/env python3
from os import listdir
import re

import markdown
from trender import TRender


files = listdir('src')


extensions = ['meta', 'tables', 'attr_list']
md = markdown.Markdown(extensions = extensions)
file = {}


def open_file(name):
    with open('src/' + name, 'r') as f:
        tmp = f.read()
        md_file = re.sub('.md\)', '.html)', tmp)

        body = md.convert(md_file)

        try:
            file['title'] = md.Meta['title'][0]
        except Exception:
            pass

        try:
            file['output'] = md.Meta['html'][0]
        except Exception:
            file['output'] = name + '.html'

        file['body'] = body


def main():
    with open('templates/base.html', 'r') as f:
        base = f.read()
        template = TRender(base)


    with open('style/style.css', 'r') as f:
        file['style'] = f.read()


    if not files:
        return

    for i in files:
        open_file(i)
        result = template.render(file)

        with open('docs/' + file['output'], 'w') as f:
            f.write(result)


if __name__ == '__main__':
    main()
