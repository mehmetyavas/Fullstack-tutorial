# Generated by Django 4.0.6 on 2022-07-20 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0045_remove_cart_ordered_remove_cartitem_ordered_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='items',
            new_name='cart_item',
        ),
    ]
