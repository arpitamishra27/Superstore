from rest_framework import serializers
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = mm_customer
        fields = ['customer_id', 'first_name', 'last_name', 'segment']

class ShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = mm_shipping_details
        fields = ['ship_id', 'order_id', 'ship_date']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = mm_product
        fields = ['product_id', 'product_name', 'mrp']

class OrderProductSerializer(serializers.ModelSerializer):
    item_to_product = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = mm_order_product
        fields = ['product_id','quantity','discount','shipping_cost','item_to_product' ]

class OrderSerializer( serializers.ModelSerializer):
    customer_id =  serializers.SlugRelatedField(slug_field='customer_id', read_only=True)
    # url = serializers.HyperlinkedIdentityField(view_name='order_details',read_only=True)
    ship_to_order = ShipSerializer(many=True, read_only=True)
    item_to_order = OrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = mm_order
        fields = ['order_id', 'order_date','return_status', 'customer_id', 'ship_to_order', 'item_to_order']
