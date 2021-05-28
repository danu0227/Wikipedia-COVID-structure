from collections import defaultdict
import json
import urllib
import urllib.request
import pandas as pd
import re
from threading import Thread
from multiprocessing import Process
import datetime

def api_work(title_list, lang, id):
    print('%s, %s start:'%(lang, id), datetime.datetime.now())
    i = 0
    tq_dict = {}
    try:
        in_f = open('./kcc2021/t2q_%s_%d.json' % (lang, id), 'r')
        tq_dict = json.load(json_file)
        inf.close()
    except:
        out_f = open('./kcc2021/t2q_%s_%d.json' % (lang, id), 'w')
    er = 0
    already = list(tq_dict.keys())
    for i in title_list:
        if i in already:
            continue
        try:
            t = urllib.parse.quote(i)
            url = 'https://%s.wikipedia.org/w/api.php?action=query&prop=pageprops&ppprop=wikibase_item&redirects=1&format=json&titles=%s' % (lang, t)
            a = urllib.request.urlopen(url)
            j = json.loads(a.read())
            j2 = j['query']['pages']
            qid = list(j2.values())[0]['pageprops']['wikibase_item']
            try:
                j3 = j['query']['redirects'][0]['to']
                tq_dict[j3] = qid
            except:
                pass
        except:
##            print(j)
##            print(url)
            qid = None
            er += 1
        tq_dict[i] = qid
        already.append(i)
    out_f.write(json.dumps(tq_dict, ensure_ascii=False))
    out_f.close()
    print('%s, %s end: %d/%d'%(lang, id, er, len(title_list)), datetime.datetime.now())
    


def split_process():
    langs = ['pt','ko','ja','en','es','fr','de','ar','it','zh','ru']
    langs = ['it']
#     langs = ['pt', 'ko', 'ja']
#     langs = ['ja','en','es','fr','de','ar','it','zh','ru']
    for lang in langs:
        titles = set()
#         for temp in ['m', 's', 'f']:
        for temp in ['m']:
            json_file = open('kcc2021/%s_%s.json' % (lang, temp), 'r')
            adjacency_dict = json.load(json_file)
            curr_titles = set(adjacency_dict.keys())
            curr_titles.update({y for x in list(adjacency_dict.values()) for y in x})
            titles = titles.union(curr_titles)
#             csv_file = open('kcc2021/title_net_list_%s.csv' % lang, 'r')
#             titles = [i.strip() for i in csv_file.readlines()]
#             titles = set(titles)
        print(lang, len(titles))
        titles = list(titles)
        procs_n = 16
        len_part = len(titles)//procs_n
        loads = []
        for i in range(procs_n):
            loads.append(titles[i*len_part:(i+1)*len_part])
        loads.append(titles[procs_n*len_part-len_part:])

        procs = [Process(target=api_work,
                         args = (loads[i], lang, i)) for i in range(len(loads))]
        for i in range(len(loads)):
            if i == 11:
                procs[i].start()
        for i in range(len(loads)):
            if i == 11:
                procs[i].join()
        
        

split_process()               
                 
                
        
