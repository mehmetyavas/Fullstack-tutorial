# Generated by Django 4.0.6 on 2022-07-19 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0033_rename_name_footerurl_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hakkimizda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Ilesitim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]