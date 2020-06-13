from django.core.cache import cache
from django.db import models
from django.db.models import Manager


# Create your models here.
class ModelBase(models.Model):
    """
    Model to save created at and updated at time and date
    """
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class Stock(ModelBase):
    """
    Model to save Stocks
    """
    name = models.CharField(verbose_name="Stock Name", max_length=255)
    buy_date = models.DateField(verbose_name="Buy Date")
    sell_date = models.DateField(verbose_name="Sold Date", null=True, blank=True)
    buy_price = models.DecimalField(verbose_name="Buy Price", max_digits=10, decimal_places=2)
    sell_price = models.DecimalField(verbose_name="Sell Price", max_digits=10, decimal_places=2, null=True, blank=True)
    units = models.IntegerField()

    objects = Manager()

    def __str__(self):
        return f"Stock : {self.name} - Units : {self.units}"

    def save(self, *args, **kwargs):
        cache.clear()
        super(Stock, self).save(*args, **kwargs)
