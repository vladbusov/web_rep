from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^$', views.main , name='main'),
    url(r'^hot/', views.questions_hot , name='hot'),
    url(r'^new/', views.questions_new, name='new'),
    url(r'^ask/', views.ask_quest , name='ask'),
    url(r'^profile/edit/', views.settings , name='settings'),
    url(r'^signup/', views.registration , name='signup'),
    url(r'^login/', views.make_login , name='login'),
    url(r'^question/(\d+)/$', views.question, name = 'questions'),
    url(r'^tag/(\w+)/', views.questions_tag, name = 'tag'),
    url(r'^logout/', views.logout, name = 'logout'),
    url(r'app/like/', views.app_like, name='change_view'),
]