from django.shortcuts import render
from django.conf import settings
from api.models import Circuits

def indexpage(request):
    circuits = Circuits.objects.all().values('lat','lng','name')
    circuits = [dict(item, **{'size':1000 * 4e-4,'color':'white'}) for item in circuits]
    context = {'circuits':circuits}
    
    return render(request, 'index.html', context)
