from django.conf.urls import url
from api_v1 import views

urlpatterns = [
    url(r'^$', views.UserList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]
