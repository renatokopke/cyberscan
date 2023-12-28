# from django.conf.urls import url
from django.urls import re_path

from scan.api.viewset_target import TargetView, ReportViewListView

urlpatterns = [
    # [ Only Admin User ]
    # url(r'^target/$', TargetView.as_view()),
    # url(r'^report/(?P<pk>[0-9]+)/$', ReportViewListView.as_view()),
    re_path(r'^target/$', TargetView.as_view()),
    re_path(r'^report/(?P<pk>[0-9]+)/$', ReportViewListView.as_view()),
]
