"""
...
"""
# from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from apps.laptops import views
# from apps.laptops.views import principal
# from django.contrib.auth import views as auth_views


app_name="app"

urlpatterns = [
     # path('',views.inicio,name="inicio"),
    # path('user_data/',views.user_data,name="user_data"),
    path('profile/',views.profile,name="profile"),
    path('registro/',views.registro,name="registro"),
    path("app/", include("apps.laptops.urls")),

    # path("accounts/",include("django.contrib.auth.urls"),name="login"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    