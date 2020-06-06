from django.urls import re_path
from sharebazaar_app.views import HomePageView, DayPageView, MonthPageView, NetWorthPageView


urlpatterns = [
    re_path(r'^home/$', HomePageView.as_view(), name="home"),
    re_path(r'^day/$', DayPageView.as_view(), name="day"),
    re_path(r'^month/$', MonthPageView.as_view(), name="month"),
    re_path(r'^networth/$', NetWorthPageView.as_view(), name="networth"),
]