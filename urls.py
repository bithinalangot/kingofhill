from django.conf.urls.defaults import *
from inctf.kingofhill import views

urlpatterns = patterns('',
        #   (r'^/$', views.kinghome),
    (r'^/scoreboard/$', views.scoreboard),
    #    (r'^/submitflag/$', views.submit_flag),    
)



