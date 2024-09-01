from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_bar_card, name='generate_bar_card'),
    path('view/', views.view_bar_card, name='view_bar_card'),
]