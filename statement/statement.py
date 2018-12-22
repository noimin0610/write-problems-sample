# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import codecs
import glob
import re
import sys

if sys.version_info[0] == 2:
    import urllib as _urllib
else:
    import urllib.request as _urllib

from markdown import markdown
import pdfkit


def escape_special_characters(s):
    r = ''
    math = False
    for c in s:
        if c == '$':
            math = not math
        if math and c in r'\`*_{}[]()#+-.!':
            r += '\\'
        r += c
    return r


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--download', action='store_true')
parser.add_argument('-i', '--id')
parser.add_argument('-o', '--output', default='html', choices=['html', 'pdf'])
args = parser.parse_args()

ids = ['A']

files = [
    '1w393hUNjYyh6OENbMSEgnTDnPrhfhKYXJ97XKvLiE2A'
]

titles = [
    'A+B'
]

apikey = '*****'

with open('header-html.html') as f:
    header = f.read()
with open('header-pdf.html') as f:
    pdf_header = f.read()

if args.download:
    for id, file in zip(ids, files):
        if args.id and id != args.id:
            continue
        print('Download {0} ... '.format(id), end='')
        sys.stdout.flush()
        url = 'https://www.googleapis.com/drive/v3/files/{0}/export?mimeType=text/plain&key={1}'.format(file, apikey)
        _urllib.urlretrieve(url, '{0}.md'.format(id))
        print('Done')

pdf_html = ''
for id, title in zip(ids, titles):
    if args.id and id != args.id:
        continue
    print('Convert {0} ... '.format(id), end='')
    sys.stdout.flush()
    md_data = ''
    first_line = True
    with codecs.open('{0}.md'.format(id), encoding='utf-8') as md_file:
        s = 1
        for line in md_file.readlines():
            if line.startswith('&HTML'):
                if args.output == 'pdf':
                    continue
                line = line[6:]
            if line.startswith('&PDF'):
                if args.output == 'html':
                    continue
                line = line[5:]

            if first_line:
                first_line = False
                line = line[3 if sys.version_info[0] == 2 else 1:]

            if line.startswith('### Problem Statement'):
                if args.output == 'html':
                    md_data = ''
                else:
                    continue

            if line.startswith('### Input') or line.startswith('### Note'):
                if args.output == 'html':
                    md_data += '___\n'
                md_data += line
            else:
                md_data += escape_special_characters(line)
        md_data += '\n'

        md_data = re.sub('’', '\'', md_data)
        md_data = re.sub('”', '\"', md_data)
        html = markdown(md_data, extensions=['markdown.extensions.fenced_code', 'markdown.extensions.tables'])
        html = re.sub('<blockquote>\n<p>', '<blockquote>', html)
        html = re.sub('</p>\n</blockquote>', '</blockquote>', html)
        html = re.sub('<pre><code>', '<pre>', html)
        html = re.sub('</code></pre>', '</pre>', html)

        input_files = sorted(glob.glob('../{0}/rime-out/tests/*sample*.in'.format(title)))
        diff_files = sorted(glob.glob('../{0}/rime-out/tests/*sample*.diff'.format(title)))
        sample = ''
        if args.output == 'html':
            for i, (input_file, diff_file) in enumerate(zip(input_files, diff_files)):
                sample += '<hr>'
                sample += '<h3>Sample Input {0}</h3>'.format(i + 1)
                sample += '<pre>'
                with open(input_file) as f:
                    sample += f.read()
                sample += '</pre>'
                sample += '<h3>Output for Sample Input {0}</h3>'.format(i + 1)
                sample += '<pre>'
                with open(diff_file) as f:
                    sample += f.read()
                sample += '</pre>'
        else:
            sample += '<div class="no-page-break"><h3>Examples</h3>'
            sample += '<table><tr><th>Input</th><th>Output</th></tr>'
            for i, (input_file, diff_file) in enumerate(zip(input_files, diff_files)):
                sample += '<tr><td><pre>'
                with open(input_file) as f:
                    sample += f.read()
                sample += '</pre></td><td><pre>'
                with open(diff_file) as f:
                    sample += f.read()
                sample += '</pre></td></tr>'
            sample += '</table></div>'
        html = re.sub('&amp;sample', sample, html)

        if args.output == 'html':
            with codecs.open('{0}.html'.format(id), 'w', encoding='utf-8') as f:
                f.write(header + html)
        else:
            pdf_html += html

    print('Done')

if args.output == 'pdf':
    print('Convert PDF ... ', end='')
    sys.stdout.flush()
    options = {
        'page-size': 'A4',
        'margin-top': 24,
        'margin-right': 16,
        'margin-bottom': 16,
        'margin-left': 16,
        'encoding': 'UTF-8',
        'javascript-delay': '10000',
        'header-center': 'Sample',
        'header-font-name': 'Times New Roman',
        'header-font-size': 10,
        'header-spacing': 12,
        'footer-center': '[page] / [toPage]',
        'footer-font-name': 'Times New Roman',
        'footer-font-size': 8,
        'footer-spacing': 8,
    }
    pdfkit.from_string(pdf_header + pdf_html, 'statement.pdf', options=options)
    print('Done')
