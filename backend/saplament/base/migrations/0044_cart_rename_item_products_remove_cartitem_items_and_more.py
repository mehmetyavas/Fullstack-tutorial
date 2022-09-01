# Generated by Django 4.0.6 on 2022-07-20 12:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0043_alter_hakkimizda_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('ordered', models.BooleanField(default=False)),
            ],
        ),
        migrations.RenameModel(
            old_name='Item',
            new_name='Products',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='items',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='ordered_date',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='start_date',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.products'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cartitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Total Fiyat'),
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(null=True, to='base.cartitem'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]