from flask import Flask, render_template, request

import glob, sys, fitz



from blabel import LabelWriter
from sh import lp


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['text_input']
        # Do something with user_input here
        label_writer = LabelWriter("templates/pathway.html",
                                   default_stylesheets=("templates/pathway.css",))
        records= [
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
    lp_cp (printername, file2print)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0") 