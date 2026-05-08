from django.urls import path
from . import views

urlpatterns = [
    path('', views.shorten_url, name='shorten-url'),
    path('check_analytics', views.analytics, name='click-analytics'),
    path('go/<str:pk>', views.go_to_link, name='go_to_link'),
    path('delete_link/<id>', views.delete_link, name='delete-link'),
    path('graph/<str:pk>', views.generate_graph, name='graph'),
    
]
