import os
from pyhtml2pdf import converter

path = os.path.abspath('templates/pathway_human.html')
converter.convert(f'file:///{path}', 'py_converted.pdf')