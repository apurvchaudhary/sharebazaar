import datetime

from sharebazaar_app.models import Stock
from sharebazaar_app.serializers import ExitedStockSerializer, NonExitedStockSerializer


def get_home_page_data():
    exited_shares = Stock.objects.filter(sell_price__isnull=False).order_by("-buy_date")
    non_exited_shares = Stock.objects.filter(sell_price__isnull=True).order_by("-buy_date")
    exited_share_serializer = ExitedStockSerializer(exited_shares, many=True)
    non_exited_share_serializer = NonExitedStockSerializer(non_exited_shares, many=True)
    data = {"exited_share" : exited_share_serializer.data,
            "non_exited_share" : non_exited_share_serializer.data,
            "date" : datetime.datetime.today().strftime("%-d %b %Y")}
    return data


def get_investment_returns_data(serialized_exited_stocks):
    money_invested, money_returns, profit, loss, net_pl,indicate = 0, 0, 0, 0, 0, 0
    for stock in serialized_exited_stocks:
        stock_buy_price, stock_sell_price, stock_units = float(stock["buy_price"]), float(stock["sell_price"]),\
                                                         stock["units"]
        money_invested += stock_buy_price * stock_units
        money_returns += stock_sell_price * stock_units
        if stock_buy_price > stock_sell_price:
            loss += (stock_buy_price - stock_sell_price) * stock_units
        elif stock_buy_price < stock_sell_price:
            profit += (stock_sell_price - stock_buy_price) * stock_units
    if profit > loss:
        net_pl += profit - loss
        indicate = 1
    elif profit < loss:
        net_pl += loss - profit
        indicate = 2
    investment_returns_data = {"total_sold_investment": money_invested,"total_sold_returns": money_returns,
                               "total_profit": round(profit, 2), "total_loss": round(loss, 2),
                               "net_pl": round(net_pl, 2), "indicate": indicate,
                               "date" : datetime.date.today().strftime("%-d %b %Y")}
    return investment_returns_data


def get_today_page_data():
    exited_shares = Stock.objects.filter(sell_date=datetime.date.today()).order_by("-buy_date")
    non_exited_share = Stock.objects.filter(sell_date__isnull=True,
                                            buy_date=datetime.date.today()).order_by("-buy_date")
    exited_shares_serializer = ExitedStockSerializer(exited_shares, many=True)
    exited_shares_serializer_data = exited_shares_serializer.data
    non_exited_share_serializer = NonExitedStockSerializer(non_exited_share, many=True)
    investment_returns_data = get_investment_returns_data(exited_shares_serializer.data)
    data = {"exited_share": exited_shares_serializer_data,
            "non_exited_share": non_exited_share_serializer.data,
            **investment_returns_data}
    return data


def get_current_month_page_data():
    exited_shares = Stock.objects.filter(sell_date__month=datetime.date.today().month).order_by("-buy_date")
    non_exited_share = Stock.objects.filter(sell_date__isnull=True,
                                            buy_date__month=datetime.date.today().month).order_by("-buy_date")
    exited_shares_serializer = ExitedStockSerializer(exited_shares, many=True)
    exited_shares_serializer_data = exited_shares_serializer.data
    non_exited_share_serializer = NonExitedStockSerializer(non_exited_share, many=True)
    investment_returns_data = get_investment_returns_data(exited_shares_serializer.data)
    data = {"exited_share": exited_shares_serializer_data,
            "non_exited_share": non_exited_share_serializer.data,
            "current_month" : datetime.datetime.today().strftime("%b %Y"),
            **investment_returns_data}
    return data


def get_net_worth_page_data():
    exited_shares = Stock.objects.filter(sell_date__isnull=False)
    non_exited_share = Stock.objects.filter(sell_date__isnull=True, created_at__month=datetime.date.today().month)
    exited_shares_serializer = ExitedStockSerializer(exited_shares, many=True)
    non_exited_share_serializer = NonExitedStockSerializer(non_exited_share, many=True)
    exited_shares_serializer_data = exited_shares_serializer.data
    non_exited_share_serializer_data = non_exited_share_serializer.data
    investment_returns_data = get_investment_returns_data(exited_shares_serializer_data)
    total_investment_till_date = 0
    total_share_bought = 0
    total_share_sold = 0
    total_share_holding = 0
    total_investment_in_holding = 0
    for stock in exited_shares_serializer_data:
        total_share_bought += stock["units"]
        total_share_sold += stock["units"]
    for stock in non_exited_share_serializer_data:
        total_share_bought += stock["units"]
        total_share_holding += stock["units"]
        invested = float(stock["buy_price"]) * stock["units"]
        total_investment_in_holding += invested
        total_investment_till_date += invested
    total_investment_till_date += investment_returns_data["total_sold_investment"]
    data = {
        "total_share_bought" : total_share_bought,
        "total_share_sold" : total_share_sold,
        "total_share_holding" : total_share_holding,
        "total_investment_in_holding" : total_investment_in_holding,
        "total_investment_till_date" : total_investment_till_date,
        **investment_returns_data}
    return data


