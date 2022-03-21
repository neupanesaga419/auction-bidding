# Generated by Django 4.0.2 on 2022-02-17 17:00

import auctionApp.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctionApp', '0008_remove_product_category_id_remove_product_creator_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BiddingTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_day', models.DateField()),
                ('bid_start_time', models.TimeField()),
                ('bid_end_time', models.TimeField()),
                ('added_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=18)),
                ('category_details', models.CharField(max_length=150)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_bid_amount', models.FloatField()),
                ('product_name', models.CharField(max_length=20)),
                ('product_description', models.CharField(max_length=200)),
                ('product_image_name', models.CharField(max_length=100)),
                ('product_image_path', models.ImageField(upload_to=auctionApp.models.user_directory_path)),
                ('added_date', models.DateTimeField(auto_now=True)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctionApp.category')),
                ('creator_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product_bid_time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctionApp.biddingtime')),
            ],
        ),
    ]