from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^$', views.main , name='main'),
    url(r'^hot/', views.questions_hot , name='hot'),
    url(r'^new/', views.questions_new, name='new'),
    url(r'^ask/', views.ask , name='ask'),
    url(r'^settings/', views.settings , name='settings'),
    url(r'^signup/', views.signup , name='signup'),
    url(r'^login/', views.login , name='login'),
    url(r'^question/(\d+)/$', views.question, name = 'questions'),
    url(r'^tag/(\w+)/', views.questions_tag, name = 'tag'),
]