from django.core.cache import cache
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from sharebazaar.settings import CORONA_URL
from sharebazaar_app.utils import get_home_page_data, get_today_page_data, \
    get_current_month_page_data, get_net_worth_page_data, get_sorting_data, get_requested_date_data, \
    get_requested_month_data


def response(data, code=status.HTTP_200_OK):
    return Response(data=data, status=code)


def get_user_details(request):
    return request.user.get_username().upper()


@api_view()
@cache_page(60 * 60 * 720)
def get_global_home_page(request):
    return render(request, template_name="global.html", context={"corona_url" : CORONA_URL})


class HomePageView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        if "stock_home" in cache:
            return render(request, template_name="home.html", context={"data": cache.get("stock_home"),
                                                                       "username": get_user_details(request)})
        data = get_home_page_data()
        cache.set("stock_home", data)
        return render(request, template_name="home.html", context={"data": data, "username": get_user_details(request)})


class DayPageView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        if "stock_today" in cache:
            return render(request, template_name="day.html", context={"data": cache.get("stock_today"),
                                                                      "username": get_user_details(request)})
        data = get_today_page_data()
        cache.set("stock_today", data)
        return render(request, template_name="day.html", context={"data": data, "username": get_user_details(request)})


class MonthPageView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        if "stock_current_month" in cache:
            return render(request, template_name="month.html", context={"data": cache.get("stock_current_month"),
                                                                        "username": get_user_details(request)})
        data = get_current_month_page_data()
        cache.set("stock_current_month", data)
        return render(request, template_name="month.html",
                      context={"data": data, "username": get_user_details(request)})


class NetWorthPageView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        if "net_worth" in cache:
            return render(request, template_name="networth.html", context={"data": cache.get("net_worth"),
                                                                           "username": get_user_details(request)})
        data = get_net_worth_page_data()
        cache.set("net_worth", data)
        return render(request, template_name="networth.html",
                      context={"data": data, "username": get_user_details(request)})


class FilterPageView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        month_and_year = request.query_params.get("month")
        date = request.query_params.get("date")
        if month_and_year:
            data = get_requested_month_data(month_and_year)
            return render(request, template_name="filters.html", context={"data": data,
                                                                          "username": get_user_details(request)})
        elif date:
            data = get_requested_date_data(date)
            return render(request, template_name="filters.html", context={"data": data,
                                                                          "username": get_user_details(request)})
        return render(request, template_name="filters.html", context={"username": get_user_details(request)})


class SortingPageView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        entity = request.query_params.get("entity")
        type = request.query_params.get("type")
        if entity and type:
            data = get_sorting_data(entity, type)
            return render(request, template_name="sortings.html", context={"data": data,
                                                                           "username": get_user_details(request)})
        return render(request, template_name="sortings.html", context={"username": get_user_details(request)})
