from django.shortcuts import render
from django.conf import settings
from api.models import Circuits

def indexpage(request):
    # locations = [{i:j for i,j in k.items() if i in ['lat','lng','name']} for k in df.to_dict('records')]
    locations = Circuits.objects.all().values('lat','lng','name')
    locations = [dict(item, **{'size':1000 * 4e-4,'color':'white'}) for item in locations]
    context = {'data22':locations}
    
    return render(request, 'index.html', context)
