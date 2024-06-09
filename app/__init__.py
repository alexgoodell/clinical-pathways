from flask import Flask, render_template, request

import glob, sys, fitz
from bs4 import BeautifulSoup
import urllib
import pandas as pd
from IPython.display import clear_output
import os

from blabel import LabelWriter
# from sh import lp
import pandoc
import pypandoc
import urllib
from pyhtml2pdf import converter
from flask import send_file, redirect

app = Flask(__name__)


# TODO auth
# https://spdb.stanford.edu/spconfigs/new


def generate_html(markdown_path, format, style):
    markdown_contents = urllib.request.urlopen(markdown_path)
    bare_html = pypandoc.convert_file(markdown_path, format="markdown", to='html')
    soup = BeautifulSoup(bare_html, 'html.parser')
    title = soup.find('h1').text
    header = ""
    subheader = ""
    image_url = ""
    content_block = ""
    rows = []

    for sibling in soup.find('h1').next_siblings:
        if sibling.name == "h2":
            header = sibling.text
        if sibling.name == "p" or sibling.name == "ul":
            content_block += str(sibling)

        if sibling.name == "figure":
            image_url = sibling.find('img')['src']

        if sibling.name == "h3":
            row = {
                "header": header,
                "subheader": subheader,
                "image_url": image_url,
                "content_block": content_block,
            }
            rows.append(row)

            subheader = sibling.text
            content_block = ""

    df = pd.DataFrame(rows[1:])

    pre = df.query("header == 'Preoperative'").to_dict(orient="records")
    intra = df.query("header == 'Intraoperative'").to_dict(orient="records")
    post = df.query("header == 'Postoperative'").to_dict(orient="records")

    content = render_template('pathway_template.html', pre=pre, intra=intra, post=post, title=title, format=format,
                              style=style)
    # with open("app/static/build/breast.html", "w") as file:
    #     file.write(content)
    return content


@app.route('/', methods=['GET'])
def index():
    style = request.args.get('style', default='larissa', type=str)
    return render_template('index_template.html', style=style)


@app.route('/breast/pdf', methods=['GET'])
def generate_pdf_breast():
    print_options = {'paperWidth': 11,
                     'paperHeight': 8.5,
                     'marginTop': 0,
                     'marginBottom': 0,
                     'marginLeft': 0,
                     'marginRight': 0,
                     'scale': 0.75}
    # always uses default style "larissa"
    request_path = 'http://localhost:5000/breast/print'
    # path = os.path.abspath('static/build/breast.html')
    # converter.convert(f'file:///{path}', 'static/build/breast.pdf', print_options=print_options)
    converter.convert(request_path, 'app/static/build/breast.pdf', print_options=print_options)
    try:
        return send_file('static/build/breast.pdf')
    except:
        return "PDF not found"


@app.route('/breast/print', methods=['GET'])
def generate_print_html():
    style = request.args.get('style', default='larissa', type=str)
    return generate_html(markdown_path='https://hackmd.io/@stanford-anesthesia/HJjHfGv6a/download', format="print",
                         style=style)


@app.route('/breast', methods=['GET'])
def generate_web_html():
    style = request.args.get('style', default='larissa', type=str)
    return generate_html(markdown_path='https://hackmd.io/@stanford-anesthesia/HJjHfGv6a/download', format="web",
                         style=style)


## fallback redirect
@app.route('/')
@app.route('/<first>')
@app.route('/<first>/<path:rest>')
def fallback(first=None, rest=None):
    redirects = {'meld': '/meld-na',
                 'chatbot': '/chat',
                 'bot': '/chat',
                 'chat': 'https://chat.openai.com/g/g-mtNkUsX41-openmedcalc',
                 'paper': 'https://www.medrxiv.org/content/10.1101/2023.12.13.23299881v1',
                 'preprint': 'https://www.medrxiv.org/content/10.1101/2023.12.13.23299881v1'}

    try:
        if redirects[first]:
            return app.redirect(location=redirects[first], code=302)
    except KeyError:
        pass
    return "Error 404: Page not found"


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
