# Generated by Django 4.2.9 on 2024-01-21 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DailyPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('open_price', models.FloatField()),
                ('high_price', models.FloatField()),
                ('low_price', models.FloatField()),
                ('close_price', models.FloatField()),
                ('shares_traded', models.BigIntegerField()),
                ('turnover', models.FloatField()),
                ('index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_prices', to='stocks.index')),
            ],
        ),
    ]
