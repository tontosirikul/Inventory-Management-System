# Generated by Django 2.2.3 on 2020-04-13 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rai_smartInventory', '0002_auto_20200413_1502'),
        ('rai_user', '0005_auto_20200330_0430'),
    ]

    operations = [
        migrations.AddField(
            model_name='raiuser',
            name='cart',
            field=models.ManyToManyField(blank=True, to='rai_smartInventory.GroupofItem'),
        ),
    ]
