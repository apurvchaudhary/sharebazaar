from django.shortcuts import render
from rest_framework.views import APIView
from django.core.cache import cache

from rest_framework.permissions import IsAdminUser
from sharebazaar_app.utils import get_home_page_data, get_today_page_data,\
    get_current_month_page_data, get_net_worth_page_data, get_requested_month_data, get_requested_date_data


class HomePageView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        if "stock_home" in cache:
            return render(request, template_name="home.html", context={"data": cache.get("stock_home")})
        data = get_home_page_data()
        cache.set("stock_home", data)
        return render(request, template_name="home.html", context={"data": data})


class DayPageView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        if "stock_today" in cache:
            return render(request, template_name="day.html", context={"data": cache.get("stock_today")})
        data = get_today_page_data()
        cache.set("stock_today", data)
        return render(request, template_name="day.html", context={"data": data})


class MonthPageView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        if "stock_current_month" in cache:
            return render(request, template_name="month.html", context={"data": cache.get("stock_current_month")})
        data = get_current_month_page_data()
        cache.set("stock_current_month", data)
        return render(request, template_name="month.html", context={"data": data})


class NetWorthPageView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        if "net_worth" in cache:
            return render(request, template_name="networth.html", context={"data": cache.get("net_worth")})
        data = get_net_worth_page_data()
        cache.set("net_worth", data)
        return render(request, template_name="networth.html", context={"data": data})


class FilterPageView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        month_and_year = request.query_params.get("month")
        date = request.query_params.get("date")
        if month_and_year:
            data = get_requested_month_data(month_and_year)
            return render(request, template_name="filters.html", context={"data": data})
        elif date:
            data = get_requested_date_data(date)
            return render(request, template_name="filters.html", context={"data": data})
        return render(request, template_name="filters.html")