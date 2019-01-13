"""tledb URL Configuration
"""

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import include, path
from rest_framework import routers

from fetcher import views

from django.contrib.auth import views as djauth_views
from django.urls import path


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'tle', views.TLEViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    url(r'^$', views.TLEListView.as_view(), name='index'),
    url(r'^accounts/', include('django_registration.backends.activation.urls')),
    # url(r'^accounts/', include('django.contrib.auth.urls')),
    path(
        'accounts/login/',
        djauth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login'
    ),
    path('logout/', djauth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', djauth_views.PasswordChangeView.as_view(), name='password_change'),
    path(
        'password_change/done/',
        djauth_views.PasswordChangeDoneView.as_view(), name='password_change_done'
    ),
    path('password_reset/', djauth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', djauth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', djauth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', djauth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
]
