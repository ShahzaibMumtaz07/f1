from django.conf.urls import url, include
from django.urls import path
from django.conf.urls import url
from api import views
app_name = "api"

urlpatterns = [
    # url('^$',views.indexpage, name = 'index')
    path('world/', views.indexpage, name = 'index'),
]
