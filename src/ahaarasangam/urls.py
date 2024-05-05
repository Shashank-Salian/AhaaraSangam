"""
URL configuration for ahaarasangam project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.urls import path

from . import views
from donor import views as donor_views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', donor_views.login_view, name="login"),
    path('signup/', donor_views.signup_view, name="signup"),
    path('logout/', donor_views.logout_view, name="logout"),
    path('donate/', donor_views.donate_view, name="donate"),
    path('donorprofile/', donor_views.donor_profile_view, name="donor_profile"),
    path('updateprofile/', donor_views.update_donor_profile, name="update_profile"),
    path('api/cities/<str:state_iso2>/',
         donor_views.get_cities_api, name='get_cities'),
    path('appassets/img/donation/<int:donation_id>/',
         donor_views.app_assets_image, name="app_assets_image"),
    path('admin/', admin.site.urls),
]

# python manage.py collectstatic
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
