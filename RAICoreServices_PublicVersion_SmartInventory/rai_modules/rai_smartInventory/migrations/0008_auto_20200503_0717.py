# Generated by Django 2.2 on 2020-05-03 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rai_smartInventory', '0007_auto_20200427_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
