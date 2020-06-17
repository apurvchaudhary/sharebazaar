from django.contrib import admin
from django.contrib.auth.models import Group, User

from sharebazaar_app.models import Stock

# Register your models here.
admin.site.register([Stock])
admin.site.unregister([Group, User])
admin.site.site_header = 'Stock Exchange Login'
admin.site.site_title = 'My Account'
admin.site.index_title = 'My Stocks'
admin.site.site_url = "/home/"
