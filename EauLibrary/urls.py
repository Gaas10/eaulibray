
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView,LogoutView
from library import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls')),


    #path('accounts/',include('django.contrib.auth.urls') ),
    #path('login', LoginView.as_view(template_name='library/gal.html')),
    #path('logout', LogoutView.as_view(template_name='library/gal.html')),
    #path('afterlogin', views.afterlogin_view)
]
