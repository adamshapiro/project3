# Generated by Django 2.0.7 on 2018-07-31 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20180731_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='toppings',
            field=models.ManyToManyField(related_name='_orderitem_toppings_+', to='orders.Topping'),
        ),
    ]
