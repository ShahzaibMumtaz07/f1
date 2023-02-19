from django.shortcuts import render
from django.conf import settings


def indexpage(request):
    # locations = [{i:j for i,j in k.items() if i in ['lat','lng','name']} for k in df.to_dict('records')]
    # locations = [dict(item, **{'size':1000 * 4e-4,'color':'white'}) for item in locations]
    context = {'data22':None}
    
    return render(request, 'index2.html', context)
