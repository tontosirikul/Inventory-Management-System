# Generated by Django 2.2 on 2020-04-27 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rai_smartInventory', '0005_auto_20200427_0805'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='items',
            new_name='items_id',
        ),
    ]
