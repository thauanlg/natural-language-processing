import re
import nltk
import json

### CLÍTICOS
### Este módulo adapta uma série de fenômenos relacionados a pronomes clíticos
### por meio de expressões regulares. A adaptação se dá de uma variante padrão
### do século XIX para o português brasileiro contemporâneo.
### A entrada dessas funções deve ser uma string correspondente a uma frase.
### Sua saída é uma lista de tuplas no formato (original, adaptado).
### Os fenômenos contemplados são:
### - Mesóclise
### - Contração pronominal
### - Inversão da ordem da sequência negativa-clítico.
### - Adaptação de ênclises raras com  o verbo "fazer".

### Cria um dicionário de regência verbal no formato lemma : preposição.
### Esse dicionário é utilizado para adaptar contrações pronominais.
lista = open('../dados/txt/regencias_propbank.txt', 'r').read().split('\n')
regencias = dict()
for item in lista:
    if len(item) > 0:
        dupla = item.split(' ')
        regencias[dupla[0]] = dupla[1]

### REGRAS PARA TRATAMENTO DE MESÓCLISE

def achar_mesoclise(frase):
    ### Cria uma lista com os verbos mesoclíticos de uma frase.
        ### A frase deve ser uma string.
        mesocliticas = []
        mesocliticas.extend(re.findall(r'(^\w*?-[mtvnls]h?[eoa]s?-[íi]?[eáãa][im]?o?s?)[\s,\.\?!:;;]', frase))
        mesocliticas.extend(re.findall(r'[\s\(](\w*?-[mtvnls]h?[eoa]s?-[íi]?[eáãa][im]?o?s?)[\s,\.\?!:;\)]', frase))
        return mesocliticas

def auxiliarizacao_fut(mesoclitica):
    ### Toma um token mesoclítico como argumento e retorna
        ### uma perífrase com verbo "ir".
        ### Exemplo:
        ### >>> auxiliarizacao_fut("dá-lo-íamos")
        ### 'íamos o dar'
        try:
            proclitica = re.sub(r'^(\w*?-[mtvnls]h?[eoa]s?-)(ei)$', r'\1vou', mesoclitica)
            proclitica = re.sub(r'^(\w*?-[mtvnls]h?[eoa]s?-)(ás?)$', r'\1vai', proclitica)
            proclitica = re.sub(r'^(\w*?-[mtvnls]h?[eoa]s?-)(í?eis)$', r'\1vão', proclitica)
            proclitica = re.sub(r'^(\w*?-[mtvnls]h?[eoa]s?-)(emos)$', r'\1vamos', proclitica)
            proclitica = re.sub(r'^(\w*?-[mtvnls]h?[eoa]s?-)(ão)$', r'\1vão', proclitica)
            proclitica = re.sub(r'^([Ff][áa]r?)-([mtvnls]h?[eoa]s?)-([víi]\w*?)$', r'\3 \2 fazer', proclitica)
            proclitica = re.sub(r'^([tT]r[áa])-([mtvnls]h?[eoa]s?)-([víi]\w*?)$', r'\3 \2 trazer', proclitica)
            proclitica = re.sub(r'^([Dd]ir?)-([mtvnls]h?[eoa]s?)-([víi]\w*?)$', r'\3 \2 dizer', proclitica)
            proclitica = re.sub(r'^(\w*?)[áa]-([mtvnls]h?[eoa]s?)-([víi]\w*?)$', r'\3 \2 \1ar', proclitica)
            proclitica = re.sub(r'^(\w*?)[êe]-([mtvnls]h?[eoa]s?)-([víi]\w*?)$', r'\3 \2 \1er', proclitica)
            proclitica = re.sub(r'^(\w*?)[ií]-([mtvnls]h?[eoa]s?)-([víi]\w*?)$', r'\3 \2 \1ir', proclitica)
            proclitica = re.sub(r'^(\w*?)[ôo]-([mtvnls]h?[eoa]s?)-([víi]\w*?)$', r'\3 \2 \1or', proclitica)
            proclitica = re.sub(r'^(\w*?)-([mtvnls]h?[eoa]s?)-([víi]\w*?)$', r'\3 \2 \1', proclitica)
            if proclitica != mesoclitica:
                proclitica = re.sub(r' l([ao]s?) ', r' \1 ', proclitica)
                return proclitica.lower()
            else:
                return proclitica
        except:
            return mesoclitica

