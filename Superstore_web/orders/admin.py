from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(mm_order)
admin.site.register(mm_address)
admin.site.register(mm_customer)
admin.site.register(mm_product)
admin.site.register(mm_category)
admin.site.register(mm_sub_category)
admin.site.register(mm_order_product)
admin.site.register(mm_shipping_details)
admin.site.register(mm_customer_address)