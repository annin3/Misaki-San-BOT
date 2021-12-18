import io
import os
import re
import datetime

from google.cloud import vision

def get_result(output):
    list = output.split()

    search_name = ""
    result = True
    date = None

    for l in list:
        if 'の検索結果' in l:
            search_name = re.findall(r'「(.*)」', l)[0]
        if '見つかりませんでした' in l:
            result = False
        if r'/' in l:
            date = datetime.datetime.strptime(l, '%H:%M%Y/%m/%d')

    d_week = {'Sun': '日', 'Mon': '月', 'Tue': '火', 'Wed': '水', 'Thu': '木', 'Fri': '金', 'Sat': '土'}
    w = d_week[date.strftime('%a')]
    d = date.strftime('%Y年%m月%d日') + f'（{w}）' + date.strftime('%H:%M')
    return search_name, result, d

def get_text(path):
    client = vision.ImageAnnotatorClient()
    file_name = os.path.abspath(path)

    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response =  client.document_text_detection(
            image=image,
            image_context={'language_hints': ['ja']}
        )

    output_text = ''
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    output_text += ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                output_text += '\n'
    return get_result(output_text)

