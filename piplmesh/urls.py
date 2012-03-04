from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from piplmesh.frontend import views as frontend_views

urlpatterns = patterns('',
    url('^$', frontend_views.HomeView.as_view(), name='home'),
    
    (r'^accounts/convert/', include('lazysignup.urls')),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'redirect_field_name': 'redirect_to',}, name='logout'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'redirect_field_name': 'redirect_to', 'template_name': 'login.html',}, name='login'),
    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
