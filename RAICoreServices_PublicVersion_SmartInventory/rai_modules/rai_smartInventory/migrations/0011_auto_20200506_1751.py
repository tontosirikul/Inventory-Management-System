# Generated by Django 2.2 on 2020-05-06 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rai_smartInventory', '0010_order_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_returned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='is_returned',
            field=models.BooleanField(default=False),
        ),
    ]
