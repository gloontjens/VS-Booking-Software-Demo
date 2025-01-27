from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa
from random import randint
import os

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    
#    file = open("my.file.pdf", "wb")
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#    file.close()
    
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def render_to_pdf_file(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    
    file = open("myfile.pdf", "wb")
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), file)
    file.close()

    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    
    file_name = "myfile.pdf"
    file_path = os.path.join(os.path.abspath(os.path.dirname("__file__")), "", file_name)
 
    return [file_path, result.getvalue()]


