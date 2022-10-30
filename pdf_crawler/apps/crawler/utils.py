
from io import BytesIO

import requests
from fake_useragent import UserAgent

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


__all__ = [
    'pdf_to_text',
    'check_url'
]


def pdf_to_text(pdf_file):
    manager = PDFResourceManager()
    byte_io = BytesIO()
    layout = LAParams(all_texts=True)
    device = TextConverter(manager, byte_io, laparams=layout)
    interpreter = PDFPageInterpreter(manager, device)
    for page in PDFPage.get_pages(pdf_file, check_extractable=True):
        interpreter.process_page(page)
    text = byte_io.getvalue()
    device.close()
    byte_io.close()
    return text


def check_url(url):
    ua = UserAgent()
    headers = {'User-Agent': str(ua.chrome)}
    res = requests.options(url, headers=headers)
    return True if res.status_code < 400 else False
