
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.show_crypto, name='show_crypto'),
    path('addcrypto/', views.new_crypto, name='new_crypto'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('graph/', views.graph, name='graph')
]
