# Generated by Django 2.0.7 on 2018-07-30 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20180729_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='toppings',
            field=models.ManyToManyField(blank=True, related_name='_orderitem_toppings_+', to='orders.Topping'),
        ),
    ]
