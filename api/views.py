from django.shortcuts import render
import requests
import pandas as pd
import json
import random
import pycountry
import os
# Create your views here.

df = pd.read_csv(os.path.join('/home','shahzaib-lfd','OLD_LFD','attempt2','LFD','my work','f1','archive','circuits.csv'))

def indexpage(request):
    kk = [{i:j for i,j in k.items() if i in ['lat','lng','name']} for k in df.to_dict('records')]
    kk = [dict(item, **{'size':1000 * 4e-4,'color':'white'}) for item in kk]
    # for i in kk:
    #     i['text'] = i['name']
    #     i['size'] = 
    #     del i['name']
    
    # d = json.loads(requests.get('https://code.highcharts.com/mapdata/custom/world.geo.json').text)
    # new_list = []
    # new_dict = dict()
    # mappings = df.groupby(['country']).size().sort_values(ascending=False).to_dict()
    # mappings['United Arab Emirates'] = mappings['UAE']
    # del mappings['UAE']
    # # mappings = {'United Arab Emirates':j if i == 'UAE' else i:j for i, j in mappings.items() }
    # # print(mappings)
    # # for i, j in mappings.items():
    # #     for k in pycountry.countries:
    # #         # print(k.name)
    # #         if k.name == i:
    # #             new_dict[k.alpha_2] = j
    # #         else:
    # #             new_dict[k.alpha_2] = 0
    # # print(new_dict)
    # for i, j in mappings.items():
    #     print(i)
    #     country = pycountry.countries.search_fuzzy(i)[0]
    #     new_dict[country.alpha_2] = j
    # print(new_dict)
    # # print({i:j  for i, j in mappings.items()})

    # # print([i for i in pycountry.countries])
    # # for i in pycountry.countries:
    # #     if i.name == 
    # #     print(i.name)
    # # print({i:j  for i, j in mappings.items()})

    # # for i, k in enumerate(d['features']):
    # #     if k['properties']['name'] in mappings.keys():
    # #         new_dict = k
    # #         new_dict['properties']['circuit_number'] = mappings[k['properties']['name']]
    # #         new_list.append(new_dict)
    # # d['features'] = new_list
    # # print(d)
    # # new_list
    context = {'data22':kk}
    # context={'a':'JING ALAL HO HO','data22': d}
    
    return render(request, 'index2.html', context)
