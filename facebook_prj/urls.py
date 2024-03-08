"""facebook_prj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from core.routing import websocket_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),

    # Routing
    path("user/", include("userauths.urls")),
    path("", include("core.urls")),

    # Web Socket
    path('ws/', include(websocket_urlpatterns)),

    # Change Password
    path('user/change-password/',auth_views.PasswordChangeView.as_view(template_name='userauths/password-reset/change-password.html',success_url = '/user/password-reset-complete/'),name='change_password'),
    path('user/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='userauths/password-reset/password_reset_complete.html'), name='password_reset_complete'),

    

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

