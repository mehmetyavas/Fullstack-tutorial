# Generated by Django 4.0.6 on 2022-07-24 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0078_image_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='urun_foto',
            field=models.ImageField(default=1, max_length=200, upload_to='', verbose_name='Index Foto'),
            preserve_default=False,
        ),
    ]