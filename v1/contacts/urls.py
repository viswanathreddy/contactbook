from django.conf.urls import url
from .views import ContactView, ContactListViewAPI

urlpatterns = [
    url(r'^$', ContactView.as_view()),
    url(r'^/(?P<pk>\d+)/$', ContactView.as_view(), name='contacts-detail'),
    url(r'^/list$', ContactListViewAPI.as_view(), name="contacts-list"),
]
