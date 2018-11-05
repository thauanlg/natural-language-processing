import json
import yattag

book = ""

with open('ex.txt', 'r') as f:
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
        book += doc.getvalue()
        last = i

if begin == end:
    book += aux[last:i]

with open('ex.html', 'w+') as f:
    f.writelines(book)
