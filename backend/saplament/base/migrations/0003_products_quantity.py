# Generated by Django 4.0.6 on 2022-07-16 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_remove_products_category_id_products_category_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
