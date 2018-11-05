import os
import json
import yattag

i = 0

page = ""
n = 0
with open('aires.txt', 'r', encoding='ISO-8859-1') as f:
    for line in f:
        if len(page) + len(line) > 1000:
            with open('{:03d}'.format(n) + '.tmp', 'w+') as out:
                out.writelines(page)
            n += 1
            page = str(line)
        else:
            page += line

pages = []
for f in os.listdir('.'):
    if f.endswith('.tmp'):
        pages.append(f)
pages = list(sorted(pages))

for p in pages:
    book = ""
    name = p.split('.')[0]
    with open(name + '.tmp', 'r') as f:
        newlines = 0
        paragraph = ""
        for line in f:
            line = line.strip()
            if len(line) == 0:
                newlines += 1
            else:
                paragraph += line + '\n'

            if newlines == 2:
                doc,tag,text = yattag.Doc().tagtext()
                with tag('p'):
                    text(paragraph)
                book += doc.getvalue()

                newlines = 0
                paragraph = ""

    if newlines != 2:
        doc,tag,text = yattag.Doc().tagtext()
        with tag('p'):
            text(paragraph)
        book += doc.getvalue()

    aux = str(book)
    book = ""
    i = 0
    last = 0
    print(name)
    while i < len(aux):
        begin = i
        if aux[i] == '{':
            book += aux[last:i]
            last = i
            match = False
            while not match:
                if aux[i] == '}':
                    match=True
                i += 1
        end = i
        i += 1

        if begin != end:
            hard, simple = list(json.loads(aux[begin:end]).items())[0]
            if len(simple) != 1:
                simple = ', '.join(map(str, simple[:-1])) + ' ou ' + simple[-1]
            else:
                simple = simple[0]
            doc,tag,text = yattag.Doc().tagtext()
            with tag('span', klass='hardword'):
                text(hard)
            with tag('span', klass='tooltiptext'):
                text(simple)
            book += ' ' + doc.getvalue() + ' '
            last = i

    if begin == end:
        book += aux[last:i]

    with open(name + '.html', 'w+') as f:
        f.writelines(book)
