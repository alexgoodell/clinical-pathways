# method 1 - uses selenium

import os
from pyhtml2pdf import converter

path = os.path.abspath('templates/pathway_human.html')
print_options = {'paperWidth': 11,
                'paperHeight': 8.5,
                'marginTop': 0,
                'marginBottom': 0,
                'marginLeft': 0,
                'marginRight': 0,
                 'scale': 0.75}
converter.convert(f'file:///{path}', 'py_converted.pdf', print_options=print_options)



# method 2 - xhtml2pdf - uses reportlab backend
# in console xhtml2pdf templates/pathway_human.html
