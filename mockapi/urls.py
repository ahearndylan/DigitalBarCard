from django.urls import path
from . import views

urlpatterns = [
    path('verify_bbo/<str:bbo_number>/', views.verify_lawyer_by_bbo, name='verify_lawyer_by_bbo'),
    path('verify_name/<str:first_name>/<str:last_name>/', views.verify_lawyer_by_name, name='verify_lawyer_by_name'),
]