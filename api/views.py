from django.shortcuts import render
import requests
import pandas as pd
import json
import random
import pycountry
import os
from django.conf import settings

df = pd.read_csv(os.path.join(settings.MEDIA_ROOT,'csv','circuits.csv'))

def indexpage(request):
    locations = [{i:j for i,j in k.items() if i in ['lat','lng','name']} for k in df.to_dict('records')]
    locations = [dict(item, **{'size':1000 * 4e-4,'color':'white'}) for item in locations]
    context = {'data22':locations}
    
    return render(request, 'index2.html', context)
