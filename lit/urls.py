from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^homepage/$', 'lit.home.views.homepage', name='homepage'),
    url(r'^logout/$', 'lit.home.views.logout', name='logout'),
    url(r'^corepage/$', 'lit.home.views.corepage', name='corepage'),
    url(r'^litsoc/$', 'lit.home.views.litsoc', name='litsoc'),
    url(r'^newevent/(?P<foobar>.+)$', 'lit.home.views.newevent', name='newevent'),
    url(r'^editevent/(?P<foobar>.+)/$','lit.home.views.editevent',name='editevent'),
    url(r'^events/(?P<foobar>.+)/$','lit.home.views.events',name='events'),
    url(r'^eventdetails/$', 'lit.home.views.eventdetails', name='eventdetails'),
    url(r'^pointstally/$', 'lit.home.views.pointstally', name='pointstally'),
    url(r'^results/(?P<foobar>.+)/$','lit.home.views.results',name='results'),
    url(r'^login/$', 'lit.home.views.login', name='login'),
    url(r'^changepw/$', 'lit.home.views.changepw', name='changepw'),
    url(r'^changepw2/$', 'lit.home.views.changepw2', name='changepw2'),
    url(r'^coordregister/(?P<foobar>.+)/$','lit.home.views.register',name='register'),
    url(r'^verticals/(?P<foobar>.+)/$','lit.home.views.verticals',name='verticals'),
    url(r'^editvertical/(?P<foobar>.+)/$','lit.home.views.editvertical',name='editvertical'),
    url(r'^approve/(?P<foobar>.+)/$','lit.home.views.approve',name='approve'),
    url(r'^gallery/$', 'lit.home.views.gallery', name='gallery'),
    url(r'^upload/(?P<foobar>.+)/$','lit.home.views.upload',name='upload'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    url(r'^downloads/$', 'lit.home.views.downloads', name='downloads'),
    url(r'^hostel/(?P<foobar>.+)/$','lit.home.views.hostel',name='hostel'),
    url(r'^hostels/$', 'lit.home.views.hostels', name='hostels'),
    url(r'^calender/$', 'lit.home.views.calender', name='calender'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
