import datetime

from sharebazaar_app.models import Stock
from sharebazaar_app.serializers import ExitedStockSerializer, NonExitedStockSerializer


def get_home_page_data():
    exited_shares = Stock.objects.filter(sell_price__isnull=False).order_by("-created_at")
    non_exited_shares = Stock.objects.filter(sell_price__isnull=True).order_by("-created_at")
    exited_share_serializer = ExitedStockSerializer(exited_shares, many=True)
    non_exited_share_serializer = NonExitedStockSerializer(non_exited_shares, many=True)
    data = {"exited_share" : exited_share_serializer.data, "non_exited_share" : non_exited_share_serializer.data}
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
                               "date" : datetime.date.today().strftime("%-d %b %y")}
    return investment_returns_data


def get_today_page_data():
    exited_shares = Stock.objects.filter(sell_date=datetime.date.today()).order_by("-created_at")
    non_exited_share = Stock.objects.filter(sell_date__isnull=True,
                                            created_at__date=datetime.date.today()).order_by("-created_at")
    exited_shares_serializer = ExitedStockSerializer(exited_shares, many=True)
    exited_shares_serializer_data = exited_shares_serializer.data
    non_exited_share_serializer = NonExitedStockSerializer(non_exited_share, many=True)
    investment_returns_data = get_investment_returns_data(exited_shares_serializer.data)
    data = {"exited_share": exited_shares_serializer_data,
            "non_exited_share": non_exited_share_serializer.data,
            **investment_returns_data}
    return data


def get_current_month_page_data():
    exited_shares = Stock.objects.filter(sell_date__month=datetime.date.today().month).order_by("-created_at")
    non_exited_share = Stock.objects.filter(sell_date__isnull=True,
                                            created_at__month=datetime.date.today().month).order_by("-created_at")
    exited_shares_serializer = ExitedStockSerializer(exited_shares, many=True)
    exited_shares_serializer_data = exited_shares_serializer.data
    non_exited_share_serializer = NonExitedStockSerializer(non_exited_share, many=True)
    investment_returns_data = get_investment_returns_data(exited_shares_serializer.data)
    data = {"exited_share": exited_shares_serializer_data,
            "non_exited_share": non_exited_share_serializer.data,
            **investment_returns_data}
    return data


def get_net_worth_page_data():
    exited_shares = Stock.objects.filter(sell_date__isnull=False).order_by("-created_at")
    non_exited_share = Stock.objects.filter(sell_date__isnull=True,
                                            created_at__month=datetime.date.today().month).order_by("-created_at")
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
