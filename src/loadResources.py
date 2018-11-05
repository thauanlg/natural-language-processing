import nltk, json

tagger = nltk.tag.sequential.UnigramTagger.decode_json_obj(json.load(open('../dados/json/tagger.json', 'r')))
unitex = json.load(open('../dados/json/unitex.json','r'))
brasileiro = json.load(open('../dados/json/br-lematizado.json','r'))
sinonimos = json.load(open('../dados/json/tep.json','r'))
dic= json.load(open('../dados/json/dic.json','r'))
