from flask import Flask, render_template, request

import glob, sys, fitz
from bs4 import BeautifulSoup
import urllib
import pandas as pd
from IPython.display import clear_output
import os

from blabel import LabelWriter
from sh import lp
import pandoc
import pypandoc
import urllib
from pyhtml2pdf import converter
from flask import send_file
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['text_input']
        # Do something with user_input here
        label_writer = LabelWriter("templates/pathway.html",
                                   default_stylesheets=("templates/pathway.css",))
        records = [
            dict(sample_id="s01", sample_name=user_input),
        ]
        label_writer.write_labels(records, target='static/label.pdf')

        # To get better resolution
        zoom_x = 0.75  # horizontal zoom
        zoom_y = 0.75  # vertical zoom
        mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension

        doc = fitz.open("static/label.pdf")  # open document
        for page in doc:  # iterate through the pages
            pix = page.get_pixmap(matrix=mat)  # render page to an image
            pix.save("static/label.png")  # store image as a PNG

        return render_template('result.html', result=user_input)
    else:
        return render_template('index.html')


@app.route('/print-confirmed', methods=['GET', 'POST'])
def print_label():
    lp_cp = lp.bake('-d')
    printername = 'UPS_Thermal_2844'
    filename = 'static/label.pdf'
    file2print = filename
    lp_cp(printername, file2print)
    return render_template('index.html')


@app.route('/breast/pdf', methods=['GET', 'POST'])
def generate_pdf_breast():
    print_options = {'paperWidth': 11,
                     'paperHeight': 8.5,
                     'marginTop': 0,
                     'marginBottom': 0,
                     'marginLeft': 0,
                     'marginRight': 0,
                     'scale': 0.75}
    # path = os.path.abspath('static/build/breast.html')
    # converter.convert(f'file:///{path}', 'static/build/breast.pdf', print_options=print_options)
    converter.convert('http://localhost:5000/breast', 'static/build/breast.pdf', print_options=print_options)
    try:
        return send_file('static/build/breast.pdf')
    except:
        return "PDF not found"


@app.route('/breast', methods=['GET', 'POST'])
def generate_html_breast():
    # file_path = "example_input.md"
    # with open(file_path, "r") as file:
    #     contents = file.read()
    #
    # doc =
    # doc.markdown = str(contents)
    # webConverted = doc.html
    # bare_html = pypandoc.convert_file('example_input.md', 'html')

    microsoft_url = "https://office365stanford-my.sharepoint.com/personal/agoodell_stanford_edu/_layouts/15/download.aspx?SourceUrl=%2Fpersonal%2Fagoodell%5Fstanford%5Fedu%2FDocuments%2Fmarkdown%5Fexample%2Emd"

    local_ondrive_path = '/Users/alexandergoodell/Library/CloudStorage/OneDrive-Stanford/clinical-pathways-documents/'
    specific_path = local_ondrive_path + 'breast.md'

    bare_html = pypandoc.convert_file(specific_path, 'html')
    #
    # file_path = "example_input.html"
    # with open(file_path, "r") as file:
    #     contents = file.read()

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
    print(df)

    pre = df.query("header == 'Preoperative'").to_dict(orient="records")
    intra = df.query("header == 'Intraoperative'").to_dict(orient="records")
    post = df.query("header == 'Postoperative'").to_dict(orient="records")
    context = {
        "pre": pre,
        "intra": intra,
        "post": post,
        'title': title
    }
    # template.render(context)

    content = render_template('pathway_template.html', pre=pre, intra=intra, post=post, title=title)
    with open("static/build/breast.html", "w") as file:
        file.write(content)

    return content


if __name__ == '__main__':
    app.run(host="0.0.0.0")
