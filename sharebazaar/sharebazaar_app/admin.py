from django.contrib import admin
from django.contrib.auth.models import Group, User
from sharebazaar_app.models import Stock


# Register your models here.
admin.site.register([Stock])
admin.site.unregister([Group, User])