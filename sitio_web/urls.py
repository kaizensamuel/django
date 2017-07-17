# demonstration/urls.py

from django.views.generic.base import TemplateView

from registration.backends.default.views import ActivationView
from registration.backends.default.views import RegistrationView

from django.conf.urls import include, url
from django.contrib import admin

#https://github.com/macdhuibh/django-registration-templates
urlpatterns = [
  url(r'^restaurantes/', include('restaurantes.urls')),
  url(r'^admin/', include(admin.site.urls)),
  url(r'^accounts/', include('registration.backends.simple.urls')),
  url(r'^activate/complete/$',
	TemplateView.as_view(template_name='registration/activation_complete.html'),
	name='registration_activation_complete'),
  url(r'^activate/(?P<activation_key>\w+)/$',
  	ActivationView.as_view(),
	name='registration_activate'),
  url(r'^register/$',
	RegistrationView.as_view(),
	name='registration_register'),
  url(r'^register/complete/$',
	TemplateView.as_view(template_name='registration/registration_complete.html'),
	name='registration_complete'),
  url(r'^register/closed/$',
	TemplateView.as_view(template_name='registration/registration_closed.html'),
	name='registration_disallowed'),
                       
]
