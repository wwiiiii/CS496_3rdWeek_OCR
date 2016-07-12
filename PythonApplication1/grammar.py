#-*- coding: utf-8 -*-

import urllib, requests, sys, types
reload(sys)
sys.setdefaultencoding('utf-8')

def correctGrammar(inputstr):
    #print type(type(inputstr))
    if type(inputstr) == types.UnicodeType:
        query = inputstr
    else :query = unicode(inputstr,'euc-kr')
    query = urllib.quote(query.encode('utf8'))

    url = 'https://m.search.naver.com/p/csearch/dcontent/spellchecker.nhn?q='+query+'&_callback=window.__jindo2_callback._spellingCheck_1'
    r = requests.get(url)
    #print r
    result =  r.text[r.text.find('result"'):]
    result = result[8:-4]; result = result.strip(); result = eval(result)
    tres = (unicode(result['html'],'utf-8'))
    res = ""; i = 0
    while i < (len(tres)):
        if tres[i] == '<':
            while tres[i]!='>': i+=1
            i+=1
        if i>=len(tres): break
        res+=tres[i]; i+=1
    return res#unicode

#ansurl = 'https://m.search.naver.com/p/csearch/dcontent/spellchecker.nhn?q=%EC%9D%B4%20%EB%82%A8%EC%9E%90%20%EB%8F%84%EB%8D%B0%EC%B2%B4%20%EB%AD%90%EC%95%BC%20&_callback=window.__jindo2_callback._spellingCheck_1'
