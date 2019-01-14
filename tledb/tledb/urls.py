"""tledb URL Configuration
"""

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import views as djauth_views
from django.urls import include, path
from rest_framework import routers

from fetcher import views as fetcher_views


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'tle', fetcher_views.TLEViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    url(r'^$', fetcher_views.TLETableView.as_view(), name='index'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^users/', include('users.urls')),
]
