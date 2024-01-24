# Generated by Django 4.2.9 on 2024-01-22 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_index_dailyprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyprice',
            name='close_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='dailyprice',
            name='high_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='dailyprice',
            name='index',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.index'),
        ),
        migrations.AlterField(
            model_name='dailyprice',
            name='low_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='dailyprice',
            name='open_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='dailyprice',
            name='turnover',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
        migrations.AlterField(
            model_name='index',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]