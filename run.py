#!/usr/bin/env python3
#
# MIT License
# 
# Copyright (c) 2022 erlin
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import os
from os import listdir
from os.path import isdir
import re

import markdown
from trender import TRender


files = listdir('src')


extensions = ['meta', 'tables', 'attr_list', 'toc']
md = markdown.Markdown(extensions = extensions)
file = {}


def prepare_filename(name):
    if isdir('src/' + name):
        try:
            os.mkdir('docs/' + name)
        except:
            pass

        files = listdir('src/' + name)

        for i in files:
            open_file(name + '/' + i)
    else:
        open_file(name)


def open_file(name):
    with open('src/' + name, 'r') as f:
        tmp = f.read()
        md_file = re.sub('.md\)', '.html)', tmp)

        body = md.convert(md_file)

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
        prepare_filename(i)
        result = template.render(file)

        with open('docs/' + file['output'], 'w') as f:
            f.write(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('title', help = "Aticle's Title")
    parser.add_argument('author', help = "Aticle's Author")
    args = parser.parse_args()

    if args.title and args.author:
        file['title'] = args.title
        file['author'] = args.author
        main()
    else:
        parser.print_help()