def get_requested_month_data(month_and_year_str):
    month_year = month_and_year_str.split("-")
    month, year = int(month_year[1]), int(month_year[0])
    exited_shares = Stock.objects.filter(sell_date__month=month, sell_date__year=year).order_by("-buy_date")
    non_exited_share = Stock.objects.filter(sell_date__isnull=True, buy_date__month=month,
                                            buy_date__year=year).order_by("-buy_date")
    exited_shares_serializer = ExitedStockSerializer(exited_shares, many=True)
    exited_shares_serializer_data = exited_shares_serializer.data
    non_exited_share_serializer = NonExitedStockSerializer(non_exited_share, many=True)
    investment_returns_data = get_investment_returns_data(exited_shares_serializer.data)
    data = {"exited_share": exited_shares_serializer_data,
            "non_exited_share": non_exited_share_serializer.data,
            "particular" : month_and_year_str,
            "type" : "Month",
            **investment_returns_data}
    return data


def get_requested_date_data(date):
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    if date_obj > datetime.date.today():
        return
    exited_shares = Stock.objects.filter(sell_date=date_obj).order_by("-buy_date")
    non_exited_share = Stock.objects.filter(sell_date__isnull=True, buy_date=date_obj).order_by("-buy_date")
    exited_shares_serializer = ExitedStockSerializer(exited_shares, many=True)
    exited_shares_serializer_data = exited_shares_serializer.data
    non_exited_share_serializer = NonExitedStockSerializer(non_exited_share, many=True)
    investment_returns_data = get_investment_returns_data(exited_shares_serializer.data)
    data = {"exited_share": exited_shares_serializer_data,
            "non_exited_share": non_exited_share_serializer.data,
            "particular": date,
            "type": "Date",
            **investment_returns_data}
    return data


def sort_by_entity(serialized_data, entity, type):
    if entity == "profit":
        if type == "lh":
            return sorted(serialized_data, key = lambda i: i['profit'])
        elif type == "hl":
            return sorted(serialized_data, key = lambda i: i['profit'], reverse=True)
    elif entity == "loss":
        if type == "lh":
            return sorted(serialized_data, key = lambda i: i['loss'])
        elif type == "hl":
            return sorted(serialized_data, key = lambda i: i['loss'], reverse=True)
    elif entity == "units":
        if type == "lh":
            return sorted(serialized_data, key = lambda i: i['units'])
        elif type == "hl":
            return sorted(serialized_data, key = lambda i: i['units'], reverse=True)


def get_sorting_data(entity, type):
    if entity == "profit":
        if type == "hightolow" or type == "lowtohigh":
            exited_shares = Stock.objects.filter(sell_date__isnull=False)
            exited_shares_serializer = ExitedStockSerializer(exited_shares, many=True)
            if type == "lowtohigh":
                exited_shares_serializer_data = sort_by_entity(exited_shares_serializer.data, "profit", "lh")
                return {"exited_share": exited_shares_serializer_data}
            elif type == "hightolow":
                exited_shares_serializer_data = sort_by_entity(exited_shares_serializer.data, "profit", "hl")
                return {"exited_share": exited_shares_serializer_data}
            return None
        return None
    elif entity == "loss":
        if type == "hightolow" or type == "lowtohigh":
            exited_shares = Stock.objects.filter(sell_date__isnull=False)
            exited_shares_serializer = ExitedStockSerializer(exited_shares, many=True)
            if type == "lowtohigh":
                exited_shares_serializer_data = sort_by_entity(exited_shares_serializer.data, "loss" ,"lh")
                return {"exited_share": exited_shares_serializer_data}
            elif type == "hightolow":
                exited_shares_serializer_data = sort_by_entity(exited_shares_serializer.data, "loss", "hl")
                return {"exited_share": exited_shares_serializer_data}
            return None
        return None
    elif entity == "units":
        if type == "hightolow" or type == "lowtohigh":
            exited_shares = Stock.objects.filter(sell_date__isnull=False)
            exited_shares_serializer = ExitedStockSerializer(exited_shares, many=True)
            non_exited_share = Stock.objects.filter(sell_date__isnull=True)
            non_exited_share_serializer = NonExitedStockSerializer(non_exited_share, many=True)
            if type == "lowtohigh":
                return {"exited_share": sort_by_entity(exited_shares_serializer.data, "units" ,"lh"),
                        "non_exited_share": sort_by_entity(non_exited_share_serializer.data, "units", "lh")}
            elif type == "hightolow":
                return {"exited_share": sort_by_entity(exited_shares_serializer.data, "units", "hl"),
                        "non_exited_share": sort_by_entity(non_exited_share_serializer.data, "units", "hl")}
    return None
