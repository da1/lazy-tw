from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('tw.views',
    # Examples:
    # url(r'^$', 'lazy.views.home', name='home'),
    # url(r'^lazy/', include('lazy.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'index', name='index'),
    # Twitter OAuth Authenticate
    url(r'^login$', 'login', name='login'),
    # Callback
    url(r'^get_callback', 'get_callback', name='get_callback'),
    # Tweet
    url(r'^post$', 'post', name='post'),
    # Tweet delete
    url(r'^delete/(?P<id>\d+)/$', 'delete', name='delete'),
    # Friends timeline
    url(r'^friends/(?P<username>\w+)/$', 'friends', name='friends'),
    # logout
    url(r'^logout$', 'logout', name='logout'),
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain"))
)
