#-*- coding: UTF-8 -*-

from snownlp import SnowNLP
from snownlp import seg
from tld import get_tld
import simplejson as json
import re

def inChinese(c):
    zhPattern = re.compile(u"[\u4e00-\u9fa5]+")
    try:
        return zhPattern.search(c) is not None
    except Exception as e:
        return None

allWords={}
allSents={}
world = json.load(open('deep_moe_lt4.json'))
world.extend(json.load(open('deep_moe_gte4_alt.json')))
world.extend(json.load(open('deep_io_me_cc_im.json')))
world.extend(json.load(open('deep_alt.json')))

sum = len(world)
count = 0
for e in world:
    count+=1
    print(str(count) + ' / ' + str(sum))
    if(e.get('text') is not None and len(e.get('text').replace(" ",""))>0):
        s = SnowNLP(e['text'])
        for w in s.words:
            if inChinese(w):
                if allWords.get(w) is None:
                    print(w + ' is listed as new word')
                    allWords[w] = 1
                else:
                    allWords[w] +=1
                    print(w + ' is presented for '+str(allWords[w])+' times' )

        domain = get_tld(e['link'])
        if allSents.get(domain) is None:
            allSents[domain] = [s.sentiments]
            print(domain + ' has 1st sentiment ' + str(s.sentiments))

        else:
            allSents[domain].append(s.sentiments)
            print(domain + ' has new sentiment ' + str(s.sentiments))


with open('resWords.json', 'w') as file:
    file.write(json.dumps(allWords))
with open('resSents.json', 'w') as file:
    file.write(json.dumps(allSents))
