
from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path(
        'profile/view',
        TemplateView.as_view(template_name='user_profile_view.html'),
        name='user_profile_view'
    ),
    path(
        'profile/update',
        views.update_profile,
        name='user_profile_update'
    ),
]
