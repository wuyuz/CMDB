from django.conf.urls import url
from api import views


urlpatterns = [
    url(r'^asset/',views.Asset.as_view() ),
    # url(r'^test/',views.Test.as_view() ),
]
