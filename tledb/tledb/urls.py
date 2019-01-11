"""tledb URL Configuration
"""

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import include, path
from rest_framework import routers

from fetcher import views


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'tle', views.TLEViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    url(r'^$', views.TLEListView.as_view(), name='tle-list'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
]
