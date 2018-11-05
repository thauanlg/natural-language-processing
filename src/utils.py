import operator, nltk
spurius = ['\x93','\x94','\x95','\x97']

def alteraTextos(text, dicSinonimos):
    newText=[0]*len(text)
    for i in range(0, len(text)):
        for j in range(0, len(text[i])):
            for k in range(0, len(spurius)):
                if text[i][j].find(spurius[k]) != -1:
                    text[i][j]=text[i][j].replace(spurius[k],'')
                    break
            try:
                text[i][j]=text[i][j]
                text[i][j]="{\'"+text[i][j]+"\':"+str(dicSinonimos[text[i][j].lower()])+"}"
            except:
                pass
        newText[i] = re.sub(r' \n\n','\n\n', re.sub(r' - ','-', " ".join(text[i])))
    return newText

# Obtem todas as palavras
def getTodasPalavras(tagger, texto, padrao):
    words = []

    #percorre todas as sentenças do texto k
    for i in range(0, len(texto)):
        # realiza o tag de uma sentença do livro, retornando um sentença com as tags
        tag_text = tagger.tag(texto[i])
        for j in range(0, len(tag_text)):
            w = tag_text[j][0].lower()
            # adiciona as palavras que são substantivos na lista words
            if tag_text[j][1] in padrao and w not in words:
                words.append(w)
    return words

def lematizaPalavras(unitex, words):
    # Lematiza as palavras
    lemWords = []
    for i in range(0, len(words)):
        try:
            lemWords.append(unitex[words[i]])
        except:
            lemWords.append(words[i])
    return lemWords

# Calcula as palavras difíceis
def getPalavrasDificeis(brasileiro, words, limiar):
    hard_words = []
    for i in range(0, len(words)):
        try:
            if brasileiro[words[i]] < limiar :
                hard_words.append(i)
        except:
            hard_words.append(i)
    return hard_words

# Obtendo os melhores sinonimos
def getMelhoresSinonimos(sinonimos, brasileiro, numSin, words, lemWords):
    dicSinonimos = {}
    for i in range(0, len(lemWords)):
        sin=[]
        try:
            todosSins = sinonimos[lemWords[i]]
            aux={}
            for sins in todosSins:
                try:
                    aux[sins] = brasileiro[sins]
                except:
                    pass
            best = sorted(aux, key=aux.get, reverse=True)
            n = numSin if len(best) > numSin else len(best)
            for j in range(0, n):
                sin.append(best[j])
            #if n == 0:
                #sin=[lemWords[i]]
        except:
            pass
            #sin=[lemWords[i]]
        if sin != []:
           dicSinonimos[words[i]]=sin
    return dicSinonimos

def getWordsIdx(words, idx):
    aux = [0]*len(idx)
    for i in range(0, len(idx)):
        aux[i]=words[idx[i]]
    return aux

def getPalavrasCsv(dic, words):
    ids = []
    for i in range(1, len(words)):
        try:
            if float(dic[words[i]]) > 6:
                ids.append(i)
        except:
            ids.append(i)
    return ids

def structureText(text):
    paragraph = str(text).split('\n\n')
    sents=[]
    for para in paragraph:
        sent = nltk.sent_tokenize(para)
        for i in range(0, len(sent)):
            sents.append(nltk.word_tokenize(sent[i]))
        sents[len(sents)-1].extend(['\n\n'])
    return sents
