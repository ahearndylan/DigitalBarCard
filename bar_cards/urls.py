from django.urls import path
from . import views

urlpatterns = [
    path('view/', views.view_bar_card, name='view_bar_card'),
    path('generate_qr_code/', views.generate_qr_code, name='generate_qr_code'),
    path('view/<str:bbo_number>/', views.view_bar_card, name='view_bar_card'),
    path('display/<str:bbo_number>/', views.bar_card_display, name='bar_card_display'),

]