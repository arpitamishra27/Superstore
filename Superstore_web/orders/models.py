from django.db import models
from datetime import datetime

# Create your models here.
class mm_customer(models.Model):
    
    class Meta:
        db_table = 'mm_customer'

    def __str__(self):
        return self.customer_id.customer_id

    id = models.AutoField(primary_key=True)
    customer_id = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    segment = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.customer_id = ( self.first_name[0].upper()
                        + self.last_name[0].upper() + '-'
                        + str(mm_customer.objects.latest('id').id + 1))
        super(mm_customer, self).save(*args, **kwargs)

class mm_address(models.Model):

    class Meta:
        db_table = 'mm_address'

    address_id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=50)
    add_state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    market = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.address_id = mm_address.objects.latest('address_id').address_id + 1
        super(mm_address, self).save(*args, **kwargs)


class mm_customer_address(models.Model):

    class Meta:
        db_table = 'mm_customer_address'
        unique_together = (('address_id', 'customer_id'),)

    id = models.AutoField(primary_key=True)
    address_id = models.ForeignKey(mm_address, related_name="customer_to_address", on_delete=models.DO_NOTHING, db_column= 'address_id')
    customer_id = models.ForeignKey(mm_customer, related_name="address_to_customer", on_delete=models.CASCADE, db_column= 'customer_id')
    postal_code = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class mm_category(models.Model):

    class Meta:
        db_table = 'mm_category'

    category_id = models.AutoField(primary_key=True) 
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category

class mm_sub_category(models.Model):

    class Meta:
        db_table = 'mm_sub_category'

    sub_category_id = models.AutoField(primary_key=True)
    category_id = models.ForeignKey(mm_category, related_name="sub_to_category", on_delete=models.DO_NOTHING, db_column= 'category_id') 
    sub_category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sub_category

class mm_product(models.Model):

    class Meta:
        db_table = 'mm_product'

    id = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=20, null=True)
    category_id = models.ForeignKey(mm_category, related_name="product_to_category", on_delete=models.DO_NOTHING, db_column= 'category_id')
    sub_category_id = models.ForeignKey(mm_sub_category, related_name="product_to_sub_category", on_delete=models.DO_NOTHING, db_column= 'sub_category_id')
    product_name = models.CharField(max_length=150)
    mrp = models.DecimalField(max_digits=5, decimal_places=2)
    manu_cost = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def save(self, *args, **kwargs):
        if not self.pk:
            self.product_id = ( self.category_id.category[:3].upper() + '-'
                        + self.sub_category_id.sub_category[:2].upper() + '-'
                        + str(mm_product.objects.latest('id').id + 1))
        super(mm_product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name

class mm_order(models.Model):

    class Meta:
        db_table = 'mm_order'

    order_id = models.CharField(primary_key=True, max_length=50)
    order_date = models.DateField(auto_now=True)
    return_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer_id = models.ForeignKey(mm_customer, related_name="order_to_customer",on_delete=models.DO_NOTHING, db_column= 'customer_id')    

class mm_order_product(models.Model):

    class Meta:
        db_table = 'mm_order_product'

    order_product_id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    order_id = models.ForeignKey(mm_order, related_name="item_to_order", on_delete=models.CASCADE, db_column= 'order_id')
    product_id = models.ForeignKey(mm_product, related_name="item_to_product", on_delete=models.DO_NOTHING, db_column= 'product_id')

class mm_shipping_details(models.Model):

    class Meta:
        db_table = 'mm_shipping_details'

    ship_id = models.AutoField(primary_key=True)
    priority = models.CharField(max_length=20) 
    ship_date = models.DateField()
    ship_mode = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    order_id = models.ForeignKey(mm_order, related_name="ship_to_order", on_delete=models.DO_NOTHING, db_column= 'order_id')
  
