# Generated by Django 4.0.6 on 2022-07-19 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_rename_item_deneme_cartitem_item'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='item',
            new_name='items',
        ),
    ]