# Generated by Django 2.0.7 on 2018-07-31 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20180731_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='add_ons',
            field=models.ManyToManyField(blank=True, related_name='_orderitem_add_ons_+', to='orders.AddOn'),
        ),
    ]
