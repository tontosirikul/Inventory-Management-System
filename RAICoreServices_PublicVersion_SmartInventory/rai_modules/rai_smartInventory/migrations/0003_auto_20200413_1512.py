# Generated by Django 2.2.3 on 2020-04-13 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rai_smartInventory', '0002_auto_20200413_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='rai_smartInventory.GroupofItem'),
        ),
    ]
