# Generated by Django 2.0.7 on 2018-07-31 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_auto_20180731_0121'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('o', 'ongoing'), ('p', 'pending'), ('c', 'confirmed')], default='p', max_length=1),
        ),
    ]