def sufixacao_fut(mesoclitica):
    ### Toma um token mesoclitico como argumento e retorna
        ### o futuro sintético + clítico.
        ### Exemplo:
        ### >>> sufixacao_fut("tê-lo-emos")
        ### 'teremos o'
        ### ESTA REGRA DEVE SER UTILIZADA QUANDO:
        ###  1- O TOKEN SEGUINTE AO VERBO TAMBÉM FOR UM VERBO.
        ###  2- A SAÍDA FOR DIFERENTE DA ENTRADA.
        ### Caso contrário, utilizar
        ### auxiliarizacao_fut.
        try:
            proclitica = re.sub(r'^([tT][êe]r?-)([mtvnls]h?[eoa]s?)-(\w*?)$', r'\1\3 \2', mesoclitica)
            proclitica = re.sub(r'^([Hh]av[êe]r?-)([mtvnls]h?[eoa]s?)-(\w*?)$', r'\1\3 \2', proclitica)
            proclitica = re.sub(r'^([Pp]od[êe]r?-)([mtvnls]h?[eoa]s?)-(\w*?)$', r'\1\3 \2', proclitica)
            proclitica = re.sub(r'^([Dd]ev[êe]r?-)([mtvnls]h?[eoa]s?)-(\w*?)$', r'\1\3 \2', proclitica)
            proclitica = re.sub(r'^([Ii]r-)([mtvnls]h?[eoa]s?)-(\w*?)$', r'\1\3 \2', proclitica)
            if proclitica != mesoclitica:
                proclitica = re.sub(r' l([ao]s?)$', r' \1 ', proclitica)
                proclitica = re.sub(r'á-', r'ar', proclitica)
                proclitica = re.sub(r'ê-', r'er', proclitica)
                proclitica = re.sub(r'i-', r'ir', proclitica)
                proclitica = re.sub(r'[oô]-', r'or', proclitica)
                proclitica = re.sub(r'r-', r'r', proclitica)
                return proclitica.lower()
            else:
                return proclitica
        except:
            return mesoclitica

def processa_mesoclise(frase, tagger):
    ### Toma uma string como entrada. Encontra mesóclises
        ### e as transforma em outras estruturas,
        ### utilizando as funções acima.
        ### ATENÇÃO, COMPUTEIROS: INCLUIR AQUI A FUNÇÃO QUE CHECA A POS-TAG DA PALAVRA SEGUINTE.
        originais = achar_mesoclise(frase)
        original_simplificado = []
        for item in originais:
            aux = frase.split(item[0][0])[1].split(' ')
            if(len(aux) > 1 and aux[0] == ''):
                palavra_seguinte = str(tagger.tag([aux[1]])[0][1])
            elif len(aux) > 1:
                palavra_seguinte = str(tagger.tag([aux[0]])[0][1])
            else:
                palavra_seguinte = "N"

            sufix = sufixacao_fut(item)
            if item != sufix and palavra_seguinte == 'V':
                original_simplificado.append((item, sufix))
            else:
                original_simplificado.append((item, auxiliarizacao_fut(item)))
        return original_simplificado

# REGRAS PARA TRATAMENTO DE CONTRAÇÃO PRONOMINAL

