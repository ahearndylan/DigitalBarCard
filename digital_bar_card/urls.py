from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views

urlpatterns = [

   path('admin/', admin.site.urls),
   path('', user_views.home, name='home'),
   path('register/', user_views.register, name='register'),
   path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
   path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
   path('bar-cards/', include('bar_cards.urls')),
   path('verification/', include('verification.urls')),
]
