# Generated by Django 2.2 on 2020-05-06 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rai_smartInventory', '0009_auto_20200505_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
