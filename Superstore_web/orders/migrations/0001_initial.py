# Generated by Django 4.0.4 on 2023-04-18 03:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='mm_address',
            fields=[
                ('address_id', models.AutoField(primary_key=True, serialize=False)),
                ('city', models.CharField(max_length=50)),
                ('add_state', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('region', models.CharField(max_length=50)),
                ('market', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'mm_address',
            },
        ),
        migrations.CreateModel(
            name='mm_category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'mm_category',
            },
        ),
        migrations.CreateModel(
            name='mm_customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('customer_id', models.CharField(max_length=20)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('segment', models.CharField(max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'mm_customer',
            },
        ),
        migrations.CreateModel(
            name='mm_order',
            fields=[
                ('order_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('order_date', models.DateField(auto_now=True)),
                ('return_status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer_id', models.ForeignKey(db_column='customer_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='order_to_customer', to='orders.mm_customer')),
            ],
            options={
                'db_table': 'mm_order',
            },
        ),
        migrations.CreateModel(
            name='mm_sub_category',
            fields=[
                ('sub_category_id', models.AutoField(primary_key=True, serialize=False)),
                ('sub_category', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category_id', models.ForeignKey(db_column='category_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='sub_to_category', to='orders.mm_category')),
            ],
            options={
                'db_table': 'mm_sub_category',
            },
        ),
        migrations.CreateModel(
            name='mm_shipping_details',
            fields=[
                ('ship_id', models.AutoField(primary_key=True, serialize=False)),
                ('priority', models.CharField(max_length=20)),
                ('ship_date', models.DateField()),
                ('ship_mode', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order_id', models.ForeignKey(db_column='order_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='ship_to_order', to='orders.mm_order')),
            ],
            options={
                'db_table': 'mm_shipping_details',
            },
        ),
        migrations.CreateModel(
            name='mm_product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_id', models.CharField(max_length=20, null=True)),
                ('product_name', models.CharField(max_length=150)),
                ('mrp', models.DecimalField(decimal_places=2, max_digits=5)),
                ('manu_cost', models.DecimalField(decimal_places=2, max_digits=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category_id', models.ForeignKey(db_column='category_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_to_category', to='orders.mm_category')),
                ('sub_category_id', models.ForeignKey(db_column='sub_category_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_to_sub_category', to='orders.mm_sub_category')),
            ],
            options={
                'db_table': 'mm_product',
            },
        ),
        migrations.CreateModel(
            name='mm_order_product',
            fields=[
                ('order_product_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('shipping_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order_id', models.ForeignKey(db_column='order_id', on_delete=django.db.models.deletion.CASCADE, related_name='item_to_order', to='orders.mm_order')),
                ('product_id', models.ForeignKey(db_column='product_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='item_to_product', to='orders.mm_product')),
            ],
            options={
                'db_table': 'mm_order_product',
            },
        ),
        migrations.CreateModel(
            name='mm_customer_address',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('postal_code', models.CharField(max_length=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('address_id', models.ForeignKey(db_column='address_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='customer_to_address', to='orders.mm_address')),
                ('customer_id', models.ForeignKey(db_column='customer_id', on_delete=django.db.models.deletion.CASCADE, related_name='address_to_customer', to='orders.mm_customer')),
            ],
            options={
                'db_table': 'mm_customer_address',
                'unique_together': {('address_id', 'customer_id')},
            },
        ),
    ]