def achar_contracoes(sent, x):
    ### Toma uma string como entrada e retorna todas as ocorrências de
    ### contração pronominal + verbo e um contexto de x palavras adiante.
    ### Os argumentos das funções abaixo devem ser as strings que resultam
    ### desta função.
    sent = re.sub(r'\n', ' ', sent)
    contracts = []
    contracts.extend(re.findall(r'\s(m[oa]\s\w.*?[\s\.,\?!;:\)]' + (x * '\S*?[\s\.,\?!;:\)]') + ')', sent))
    contracts.extend(re.findall(r'\s(t[oa]s?\s\w.*?[\s\.,\?!;:\)]' + (x * '\S*?[\s\.,\?!;:\)]') + ')', sent))
    contracts.extend(re.findall(r'\s(\S*?-m[oa]s?[\s\.,\?!;:\)]' + (x * '\S*?[\s\.,\?!;:\)]') + ')', sent))
    contracts.extend(re.findall(r'\s(\S*?-t[oa]s?[\s\.,\?!;:\)]' + (x * '\S*?[\s\.,\?!;:\)]') + ')', sent))
    contracts.extend(re.findall(r'^(\S*?-m[oa]s?[\s\.,\?!;:\)]' + (x * '\S*?[\s\.,\?!;:\)]') + ')', sent))
    contracts.extend(re.findall(r'^(\S*?-t[oa]s?[\s\.,\?!;:\)]' + (x * '\S*?[\s\.,\?!;:\)]') + ')', sent))
    contracts.extend(re.findall(r'\s(\S*?-lh[oa]s?[\s\.,\?!;:\)]' + (x * '\S*?[\s\.,\?!;:\)]') + ')', sent))
    contracts.extend(re.findall(r'^(\S*?-lh[oa]s?[\s\.,\?!;:\)]' + (x * '\S*?[\s\.,\?!;:\)]') + ')', sent))
    contracts.extend(re.findall(r'\s(lh[oa]s?\s\w.*?[\s\.,\?!;:\)]' + (x * '\S*?[\s\.,\?!;:\)]') + ')', sent))
    contracts.extend(re.findall(r'\s([nv]o-l[oa]s?\s\w.*?[\s\.,\?!;:\)]' + (x * '\S*?[\s\.,\?!;:\)]') + ')', sent))
    contracts.extend(re.findall(r'\s(\S*?-[nv]o-l[oa]s?[\s\.,\?!;:\)]' + (x * '\S*?[\s\.,\?!;:\)]') + ')', sent))
    contracts.extend(re.findall(r'^(\S*?-[nv]o-l[oa]s?[\s\.,\?!;:\)]' + (x * '\S*?[\s\.,\?!;:\)]') + ')', sent))
    contracts.extend(re.findall(r'\s(lhe-l[oa]s?\s\w.*?[\s\.,\?!;:\)]' + (x * '\S*?[\s\.,\?!;:\)]') + ')', sent))
    contracts.extend(re.findall(r'\s(\S*?-lhe-l[oa]s?[\s\.,\?!;:\)]' + (x * '\S*?[\s\.,\?!;:\)]') + ')', sent))
    contracts.extend(re.findall(r'^(\S*?-lhe-l[oa]s?[\s\.,\?!;:\)]' + (x * '\S*?[\s\.,\?!;:\)]') + ')', sent))
    return contracts

def preposicionar(contracao, prep):
    ### Toma uma string contendo verbo e contração pronominal (contracao)
        ### e uma preposição para introdução do dativo (prep). Desmembra a contração
        ### em pronome acusativo e sintagma preposicional com pronome dativo tônico.
        ### Exemplo:
        ###     >>> preposicionar("mos contou", "a")
        ###     "os contou a mim"
        ### ESTA REGRA DEVE SER APLICADA QUANDO A SEGUINTE NÃO SE APLICAR.
        try:
            prepos = re.sub('^m([oa]s?)\s(\w*?)[\s\.,\)\?!:;]$', r'\1 \2 ' + prep + r' mim', contracao)
            prepos = re.sub('^(\w.*?-)m([oa]s?)[\s\.,\)\?!:;]', r'\1\2 ' + prep + r' mim', prepos)
            prepos = re.sub('^t([oa]s?)\s(\w*?)[\s\.,\)\?!:;]$', r'\1 \2 ' + prep + r' ti', prepos)
            prepos = re.sub('^(\w.*?-)t([oa]s?)[\s\.,\)\?!:;]', r'\1\2 ' + prep + r' ti', prepos)
            prepos = re.sub('^lh([oa]s?)\s(\w*?)[\s\.,\)\?!:;]$', r'\1 \2 ' + prep + ' ele(a)', prepos)
            prepos = re.sub('^(\w.*?-)lh([oa]s?)[\s\.,\)\?!:;]', r'\1\2 ' + prep + r' ele(a)', prepos)
            prepos = re.sub('^([nv])o-l([oa]s?)\s(\w*?)[\s\.,\)\?!:;]$', r'\2 \3 ' + prep + r' \1ós', prepos)
            prepos = re.sub('^(\w.*?)-([nv])o-l([oa]s?)[\s\.,\)\?!:;]', r'\3 \1 ' + prep + r' \2ós', prepos)
            prepos = re.sub('^(lhe)-l([oa]s?)\s(\w*?)[\s\.,\)\?!:;]$', r'\2 \3 ' + prep + r' eles(as)', prepos)
            prepos = re.sub('^(\w*?)-(lhe)-l([oa]s?)[\s\.,\)\?!:;]', r'\3 \1 ' + prep + r' eles(as)', prepos)
            prepos = re.sub('ar-([oa])', r'á-l\1', prepos)
            prepos = re.sub('er-([oa])', r'ê-l\1', prepos)
            prepos = re.sub('ir-([oa])', r'i-l\1', prepos)
            prepos = re.sub('or-([oa])', r'ô-l\1', prepos)
            prepos = re.sub('m-([oa])', r'm-n\1', prepos)
            prepos = re.sub(' de e', r' de', prepos)
            prepos = re.sub(' em e', r' ne', prepos)
            return prepos
        except:
            return contracao

