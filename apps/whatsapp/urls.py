from django.conf.urls import url
from django.urls import path
from . import views
from apps.whatsapp.views import *
from django.contrib.auth.decorators import login_required

app_name = 'Mensaje'

urlpatterns = [
    path('nuevo', login_required(CrudView.as_view()), name='nuevo'),
]
