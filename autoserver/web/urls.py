from django.conf.urls import url
from web import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),

    # 主机
    url(r'^server_list/$', views.server_list, name='server_list'),
    url(r'^server_add/$', views.server_change, name='server_add'),
    url(r'^server_edit/(\d+)/$', views.server_change, name='server_edit'),
    url(r'^server_detail/(\d+)/$', views.server_detail, name='server_detail'),
    url(r'^server_record/(\d+)/$', views.server_record, name='server_record'),
]