def pospor(contracao):
    ### Toma uma string contendo verbo auxiliar, principal e contração pronominal
    ### (contracao). Desmembra a contração
    ### em pronome acusativo e dativo.
    ### Exemplo:
    ###     >>> preposicionar("mos havia contado")
    ###     "os havia me contado"
    ### ESTA REGRA DEVE SER APLICADA QUANDO A PALAVRA SEGUINTE AO VERBO PRINCIPAL
    ### TAMBÉM FOR UM VERBO.
    try:
        prepos = re.sub('^(m|t|lh)([oa]s?)\s(\w*?)\s(\w*?)[\s\.,\)\?!:;]$', r'\2 \3 \1e \4', contracao)
        prepos = re.sub('^(\w.*?-)(m|t|lh)([oa]s?)\s(\w*?)[\s\.,\)\?!:;]', r'\1\3 \2e \4', prepos)
        prepos = re.sub('^([nv])o-l([oa]s?)\s(\w*?)\s(\w*?)[\s\.,\)\?!:;]$', r'\2 \3 \1os \4', prepos)
        prepos = re.sub('^(\w.*?-)([nv])o-l([oa]s?)\s(\w*?)[\s\.,\)\?!:;]', r'\1\3 \2os \4', prepos)
        prepos = re.sub('^(lhe)-l([oa]s?)\s(\w*?)\s(\w*?)[\s\.,\)\?!:;]', r'\2 \3 \1s \4', prepos)
        prepos = re.sub('^(\w*?-)(lhe)-l([oa]s?)\s(\w*?)[\s\.,\)\?!:;]', r'\1\3 \2s \4', prepos)
        prepos = re.sub('ar-([oa])', r'á-l\1', prepos)
        prepos = re.sub('er-([oa])', r'ê-l\1', prepos)
        prepos = re.sub('ir-([oa])', r'i-l\1', prepos)
        prepos = re.sub('or-([oa])', r'ô-l\1', prepos)
        prepos = re.sub('m-([oa])', r'm-n\1', prepos)
        prepos = re.sub(' de e', r' de', prepos)
        prepos = re.sub(' em e', r' ne', prepos)
        return prepos
    except:
        return contracao

def remover_cliticos(trecho):
    ### Tira os clíticos de um verbo para ajudar na lematização
    if len(re.findall(r'^[NnVv]o-l[aeo]s?[\s,\.;:\?!\)]', trecho)) > 0:
        return re.findall(r'^[NnVv]o-l[aeo]s?\s(\w*?)[\s,\.;:\?!\)]', trecho)[0]
    else:
        try:
            verbo = re.findall(r'^(\w*?-)\w*?[\s,\.;:\?!\)]', trecho)
            verbo = re.sub(r'ê-$', 'er', verbo[0])
            verbo = re.sub(r'á-$', 'ar', verbo)
            verbo = re.sub(r'[^e]i-$', 'ir', verbo)
            verbo = re.sub(r'ô-$', 'or', verbo)
            verbo = re.sub(r'-$', '', verbo)
            return verbo
        except:
            try:
                return re.findall(r'^\w*?\s(\w*?)[\s,\.;:\?!\)]', trecho)[0]
            except:
                return trecho

