# Generated by Django 4.0.6 on 2022-07-18 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_item_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(blank=True, to='base.orderitem'),
        ),
    ]
