# Generated by Django 4.0.6 on 2022-07-24 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0075_image_alter_products_urun_foto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='urun_foto',
        ),
        migrations.AddField(
            model_name='products',
            name='urun_foto',
            field=models.ManyToManyField(null=True, to='base.image'),
        ),
    ]