def processa_contracao(frase, tagger, unitex):
    ### Toma uma frase, procura contrações e aplica as regras necessárias
    ### para sua simplificação. Retorna pares de original / siplificado em uma
    ### lista de tuplas.
    ### ANTENÇÃO COMPUTEIROS:
    ### É necessário passar um POS-tagger no resultado
    ### da primeira função, e um lematizador no resultado da segunda função.
    contracoes = achar_contracoes(frase, 1)
    original_simplificado = []
    for contracao in contracoes:
        ### INSIRA CÓDIGO PARA VERIFICAR A POS-TAG DA ÚLTIMA PALAVRA DE "contracao"
        aux = contracao.split(' ')
        if len(aux) > 0:
            pos_da_ultima_palavra = str(tagger.tag([aux[len(aux)-1]])[0][1])
        else:
            pos_da_ultima_palavra = "N"

        posposicao = pospor(contracao)
        if contracao != posposicao and pos_da_ultima_palavra == "V":
            original_simplificado.append((contracao, posposicao))
    if len(original_simplificado) == len(contracoes):
        return original_simplificado
    else:
        contracoes = achar_contracoes(frase, 0)
        for contracao in contracoes:
            verbo = remover_cliticos(contracao)
            ### LEMATIZAR O VERBO AQUI!!!
            try:
                lematizado = unitex[verbo]
            except:
                lematizado = verbo
            try:
                preposicao = regencias[lematizado]
            except:
                preposicao = 'para'
            preposicionado = preposicionar(contracao, preposicao)
            original_simplificado.append((contracao, preposicionado))
    return original_simplificado

### REGRA PARA INVERSÃO DA NEGATIVA

def inverter_negacao(frase):
    ### Toma uma frase (string). Retorna pares de negações invertidas
    ### e sua versão simplificada.
    ### Exemplo:
    ### >>> inverter_negacao("Maria o não avisou")
    ### (' o não ', ' não o ')
    pares = []
    originais = re.findall(r'\s[tmlh]h?es?\snão\s', frase)
    originais.extend(re.findall(r'\s[tlhnv]?h?[oa]s?\snão\s', frase))
    originais.extend(re.findall(r'\smos?\snão\s', frase))
    originais.extend(re.findall(r'\sma\snão\s', frase))
    for o in originais:
        pares.append((o, re.sub(r'\s(t|m|lh|n|v)?([oae]s?)\snão\s', r' não \1\2 ', o)))
    return pares

### ÊNCLISES COM O VERBO 'FAZER'

def enclises_raras(frase):
        ### Gera uma lista de tuplas contendo originais e paráfrases
        ### de estruturas enclíticas pouco correntes no português brasileiro
        ### contemporâneo.
        ### Exemplo:
        ### >>> enclises_raras('Fi-la com muita vontade')
        ### [('Fi-la', 'Eu a fiz')]
        enclises = re.findall(r'^(F[êi]-[tlmnv][ao]s?)[\s,\.;:\?!\)]', frase)
        enclises.extend(re.findall(r'\s(f[êi]-[tlmnv][ao]s?)[\s,\.;:\?!\)]', frase))
        original_simplificado = []
        for item in enclises:
                simplificado = re.sub(r'^Fê-([tlmnv][ao]s?)$', r'Ele(a) \1 fez', item)
                simplificado = re.sub(r'^Fi-([tlmnv][ao]s?)$', r'Eu \1 fiz', simplificado)
                simplificado = re.sub(r'^fê-([tlmnv][ao]s?)$', r'\1 fez', simplificado)
                simplificado = re.sub(r'^fi-([tlmnv][ao]s?)$', r'\1 fiz', simplificado)
                simplificado = re.sub(r' l([oa]s?) ', r' \1 ', simplificado)
                simplificado = re.sub(r'^l([oa]s?) ', r' \1 ', simplificado)
                original_simplificado.append((item, simplificado))
        return original_simplificado
