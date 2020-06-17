from django.urls import re_path

from sharebazaar_app.views import HomePageView, DayPageView, MonthPageView, NetWorthPageView, \
    FilterPageView, SortingPageView, get_global_home_page

urlpatterns = [
    re_path(r'^home/$', HomePageView.as_view(), name="home"),
    re_path(r'^day/$', DayPageView.as_view(), name="day"),
    re_path(r'^month/$', MonthPageView.as_view(), name="month"),
    re_path(r'^networth/$', NetWorthPageView.as_view(), name="networth"),
    re_path(r'^filters/$', FilterPageView.as_view(), name="filters"),
    re_path(r'^sortings/$', SortingPageView.as_view(), name="sortings"),
    re_path(r'', get_global_home_page, name="global-home"),
]
