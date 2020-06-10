from rest_framework import serializers
from sharebazaar_app.models import Stock


class NonExitedStockSerializer(serializers.ModelSerializer):
    """
        Serializer to serialize stock all fields
        """
    buy_date = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = ("id", "name", "buy_date","buy_price", "units")

    def get_buy_date(self, obj):
        return obj.buy_date.strftime("%-d %b %y")


class ExitedStockSerializer(serializers.ModelSerializer):
    """
    Serializer to serialize stock all fields
    """
    buy_date = serializers.SerializerMethodField()
    sell_date = serializers.SerializerMethodField()
    profit = serializers.SerializerMethodField()
    loss = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = ("id", "name", "buy_date", "sell_date", "buy_price", "sell_price", "units", "profit", "loss")

    def get_buy_date(self, obj):
        return obj.buy_date.strftime("%-d %b %y")

    def get_sell_date(self, obj):
        if obj.sell_date:
            return obj.sell_date.strftime("%-d %b %y")
        return None

    def get_profit(self, obj):
        if obj.sell_price and obj.sell_price > obj.buy_price:
            return (obj.sell_price - obj.buy_price) * obj.units
        elif obj.sell_price and obj.sell_price == obj.buy_price:
            return 0
        return 0

    def get_loss(self, obj):
        if obj.sell_price and obj.sell_price < obj.buy_price:
            return (obj.buy_price - obj.sell_price) * obj.units
        elif obj.sell_price and obj.sell_price == obj.buy_price:
            return 0
        return 0