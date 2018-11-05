# Cria um tagger e realizando o tagging em um texto do Machado, salvandos os substantivos em um arquivos json
from nltk.corpus import machado
import nltk, json, csv, re
exec(open('loadResources.py','r').read())
exec(open('utils.py','r').read())
exec(open('cliticos.py','r').read())

def execSimplica(texto):
    # adjetivos
    print("ADJETIVOS")
    print("Obtendo palavras")
    words = getTodasPalavras(tagger, texto, ['ADJ'])
    print("Lematizando")
    lemWords = lematizaPalavras(unitex, words)
    print("Obtendo dificeis")
    idx = getPalavrasDificeis(brasileiro, lemWords, 800)
    words = getWordsIdx(words, idx)
    lemWords = getWordsIdx(lemWords, idx)

    idx = getPalavrasCsv(dic, lemWords)
    words = getWordsIdx(words, idx)
    lemWords = getWordsIdx(lemWords, idx)

    print("Obtendo sinonimos")
    dicSinonimos = getMelhoresSinonimos(sinonimos, brasileiro, 3, words, lemWords)

    # adverbios
    print("\nADVÉRBIOS")
    print("Obtendo palavras")
    words = getTodasPalavras(tagger, texto, ['ADV','ADV-KS','ADV-KS-REL'])
    print("Lematizando")
    lemWords = lematizaPalavras(unitex, words)
    print("Obtendo dificeis")
    idx = getPalavrasDificeis(brasileiro, lemWords, 6000)
    words = getWordsIdx(words, idx)
    lemWords = getWordsIdx(lemWords, idx)

    idx = getPalavrasCsv(dic, lemWords)
    words = getWordsIdx(words, idx)
    lemWords = getWordsIdx(lemWords, idx)

    print("Obtendo sinonimos")
    dicSinonimos.update(getMelhoresSinonimos(sinonimos, brasileiro, 3, words, lemWords))

    # substantivos
    print("\nSUBSTANTIVOS")
    print("Obtendo palavras")
    words = getTodasPalavras(tagger, texto, ['N'])
    print("Lematizando")
    lemWords = lematizaPalavras(unitex, words)
    print("Obtendo dificeis")
    idx = getPalavrasDificeis(brasileiro, lemWords, 3000)
    words = getWordsIdx(words, idx)
    lemWords = getWordsIdx(lemWords, idx)

    idx = getPalavrasCsv(dic, lemWords)
    words = getWordsIdx(words, idx)
    lemWords = getWordsIdx(lemWords, idx)

    print("Obtendo sinonimos")
    dicSinonimos.update(getMelhoresSinonimos(sinonimos, brasileiro, 3, words, lemWords))
    
    return dicSinonimos

def execAll(title):
    texto = machado.raw(title)
    texto = structureText(texto)
    dicSinonimos = execSimplica(texto)
    texto = alteraTextos(texto, dicSinonimos)
    
    print("\nSimplificações Gramaticais")
    for i in range(0, len(texto)):
        mesoclise = processa_mesoclise(texto[i], tagger)
        for meso in mesoclise:
            texto[i]=re.sub(meso[0], "{\'"+meso[0]+"\':[\'"+meso[1]+"\']}", texto[i])
        
        mesoclise = processa_contracao(texto[i], tagger, unitex)
        for meso in mesoclise:
            meso=list(meso)
            meso[0]= " ".join(meso[0].split())
            texto[i]=re.sub(meso[0], "{\'"+meso[0]+"\':[\'"+meso[1]+"\']}", texto[i])

        mesoclise = inverter_negacao(texto[i])
        for meso in mesoclise:
            texto[i]=re.sub(meso[0], "{\'"+meso[0]+"\':[\'"+meso[1]+"\']}", texto[i])
        
        mesoclise = enclises_raras(texto[i])
        for meso in mesoclise:
            texto[i]=re.sub(meso[0], "{\'"+meso[0]+"\':[\'"+meso[1]+"\']}", texto[i])
    texto = ''.join(texto)
    return texto

# Esta lista indeicam as obras simplificadas por nós neste trabalho, porém pode se escolher qualquer obra de Machado e adicionar
# nas lista abaixo. A lista "names" contém os nomes pelo qual podemos acessar as respectivas obras do Machado utilizando o
# córpus Machado do nltk.
p = ["Memórias Póstumas de Brás Cubas", "\nQuincas Borba", "\nDom Casmurro", "\nEsaú e Jacó", "\nMemorial de Aires"]
titles = ['cubas.txt','borbas.txt','casmurro.txt','esau.txt','aires.txt']
names = ['marm05.txt', 'marm07.txt', 'marm08.txt','marm09.txt', 'marm10.txt']

# Os textos no formato simplificado serão armazenados na pasta saida
for i in range(0, len(titles)):
    print(p[i])
    open('../saida/'+titles[i], 'w').write(execAll('romance/'+names[i]))
